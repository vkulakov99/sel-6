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


def test_countries_order(driver):
    driver.implicitly_wait(10)
    #driver.get("http://localhost/litecart/admin/login.php")


    driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_css_selector('button[name="login"]').click()

    # ждем появления кнопок после всех стран. Для гарантии, что все страны загрузились
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-group")))

    # находим все страны
    countries = driver.find_elements_by_css_selector("table.table a:not([title=Edit])")
    number_of_countries = len(countries)

    # печатать будем с новой строки
    print()

    # для каждой страны
    for i in range(0, number_of_countries-1):
        country = re.sub('Å', 'A', countries[i].text)
        # печатаем порядковый номер, исходное название страны и название с учетом эквивалентности 'Å' и 'A'
        print (str(i+1) + ' ' + countries[i].text + '->' + country)
        next_country = re.sub('Å', 'A', countries[i+1].text)

        if country > next_country:
            raise Exception("Страны стоят не по порядку")
        if country == next_country:
            raise Exception("Две одинаковых страны подряд")

    # печатаем порядковый номер и название последней страны
    country = re.sub('Å', 'A', countries[number_of_countries-1].text)
    print (str(number_of_countries) + ' ' + countries[number_of_countries-1].text + '->' + country)




