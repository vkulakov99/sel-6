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


def test_countries_and_zones_order(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/admin/?app=countries&doc=countries')
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_css_selector('button[name="login"]').click()

    # ждем появления кнопок после всех стран. Для гарантии, что все страны загрузились
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-group")))

    # находим таблицу
    table = driver.find_element_by_css_selector("table.table tbody")
    rows = table.find_elements_by_css_selector("tr")
    number_of_rows = len(rows)

    # печатать будем с новой строки
    print()

    # инициализируем список за пределами цикла for
    countries_links_with_zones = []

    # для каждой страны
    for i in range(0, number_of_rows-1):
        row = rows[i]
        next_row = rows[i+1]
        country_name = row.find_element_by_css_selector("a:not([title=Edit])").text
        modified_country_name = re.sub('Å', 'A', country_name)

        # узнаем сколько у данной страны зон
        number_of_zones = row.find_element_by_css_selector("td.text-center").text

        # печатаем порядковый номер, исходное название страны и название с учетом эквивалентности 'Å' и 'A'
        print (str(i+1) + ' ' + country_name + ' -> ' + modified_country_name + ' ' + str(number_of_zones))

        next_country_name = next_row.find_element_by_css_selector("a:not([title=Edit])").text
        modified_next_country_name = re.sub('Å', 'A', next_country_name)

        if number_of_zones != '0':
            href = row.find_element_by_css_selector("a:not([title=Edit])").get_attribute("href")
            print (href)
            countries_links_with_zones.append(href)
        if modified_country_name > modified_next_country_name:
            raise Exception("Страны стоят не по порядку")
        if modified_country_name == modified_next_country_name:
            raise Exception("Две одинаковых страны подряд")

    # печатаем порядковый номер и название последней страны
    row = rows[number_of_rows-1]  # элементы списка нумеруются с нуля. Номер последнего элемента на 1 меньше количества
    country_name = row.find_element_by_css_selector("a:not([title=Edit])").text
    modified_country_name = re.sub('Å', 'A', country_name)
    number_of_zones = row.find_element_by_css_selector("td.text-center").text
    print (str(number_of_rows) + ' ' + country_name + ' -> ' + modified_country_name + ' ' + str(number_of_zones))
    if number_of_zones != '0':
        href = row.find_element_by_css_selector("a:not([title=Edit])").get_attribute("href")
        print (href)
        countries_links_with_zones.append(href)

    # проверяем страны с ненулевым количеством зон
    print ()
    print("Страны с зонами")
    for country_link in countries_links_with_zones:
        print (country_link)
        driver.get(country_link)  # загружаем страницу с зонами каждой такой страны по сохраненным ранее ссылкам
        # ждем появления кнопки "Add zone" после списка зон. Для гарантии, что все зоны загрузились
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "a.add")))
        zones = driver.find_elements_by_css_selector("[name$='name]']")  # атрибут name должен оканчиваться на 'name]'
        for i in range(0, len(zones)-1):
            zone_name = zones[i].get_attribute("value")
            next_zone_name = zones[i+1].get_attribute("value")
            print (zone_name)  # Печатаем название зоны
            if zone_name > next_zone_name:
                raise Exception("Зоны стоят не по порядку")
            if zone_name == next_zone_name:
                raise Exception("Две одинаковых зоны подряд")
        zone_name = zones[len(zones)-1].get_attribute("value")
        print (zone_name)


