from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from .main_page import MainPage

class ProductPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.main_page = MainPage(self.driver)

    def open(self, product_number):
        self.main_page.get_products()[product_number].click()
        WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=add_cart_product]")))

    def select_size(self, size_index):
        size = Select(self.driver.find_element_by_name('options[Size]'))
        # в этом селекте размеры нумеруются с 1, т.к. нулевой размер - это просто подсказка "--Select--"
        size.select_by_index(size_index + 1)

    def add_to_cart(self, ititial_number_of_items):
        button = self.driver.find_element_by_css_selector("button[name=add_cart_product]")
        button.click()
        # Ждем, пока количество товаров в корзине увеличится на 1
        WebDriverWait(self.driver,10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart .quantity"),str(ititial_number_of_items + 1)))