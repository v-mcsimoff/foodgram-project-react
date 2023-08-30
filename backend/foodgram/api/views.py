from django.http import HttpResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from api import filters, mixins, serializers, paginators
from recipes import models


class IngredientViewSet(mixins.RetrieveListViewSet):
    """Processing of operations with ingredients."""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientListSerializer
    pagination_class = (None)
    permission_classes = (AllowAny, )
    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.IngredientFilter


class TagViewSet(mixins.RetrieveListViewSet):
    """Processing of operations with tags."""

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = (None)
    permission_classes = (AllowAny, )


class RecipeViewSet(viewsets.ModelViewSet):
    """Processing of operations with recipe."""

    filter_backends = (DjangoFilterBackend,)
    filterset_class = filters.RecipeFilter
    pagination_class = paginators.PageLimitPagination

    def get_queryset(self):
        favorite = self.request.query_params.get('is_favorited')
        shop = self.request.query_params.get('is_in_shopping_cart')
        queryset = models.Recipe.objects.all()
        if favorite:
            queryset = queryset.filter(
                favorite_recipe__user=self.request.user
            )
        if shop:
            queryset = queryset.filter(
                shopping__user=self.request.user
            )
        return queryset

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            permission_classes = (AllowAny, )
        else:
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return serializers.RecipeWriteSerializer
        return serializers.RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user
        )

    def _recipes_list(self, request, serializer, model):
        user = self.request.user
        recipe = get_object_or_404(models.Recipe, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            data = {}
            data['user'] = user.id
            data['recipe'] = recipe.pk
            serializer = serializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.get_serializer(recipe)
            return Response(serializer.data)
        if request.method == 'DELETE':
            current_recipe = get_object_or_404(
                model,
                user=user,
                recipe=recipe
            )
            current_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], name='download')
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = models.Recipe.objects.filter(
            shopping__user=user
        ).values_list(
            'ingredients__ingredient__name',
            'ingredients__ingredient__measurement_unit__name'
        ).annotate(amount=Sum('ingredients__amount'))
        response = HttpResponse(content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename="sc.txt"'
        for name, mu, amount in shopping_cart:
            response.write(f'-{name}({mu})-{amount}\n')
        return response

    @action(detail=True, methods=['post', 'delete'], name='favorite')
    def favorite(self, request, pk=None):
        """Processing of operations with favorite."""
        return self._recipes_list(
            request,
            serializers.FavoritedSerializer,
            models.FavoriteRecipe
        )

    @action(detail=True, methods=['post', 'delete'], name='favorite')
    def shopping_cart(self, request, pk=None):
        """Processing of operations with the cart."""
        return self._recipes_list(
            request,
            serializers.ShoppingCartSerializer,
            models.ShopRecipe
        )


class UserViewSet(viewsets.ModelViewSet):
    """Processing of operations with users."""

    queryset = serializers.User.objects.all()

    def get_serializer_class(self):
        pk = self.kwargs.get('pk')
        sub_path = (
            reverse('api:users-subscriptions'),
            reverse('api:users-subscribe', kwargs={'pk': pk})
        )
        if self.request.path in sub_path:
            return serializers.UserSubsrcibeSerializer
        if self.action == 'create':
            return serializers.UserCreateSerializer
        return serializers.UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = (AllowAny, )
        else:
            permission_classes = (IsAuthenticated, )
        return [permission() for permission in permission_classes]

    def get_object(self):
        if self.request.path == reverse(
            'api:users-detail', kwargs={'pk': 'me'}
        ):
            return self.request.user
        return super().get_object()

    @action(detail=False, methods=['post'], name='set_password')
    def set_password(self, request):
        new_password = request.data.get('new_password')
        current_password = request.data.get('current_password')
        user = self.request.user
        if user.password == current_password:
            user.password = new_password
            user.save()
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        return Response(request.data)

    @action(detail=False, methods=['get'], name='subscriptions')
    def subscriptions(self, request):
        user = request.user
        following = models.User.objects.filter(
            following__user=user
        )
        paginator = self.paginate_queryset(following)
        serializer = self.get_serializer(paginator, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post', 'delete'], name='follow')
    def subscribe(self, request, pk=None):
        """Processing of operations with subscriptions."""
        user = self.request.user
        author = get_object_or_404(models.User, id=self.kwargs.get('pk'))
        if request.method == 'POST':
            data = {}
            data['user'] = user.id
            data['author'] = author.id
            serializer = serializers.FollowingSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            serializer = self.get_serializer(instance=author)
            return Response(serializer.data)
        if request.method == 'DELETE':
            subscribe = get_object_or_404(
                models.Following,
                user=user,
                author=author
            )
            subscribe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Token creation."""

    email = request.data.get('email')
    password = request.data.get('password')

    if None not in (email, password):
        user = get_object_or_404(
            serializers.User,
            email=email,
            password=password
        )
        token = Token.objects.create(user=user)
        return Response({'auth_token': str(token.key), })
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_token(request):
    """Logout token creation."""
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
