import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import time
import re
import os
import datetime


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_cart(driver):
    driver.implicitly_wait(10)

    for product_counter in range(0,3):
        driver.get("http://localhost/litecart/")
        products = driver.find_elements_by_css_selector("a.link")

        products[0].click()
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=add_cart_product]")))

        size = Select(driver.find_element_by_name('options[Size]'))
        size.select_by_index(product_counter+1)  # нулевая опция - это просто подсказка --Select--, поэтому начинаем с 1

        # Сохраняем начальное число товаров в корзине
        ititial_number_of_items = int(driver.find_element_by_css_selector("#cart .quantity").get_attribute("textContent"))

        button = driver.find_element_by_css_selector("button[name=add_cart_product]")
        button.click()

        # Ждем, пока значение в корзине увеличится на 1
        WebDriverWait(driver,10).until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cart .quantity"),str(ititial_number_of_items+1)))

    # Заходим в корзину (через главную страницу)
    driver.get("http://localhost/litecart/")
    driver.find_element_by_css_selector("a.image").click()

    # Удаляем товары из корзины по очереди
    for product_counter in range(0,3):
        trash_button = driver.find_element_by_css_selector("button[name='remove_cart_item'")
        trash_button.click()
        WebDriverWait(driver,10).until(EC.staleness_of(trash_button))




