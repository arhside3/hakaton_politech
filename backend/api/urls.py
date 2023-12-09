from django.urls import include, path

from rest_framework.routers import DefaultRouter

from api.views import (
    RecipeViewSet,
    TagViewSet,
    UserView,
    SubscriptionList,
)

router_v1 = DefaultRouter()
router_v1.register(r'users', UserView)
router_v1.register(r'recipes', RecipeViewSet, basename='recipe')
router_v1.register(r'tags', TagViewSet, basename='tag')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('', include('djoser.urls')),
    path('users/subscriptions/', SubscriptionList.as_view()),
    path('auth/', include('djoser.urls.authtoken')),
]
