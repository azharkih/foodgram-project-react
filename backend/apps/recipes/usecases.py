from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .models import RecipeIngredient


def get_ingredients_for_buy(user):
    ingredients_for_buy = {}
    ingredients = RecipeIngredient.objects.filter(
        recipe__cart_items__user=user).values_list(
        'ingredient__name', 'ingredient__measurement_unit',
        'amount')
    for item in ingredients:
        name = item[0]
        if name not in ingredients_for_buy:
            ingredients_for_buy[name] = {
                'measurement_unit': item[1],
                'amount': item[2]
            }
        else:
            ingredients_for_buy[name]['amount'] += item[2]
    return ingredients_for_buy


def add_shopping_cart_pdf_to_response(user, response):
    ingredients_for_buy = get_ingredients_for_buy(user)
    pdfmetrics.registerFont(TTFont('yahfie', 'yahfie.ttf'))
    page = canvas.Canvas(response)
    page.setFont('yahfie', size=24)
    page.drawString(200, 800, 'Список ингредиентов')
    page.setFont('yahfie', size=16)
    height = 750
    for i, (name, data) in enumerate(ingredients_for_buy.items(), 1):
        page.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
                                     f'{data["measurement_unit"]}'))
        height -= 25
    page.showPage()
    page.save()
