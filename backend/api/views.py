from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredients, Recipe,
                            ShoppingCart, Tags, IngredientAmount)
from rest_framework import status, mixins, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated, AllowAny,
                                        IsAuthenticatedOrReadOnly,)
from rest_framework.response import Response

from users.models import Subscription, UserFoodgram
from .filters import IngredientsFilter, RecipeFilter
from .paginators import CustomPagination
from .serializers import (CreateRecipeSerializer, FavoriteSerializer,
                          IngredientsSerializer, RecipeReadSerializer,
                          ShoppingCartSerializer, TagsSerializer,
                          UserFoodgramSerializer, SubscriptionSerializer,
                          RecipeSubscriptionSerializer)


class TagsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """Вывод тегов."""
    queryset = Tags.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (AllowAny,)


class IngredientsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin
):
    """Вывод ингредиентов."""
    pagination_class = None
    queryset = Ingredients.objects.all()
    serializer_class = IngredientsSerializer
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('name',)
    ordering_fields = ('name',)
    filterset_class = IngredientsFilter
    permission_classes = (AllowAny,)


class RecipeViewSet(viewsets.ModelViewSet):
    """Работа с рецептами."""
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Recipe.objects.all()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response('Рецепт успешно удален',
                        status=status.HTTP_204_NO_CONTENT)

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeReadSerializer
        return CreateRecipeSerializer

    def get_queryset(self):
        is_favorited = self.request.query_params.get('is_favorited') or 0
        if int(is_favorited) == 1:
            return Recipe.objects.filter(
                favorites__user=self.request.user
            )
        is_in_shopping_cart = self.request.query_params.get(
            'is_in_shopping_cart') or 0
        if int(is_in_shopping_cart) == 1:
            return Recipe.objects.filter(
                cart__user=self.request.user
            )
        return Recipe.objects.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def delete_obj(self, request, pk, model):
        recipe = get_object_or_404(Recipe, pk=pk)
        if model.objects.filter(user=request.user, recipe=recipe).exists():
            follow = get_object_or_404(model, user=request.user,
                                       recipe=recipe)
            follow.delete()
            return Response(
                'Рецепт успешно удален из избранного/списка покупок',
                status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            {'errors': 'Данного рецепта не было в избранном/списке покупок'},
            status=status.HTTP_400_BAD_REQUEST
        )

    def post_obj(self, request, pk, model, serializer):
        recipe = get_object_or_404(Recipe, pk=pk)
        if model.objects.filter(user=request.user, recipe=recipe).exists():
            return Response(
                {'errors': 'Рецепт уже есть в избранном/списке покупок'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        model.objects.get_or_create(user=request.user, recipe=recipe)
        data = serializer(recipe).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=('POST', 'DELETE'), )
    def favorite(self, request, pk):
        if self.request.method == 'POST':
            return self.post_obj(
                request, pk, Favorite, RecipeSubscriptionSerializer
            )
        return self.delete_obj(request, pk, Favorite)

    @action(detail=True, methods=('POST', 'DELETE'), )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.post_obj(
                request, pk, ShoppingCart, RecipeSubscriptionSerializer
            )
        return self.delete_obj(request, pk, ShoppingCart)

    @action(detail=False, methods=('GET',), )
    def download_shopping_cart(self, request):
        if not request.user.cart.exists():
            return Response(
                'В корзине нет товаров', status=status.HTTP_400_BAD_REQUEST)
        ingredients = (
            IngredientAmount.objects
            .filter(recipe__cart__user=request.user)
            .values('ingredient')
            .annotate(total_amount=Sum('amount'))
            .values_list(
                'ingredient__name',
                'total_amount',
                'ingredient__measurement_unit'
            )
        )

        text = ''
        for ingredient in ingredients:
            text += '{} - {} {}. \n'.format(*ingredient)

        file = HttpResponse(
            f'Покупки:\n {text}', content_type='text/plain'
        )

        file['Content-Disposition'] = ('attachment; filename=cart.txt')
        return file


class UserFoodgramViewSet(UserViewSet):
    """Работа с юзерами."""
    queryset = UserFoodgram.objects.all()
    serializer_class = UserFoodgramSerializer
    pagination_class = LimitOffsetPagination

    @action(
        detail=False,
        methods=('POST',),
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(UserFoodgram, pk=id)

        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                author, data=request.data, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            Subscription.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            get_object_or_404(
                Subscription, user=user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = UserFoodgram.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Создание токена."""

    email = request.data.get('email')
    password = request.data.get('password')

    if None not in (email, password):
        user = get_object_or_404(
            UserFoodgramSerializer,
            email=email,
            password=password
        )
        token = Token.objects.create(user=user)
        return Response({'auth_token': str(token.key), })
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_token(request):
    """Создание токена."""
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
