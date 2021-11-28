from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import Ingredient, Recipe, RecipeIngredient, Tag
from .tools.serializers import Base64ImageField
from ..users.serializers import CustomUserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        validators = [
            UniqueTogetherValidator(
                queryset=RecipeIngredient.objects.all(),
                fields=['ingredient', 'recipe']
            )
        ]


class RecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)
    tags = TagSerializer(read_only=True, many=True)
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(
        read_only=True, many=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart_items__user=user, id=obj.id).exists()

    def validate(self, data):
        ingredients = self.initial_data.get('ingredients')
        if not ingredients:
            raise serializers.ValidationError({
                'ingredients': 'Не добавлен ни один ингридиент'})
        ingredient_list = []
        for ingredient_item in ingredients:
            ingredient = Ingredient.objects.get(id=ingredient_item['id'])
            if not ingredient:
                raise serializers.ValidationError('Неизвестный ингредиент')
            if ingredient in ingredient_list:
                raise serializers.ValidationError('Ингридиенты должны '
                                                  'быть уникальными')
            ingredient_list.append(ingredient)
            if int(ingredient_item['amount']) < 0:
                raise serializers.ValidationError({
                    'ingredients': 'единица измерения -- положительное число'
                })
        data['ingredients'] = ingredients
        return data

    def create(self, validated_data, **kwargs):
        ingredients = validated_data.pop('ingredients')
        recipe = super().create(validated_data)
        self._create_ingredients(ingredients, recipe)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        recipe = super().update(instance, validated_data)
        recipe.ingredients.all().delete()
        self._create_ingredients(ingredients, recipe)
        tags_data = self.initial_data.get('tags')
        recipe.tags.set(tags_data)
        return recipe

    @staticmethod
    def _create_ingredients(ingredients, recipe):
        ingredients = [RecipeIngredient(ingredient_id=ingredient['id'],
                                        recipe=recipe,
                                        amount=ingredient['amount'])
                       for ingredient in ingredients]
        RecipeIngredient.objects.bulk_create(ingredients)


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField(use_url=True)

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')
