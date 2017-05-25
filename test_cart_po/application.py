from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
        # Сохраняем начальное число товаров в корзине
        ititial_number_of_items = self.get_number_of_items_in_cart()

        self.product_page.open(product_number) # открываем продукт с порядковым номером на странице product_number

        self.product_page.select_size(size_index)
        #size = Select(self.driver.find_element_by_name('options[Size]'))
        #size.select_by_index(product.size)  # нулевая опция - это просто подсказка --Select--, поэтому начинаем с 1

        self.product_page.add_to_cart(ititial_number_of_items)
        #button = self.driver.find_element_by_css_selector("button[name=add_cart_product]")
        #button.click()

        # Ждем, пока количество товаров в корзине увеличится на 1
        #WebDriverWait(self.driver,10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart .quantity"),str(ititial_number_of_items+1)))


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