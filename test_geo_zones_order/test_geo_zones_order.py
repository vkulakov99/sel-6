import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_geo_zones_order(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/admin/?app=geo_zones&doc=geo_zones')
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_css_selector('button[name="login"]').click()

    # ждем появления кнопок после всех стран. Для гарантии, что все страны загрузились
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.table tfoot")))

    # находим все строки таблицы
    rows = driver.find_elements_by_css_selector("table.table tbody tr")

    # иницализируем список ссылок за пределами цикла for
    countries_links = []

    for row in rows:
        country_link = row.find_element_by_css_selector("a:not([title=Edit])")
        countries_links.append(country_link.get_attribute("href"))

    # печатать будем с новой строки
    print()

    # для каждой страны
    for country_link in countries_links:
        # Печатаем ссылку
        print (country_link)
        driver.get(country_link)  # загружаем страницу с зонами каждой такой страны по сохраненным ранее ссылкам
        # ждем появления кнопки "Add zone" после списка зон. Для гарантии, что все зоны загрузились
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.add")))

        zones = driver.find_elements_by_css_selector("table.table tbody tr td:nth-child(3)")  # 3-я колонка в таблице
        for i in range(0, len(zones)-1):
            zone_name = zones[i].get_attribute("textContent")
            next_zone_name = zones[i+1].get_attribute("textContent")
            print (zone_name)  # Печатаем название зоны
            if zone_name > next_zone_name:
                raise Exception("Зоны стоят не по порядку")
            if zone_name == next_zone_name:
                raise Exception("Две одинаковых зоны подряд")
        # Печатаем название последней зоны
        zone_name = zones[len(zones)-1].get_attribute("textContent")
        print (zone_name)


