from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class LimitPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'limit'


def add_obj(self, model, user, pk):
    obj = get_object_or_404(model, id=pk)
    model.objects.get_or_create(user=user, recipe=recipe)
    serializer = CropRecipeSerializer(recipe)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


def delete_obj(self, model, user, pk):
    obj = model.objects.filter(user=user, recipe__id=pk)
    if obj.exists():
        obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({
        'errors': 'Рецепт уже удален'
    }, status=status.HTTP_400_BAD_REQUEST)
