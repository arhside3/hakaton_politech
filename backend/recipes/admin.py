from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.safestring import mark_safe
from django.contrib.auth.admin import UserAdmin

from recipes.models import (
    Favorite,
    Recipe,
    ShoppingCart,
    Tag,
    User,
    Subscribe,
)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
        'cooking_time',
        'grade',
        'get_favorites_count',
        'get_image_recipe',
        'get_tags',
    )
    fields = (
        'name',
        'author',
        'tags',
        'text',
        'image',
    )
    list_filter = ('author', 'tags')

    @admin.display(description='картинка')
    def get_image_recipe(self, image_recipe):
        if image_recipe.image:
            return mark_safe(
                f'<img src="{image_recipe.image.url}" width="50" height="50"/>'
            )
        else:
            return '-'

    @admin.display(description='тэги')
    def get_tags(self, tags_list):
        return mark_safe(', '.join(tag.name for tag in tags_list.tags.all()))

    @admin.display(description='в избранном')
    def get_favorites_count(self, favorites_count):
        return favorites_count.favorites.count()


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug', 'color_tag')

    @admin.display(description='цвет тэга')
    def color_tag(self, color_tag):
        return mark_safe(
            (
                '<div style="width: 20px; height: 20px; background-color:'
                f'{color_tag.color};"></div>'
            )
        )


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user')


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = (
        'id',
        'first_name',
        'last_name',
        'username',
        'email',
        'subscriptions',
        'followers',
        'count_recipes',
    )

    def subscriptions(self, subscriptions):
        return subscriptions.subscriber.count()

    def followers(self, followers):
        return followers.subscriber.count()

    def count_recipes(self, count_recipes):
        return count_recipes.recipes.count()


@admin.register(Subscribe)
class SubscribeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'author',
    )
    list_display_links = ('id', 'user')


admin.site.unregister(Group)
