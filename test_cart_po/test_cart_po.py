import pytest
from selenium import webdriver
from application import Application


@pytest.fixture
def app(request):
    app = Application()
    request.addfinalizer(app.quit)
    return app
# def driver(request):
#     wd = webdriver.Chrome()
#     request.addfinalizer(wd.quit)
#     return wd


def test_cart_po(app):


    # Описываем новый класс Product
    class Product:
        def __init__(self, size=None):
            self.size = size

    for product_counter in range(0,3):

        # Создаем объект класса Product
        product = Product(size = product_counter+1)

        # Открываем главную страницу
        app.open_main_page()

        # Вызываем функцию добавления продукта
        app.add_product(0, product_counter) # нулевой продукт в списке продуктов, размеры нумеруются с нуля



    # Удаляем товары из корзины по очереди
    for product_counter in range(0,3):
        app.delete_product()