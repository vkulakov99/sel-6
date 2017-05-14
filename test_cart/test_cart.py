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
    driver.get("http://localhost/litecart/")
    products = driver.find_elements_by_css_selector("a.link")

    products[0].click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=add_cart_product]")))
    product_name = driver.find_element_by_css_selector("h1.title").text

    size = Select(driver.find_element_by_name('options[Size]'))
    size.select_by_visible_text("Small")

    # Сохраняем начальное число товаров в корзине
    cart_content = driver.find_element_by_css_selector("div.content").text
    m = re.search('(\d+) item\(s\)', cart_content)
    ititial_number_of_items = int(m.group(1))

    button = driver.find_element_by_css_selector("button[name=add_cart_product]")
    button.click()

    i = 0
    while True:
        if i > 20:
            raise Exception("В течение 10 секунд счетчик товаров в корзине не обновился.")
        cart_content = driver.find_element_by_css_selector("div.content").text
        m = re.search('(\d+) item\(s\)', cart_content)
        changed_number_of_items = int(m.group(1))
        if changed_number_of_items - ititial_number_of_items == 1:
            print ("Товар " + product_name + " размером \"Small\" успешно добавлен в корзину.")
            break
        time.sleep(0.5)
        i+=1

    # Начинаем добавление второго продукта в корзину
    driver.get("http://localhost/litecart/")
    products = driver.find_elements_by_css_selector("a.link")
    products[0].click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=add_cart_product]")))
    product_name = driver.find_element_by_css_selector("h1.title").text

    size = Select(driver.find_element_by_name('options[Size]'))
    size.select_by_visible_text("Medium +$2.50")

    cart_content = driver.find_element_by_css_selector("div.content").text
    m = re.search('(\d+) item\(s\)', cart_content)
    ititial_number_of_items = int(m.group(1))

    button = driver.find_element_by_css_selector("button[name=add_cart_product]")
    button.click()

    i = 0
    while True:
        if i > 20:
            raise Exception("В течение 10 секунд счетчик товаров в корзине не обновился.")
        cart_content = driver.find_element_by_css_selector("div.content").text
        m = re.search('(\d+) item\(s\)', cart_content)
        changed_number_of_items = int(m.group(1))
        if changed_number_of_items - ititial_number_of_items == 1:
            print ("Товар " + product_name + " размером \"Medium\" успешно добавлен в корзину.")
            break
        time.sleep(0.5)
        i+=1

    # Начинаем добавление третьего продукта в корзину
    driver.get("http://localhost/litecart/")
    products = driver.find_elements_by_css_selector("a.link")
    products[0].click()
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button[name=add_cart_product]")))
    product_name = driver.find_element_by_css_selector("h1.title").text

    size = Select(driver.find_element_by_name('options[Size]'))
    size.select_by_visible_text("Large +$5")

    cart_content = driver.find_element_by_css_selector("div.content").text
    m = re.search('(\d+) item\(s\)', cart_content)
    ititial_number_of_items = int(m.group(1))

    button = driver.find_element_by_css_selector("button[name=add_cart_product]")
    button.click()

    i = 0
    while True:
        if i > 20:
            raise Exception("В течение 10 секунд счетчик товаров в корзине не обновился.")
        cart_content = driver.find_element_by_css_selector("div.content").text
        m = re.search('(\d+) item\(s\)', cart_content)
        changed_number_of_items = int(m.group(1))
        if changed_number_of_items - ititial_number_of_items == 1:
            print ("Товар " + product_name + " размером \"Large\" успешно добавлен в корзину.")
            break
        time.sleep(0.5)
        i+=1

    # Заходим в корзину (через главную страницу)
    driver.get("http://localhost/litecart/")
    driver.find_element_by_css_selector("a.image").click()

    # Удаляем первый из трех товаров из корзины
    trash_buttons = driver.find_elements_by_css_selector("button[name='remove_cart_item'")
    trash_buttons[0].click()
    time.sleep(3)
    footer = driver.find_element_by_css_selector("tr.footer")
    print(footer.find_element_by_css_selector("td:nth-child(2)").text)

    # Удаляем первый из двух оставшихся товаров из корзины
    trash_buttons = driver.find_elements_by_css_selector("button[name='remove_cart_item'")
    trash_buttons[0].click()
    time.sleep(3)
    footer = driver.find_element_by_css_selector("tr.footer")
    print(footer.find_element_by_css_selector("td:nth-child(2)").text)

    # Удаляем последний и единственный товар из корзины
    trash_buttons = driver.find_elements_by_css_selector("button[name='remove_cart_item'")
    trash_buttons[0].click()
    # Ждем, пока таблица внизу исчезнет
    WebDriverWait(driver,10).until(EC.staleness_of(footer))


