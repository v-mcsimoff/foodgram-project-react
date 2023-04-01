from rest_framework.routers import DefaultRouter

from django.urls import include, path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import (RecipeViewSet, TagsViewSet,
                    IngredientsViewSet, UserFoodgramViewSet)

app_name = 'api'


router = DefaultRouter()
router.register('recipe', RecipeViewSet, basename='recipe')
router.register('tags', TagsViewSet, basename='tags')
router.register('ingredients', IngredientsViewSet, basename='ingredients')
router.register('users', UserFoodgramViewSet, basename='user')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]

urlpatterns += staticfiles_urlpatterns()
