from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.product_page import ProductPage
from pages.cart_page import CartPage
from pages.main_page import MainPage

class Application:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.main_page = MainPage(self.driver)
        self.product_page = ProductPage(self.driver)
        self.cart_page = CartPage(self.driver)


    def quit(self):
        self.driver.quit()


    def add_product(self, product_number, size_index):
        ititial_number_of_items = self.get_number_of_items_in_cart() # Сохраняем начальное число товаров в корзине
        self.product_page.open(product_number) # открываем продукт с порядковым номером на странице product_number
        self.product_page.select_size(size_index) # выбираем размер продукта
        self.product_page.add_to_cart(ititial_number_of_items) # добавляем товар и ждем пока объем корзины увеличится


    def get_number_of_items_in_cart(self):
        self.main_page.open()
        return self.main_page.cart_quantity()


    def delete_product(self):
        self.cart_page.open()
        trash_button = self.cart_page.trash_button
        trash_button.click()
        WebDriverWait(self.driver,10).until(EC.staleness_of(trash_button))


    def open_cart(self):
        self.cart_page.open()


    def open_main_page(self):
        self.main_page.open()