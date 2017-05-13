import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import datetime


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_add_product(driver):
    driver.implicitly_wait(10)
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    # driver.find_element_by_css_selector('button[name="login"]').click()
    driver.find_element_by_name("password").send_keys(Keys.ENTER)

    driver.find_element_by_xpath("//span[.='Catalog']").click()

    driver.find_element_by_xpath("//a[.=' Add New Product']").click()

    driver.find_element_by_xpath("//label[.=' Enabled']").click()

    # генерируем уникальный код товара по дате и времени
    now_time = datetime.datetime.now()
    code = now_time.strftime("%d%m%Y%I%M%S")
    driver.find_element_by_xpath("//input[@name='code']").send_keys(code)

    driver.find_element_by_css_selector("input[name='name[en]']").send_keys("AngryDuck")

    driver.find_element_by_xpath("//input[@name='quantity']").send_keys('200')

    weight = driver.find_element_by_xpath("//input[@name='weight']")
    weight.clear()
    weight.send_keys('0,1')

    dim_x = driver.find_element_by_xpath("//input[@name='dim_x']")
    dim_x.clear()
    dim_x.send_keys('9,5')

    dim_y = driver.find_element_by_xpath("//input[@name='dim_y']")
    dim_y.clear()
    dim_y.send_keys('9,5')

    dim_z = driver.find_element_by_xpath("//input[@name='dim_z']")
    dim_z.clear()
    dim_z.send_keys('7,5')

    driver.find_element_by_xpath("//input[@name='product_groups[]'][@value='1-3']").click()

    # Начальная дата - сегодняшнее число
    valid_from = now_time
    driver.find_element_by_xpath("//input[@name='date_valid_from']").send_keys(valid_from.strftime("%d%m%Y"))
    # Конечная дата - через год (365 дней) от начальной даты
    delta = datetime.timedelta(365)
    valid_to = valid_from + delta
    driver.find_element_by_xpath("//input[@name='date_valid_to']").send_keys(valid_to.strftime("%d%m%Y"))

    picture_file_path = (os.getcwd() + "\\" + 'angry_duck.png')
    driver.find_element_by_css_selector("input[name='new_images[]']").send_keys(picture_file_path)

    # Работаем с вкладкой Information
    driver.find_element_by_xpath("//a[.='Information']").click()

    manufacturer = Select(driver.find_element_by_name('manufacturer_id'))
    manufacturer.select_by_visible_text("ACME Corp.")

    driver.find_element_by_xpath("//input[@name='keywords']").send_keys('angry duck')
    driver.find_element_by_xpath("//input[@name='short_description[en]']").send_keys('Yellow Angry Duck')

    description = driver.find_element_by_xpath("//div[@class='trumbowyg-editor']")
    description.click()
    description.send_keys('Very big and ugly angry duck.')

    driver.find_element_by_xpath("//input[@name='meta_description[en]']").send_keys('angry ugly bitchy stinky duck')

    # Работаем с вкладкой Prices
    driver.find_element_by_xpath("//a[.='Prices']").click()

    purchase_price = driver.find_element_by_xpath("//input[@name='purchase_price']")
    purchase_price.clear()
    purchase_price.send_keys('1')

    currenry = Select(driver.find_element_by_name('purchase_price_currency_code'))
    currenry.select_by_visible_text("US Dollars")

    # Цена без налога заполняется автоматически на основе цены с налогом
    #prices_usd = driver.find_element_by_xpath("//input[@name='prices[USD]']")
    #prices_usd.clear()
    #prices_usd.send_keys('13.00')

    gross_prices_usd = driver.find_element_by_xpath("//input[@name='gross_prices[USD]']")
    gross_prices_usd.clear()
    gross_prices_usd.send_keys('13.00')

    driver.find_element_by_css_selector("button[name=save]").click()

    search_form = driver.find_element_by_css_selector("form[name=search_form] input[name='query']")
    search_form.send_keys(code + Keys.ENTER)
    if driver.find_element_by_xpath("//td[contains(.,'Products:')]").text != 'Products: 1':
        raise Exception("Ошибка добавления продукта!")