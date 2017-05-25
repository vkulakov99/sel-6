import pytest
from application import Application


@pytest.fixture
def app(request):
    app = Application()
    request.addfinalizer(app.quit)
    return app


def test_cart_po(app):

    for product_counter in range(0,3):
        # Открываем главную страницу
        app.open_main_page()
        # Вызываем функцию добавления продукта
        app.add_product(0, product_counter) # нулевой продукт в списке продуктов, размеры нумеруются с нуля

    # Удаляем товары из корзины по очереди
    for product_counter in range(0,3):
        app.delete_product()