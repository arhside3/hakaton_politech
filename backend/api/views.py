from djoser.views import UserViewSet
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError
from django.http import FileResponse

from api.filters import RecipeFilter
from api.utils import format_shopping_cart
from api.permissions import IsAuthorOrReadOnly
from api.pagination import LimitPageNumberPagination
from api.serializers import (
    CreateRecipeSerializer,
    DefaultRecipeSerializer,
    RecipeSerializer,
    SubscribeSerializer,
    TagSerializer,
)
from recipes.models import (
    Favorite,
    Recipe,
    ShoppingCart,
    Tag,
    Subscribe,
    User,
)


class UserView(UserViewSet):
    pagination_class = LimitPageNumberPagination

    @action(
        detail=True,
        methods=['post'],
        serializer_class=SubscribeSerializer,
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, pk=id)

        if Subscribe.objects.filter(user=user, author=author).exists():
            raise ValidationError('Эта подписка уже существует.')
        if user == author:
            raise ValidationError('Нельзя подписаться на самого себя.')

        Subscribe.objects.create(user=user, author=author)

        serializer = self.get_serializer(author)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def subscribe_delete(self, request, id):
        subscribe = Subscribe.objects.filter(
            user=request.user,
            author=get_object_or_404(User, pk=id),
        )
        if not subscribe.exists():
            raise ValidationError('Подписки не существует.')
        subscribe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubscriptionList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubscribeSerializer
    pagination_class = LimitPageNumberPagination

    def get_queryset(self):
        return Subscribe.objects.filter(subscribing__user=self.request.user)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all().order_by('id')
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = LimitPageNumberPagination

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return CreateRecipeSerializer

    def add_favorite_and_shopping_cart(self, model, user, pk):
        if model.objects.filter(user=user, recipe__id=pk).exists():
            raise ValidationError('Рецепт уже добавлен')
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        return Response(
            DefaultRecipeSerializer(recipe).data,
            status=status.HTTP_201_CREATED,
        )

    def delete_favorite_and_shopping_cart(self, model, user, pk=None):
        model.objects.filter(user=user, recipe__id=pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_favorite_and_shopping_cart(
                Favorite, request.user, pk
            )
        return self.delete_favorite_and_shopping_cart(
            Favorite, request.user, pk
        )

    @action(
        detail=True,
        methods=['POST', 'DELETE'],
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_favorite_and_shopping_cart(
                ShoppingCart, request.user, pk
            )
        return self.delete_favorite_and_shopping_cart(
            ShoppingCart, request.user, pk
        )

    @action(detail=False, methods=("GET",))
    def download_shopping_cart(self, request):
        ingredients = []
        for shopping_cart in ShoppingCart.objects.filter(
            user=request.user
        ).all():
            ingredients += shopping_cart.get_shopping_cart_ingredients()
        return FileResponse(
            format_shopping_cart(ingredients), content_type='text/plain'
        )


class TagViewSet(
    viewsets.ReadOnlyModelViewSet,
):
    permission_classes = (permissions.AllowAny,)
    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
