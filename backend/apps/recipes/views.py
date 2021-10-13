from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from .filters import IngredientFilter, RecipeFilter
from .models import Ingredient, Recipe, Tag
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import (GetRecipeSerializer, IngredientSerializer,
                          SetRecipeSerializer, TagSerializer)
from .tools.views import LimitPagination


class TagViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """ Класс TagsViewSet используется для ...
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAdminOrReadOnly, ]


class IngredientViewSet(RetrieveModelMixin, ListModelMixin, GenericViewSet):
    """ Класс IngredientViewSet используется для ...
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class RecipeViewSet(ModelViewSet):
    """ Класс IngredientViewSet используется для ...
    """
    pagination_class = LimitPagination
    queryset = Recipe.objects.all()
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return GetRecipeSerializer
        return SetRecipeSerializer
