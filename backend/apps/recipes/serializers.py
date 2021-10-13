from rest_framework import serializers

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .tools.serializers import Base64ImageField, CurrentUserId
from ..users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


# def add_ingredients(ingredients):
#     regions = [Region(code=x) for x in region_codes]
#     Region.objects.bulk_create(regions, ignore_conflicts=True)
#     return regions

class RecipeIngredientField(serializers.RelatedField):
    def to_representation(self, value):
        return {'id': value.ingredient.id,
                'name': value.ingredient.name,
                'measurement_unit': value.ingredient.measurement_unit,
                'amount': value.amount}

class SetRecipeSerializer(serializers.ModelSerializer):
    # author_id = serializers.HiddenField(default=CurrentUserId())
    author_id = serializers.IntegerField(default=1)
    image = Base64ImageField(use_url=True)
    ingredients = serializers.ListField()

    def create(self, validated_data, **kwargs):
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        ingredients = [RecipeIngredient(ingredient_id=ingredient['id'],
                                        recipe_id=recipe.id,
                                        amount=ingredient['amount'])
                       for ingredient in ingredients]
        RecipeIngredient.objects.bulk_create(ingredients)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = super().update(validated_data)
        recipe.ingredients.delete()
        self._create_ingredients(ingredients, recipe)
        return recipe

    @staticmethod
    def _create_ingredients(ingredients, recipe):
        ingredients = [RecipeIngredient(ingredient_id=ingredient['id'],
                                        recipe_id=recipe.id,
                                        amount=ingredient['amount'])
                       for ingredient in ingredients]
        RecipeIngredient.objects.bulk_create(ingredients)
    class Meta:
        model = Recipe
        fields = ('tags', 'author_id', 'name', 'text', 'image', 'ingredients',
                  'cooking_time')


class GetRecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer()
    tags = TagSerializer(many=True)
    ingredients = RecipeIngredientField(many=True, read_only=True)
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'name', 'text', 'ingredients',
                  'image', 'cooking_time')

# 'is_favorited',
#             'is_in_shopping_cart',
