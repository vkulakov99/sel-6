import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re


@pytest.fixture
def driver(request):
    #wd = webdriver.Chrome()
    #wd = webdriver.Firefox()
    wd = webdriver.Edge()
    request.addfinalizer(wd.quit)
    return wd


def test_campaign_products(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/en/')

    # ждем загрузки конца страницы. Для гарантии, что все продукты во вкладке загрузились
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".bottom")))

    # находим все продукты во вкладке
    products = driver.find_elements_by_css_selector("#box-campaigns div.product")
    product_hrefs = []
    product_names = []
    product_regular_prices = []
    product_regular_price_font_sizes = []
    product_regular_price_font_weights = []
    product_regular_price_colors = []
    product_regular_price_decorations = []
    product_campaign_prices = []
    product_campaign_price_font_sizes = []
    product_campaign_price_font_weights = []
    product_campaign_price_colors = []
    product_campaign_price_decorations = []

    i = 0
    print() # Будем печатать с новой строки
    for product in products:
        product_hrefs.append(product.find_element_by_css_selector("a.link").get_attribute("href"))
        product_names.append(product.find_element_by_css_selector("div.name").get_attribute("textContent"))

        product_regular_prices.append(product.find_element_by_css_selector(".regular-price").get_attribute("textContent"))
        product_regular_price_font_sizes.append(product.find_element_by_css_selector(".regular-price").value_of_css_property("font-size"))
        #print(product.find_element_by_css_selector(".regular-price").value_of_css_property("font-size"))
        m = re.search('(\d|\.)+', product_regular_price_font_sizes[i])
        product_regular_price_font_sizes[i] = float(m.group(0))
        product_regular_price_font_weights.append(product.find_element_by_css_selector(".regular-price").value_of_css_property("font-weight"))

        product_regular_price_colors.append(product.find_element_by_css_selector(".regular-price").value_of_css_property("color"))
        #print(product.find_element_by_css_selector(".regular-price").value_of_css_property("color"))
        m = re.search('(\d+), (\d+), (\d+)', product_regular_price_colors[i])
        if m.group(1) != m.group(2) or m.group(2) != m.group(3) :
            raise Exception ("Обычная цена на главной странице не серая!")

        product_regular_price_decorations.append(product.find_element_by_css_selector(".regular-price").value_of_css_property("text-decoration"))
        #print(product.find_element_by_css_selector(".regular-price").value_of_css_property("text-decoration"))
        m = re.search('(\w+-\w+)', product_regular_price_decorations[i])
        if  m.group(1) != 'line-through':
            raise Exception ("Обычная цена на главной странице не зачеркнута!")

        product_campaign_prices.append(product.find_element_by_css_selector(".campaign-price").get_attribute("textContent"))
        product_campaign_price_font_sizes.append(product.find_element_by_css_selector(".campaign-price").value_of_css_property("font-size"))
        #print(product.find_element_by_css_selector(".campaign-price").value_of_css_property("font-size"))
        m = re.search('(\d|\.)+', product_campaign_price_font_sizes[i])
        product_campaign_price_font_sizes[i] = float(m.group(0))
        if product_campaign_price_font_sizes[i] <= product_regular_price_font_sizes[i]:
            raise Exception ("Акционная цена написана не крупнее обычной!")

        product_campaign_price_font_weights.append(product.find_element_by_css_selector(".campaign-price").value_of_css_property("font-weight"))
        #print(product.find_element_by_css_selector(".campaign-price").value_of_css_property("font-weight"))
        # Chrome показывает жирность как bold, а Firefox и Edge как 700
        if product_campaign_price_font_weights[i] != 'bold' and product_campaign_price_font_weights[i] != '700' :
            raise Exception ("Акционная цена на главной странице не жирная!")

        product_campaign_price_colors.append(product.find_element_by_css_selector(".campaign-price").value_of_css_property("color"))
        m = re.search('(\d+), (\d+), (\d+)', product_campaign_price_colors[i])
        if int(m.group(2)) != 0 or int(m.group(3)) != 0 :
            raise Exception ("Акционная цена на главной странице не красная!")
        product_campaign_price_decorations.append(product.find_element_by_css_selector(".campaign-price").value_of_css_property("text-decoration"))

        i += 1

    # Теперь проверяем все параметры на странице самого товара

    i = 0
    for product_href in product_hrefs:
        print (product_names[i])
        driver.get(product_href)

        title = driver.find_element_by_css_selector("h1").get_attribute("textContent")
        if title != product_names[i]:
            raise Exception ("Названия товара на главной странице и на карточке не совпадают!")

        regular_price = driver.find_element_by_css_selector("del.regular-price").get_attribute("textContent")
        regular_price_decoration = driver.find_element_by_css_selector("del.regular-price").value_of_css_property("text-decoration")
        m = re.search('(\w+-\w+)', regular_price_decoration)
        if  m.group(1) != 'line-through':
            raise Exception ("Обычная цена на странице продукта не зачеркнута!")

        regular_price_font_size = driver.find_element_by_css_selector("del.regular-price").value_of_css_property("font-size")
        m = re.search('(\d|\.)+', regular_price_font_size)
        regular_price_font_size = float(m.group(0))

        regular_price_color = driver.find_element_by_css_selector("del.regular-price").value_of_css_property("color")
        m = re.search('(\d+), (\d+), (\d+)', regular_price_color)
        if m.group(1) != m.group(2) or m.group(2) != m.group(3) :
            raise Exception ("Обычная цена на странице продукта не серая!")

        if regular_price != product_regular_prices[i] :
            raise Exception ("Обычная цена товара на главной странице и на карточке не совпадает!")

        campaign_price = driver.find_element_by_css_selector("div.well strong").get_attribute("textContent")
        if campaign_price != product_campaign_prices[i] :
            raise Exception ("Акционная цена товара на главной странице и на карточке не совпадает!")

        campaign_price_font_size = driver.find_element_by_css_selector("div.well strong").value_of_css_property("font-size")
        m = re.search('(\d|\.)+', campaign_price_font_size)
        campaign_price_font_size = float(m.group(0))
        if campaign_price_font_size <= regular_price_font_size:
            raise Exception ("Акционная цена на странице продукта написана не крупнее обычной!")

        campaign_price_font_weight = driver.find_element_by_css_selector("div.well strong").value_of_css_property("font-weight")
        # Chrome показывает жирность как bold, а Firefox и Edge как 700
        if campaign_price_font_weight != 'bold' and campaign_price_font_weight != '700' :
            raise Exception ("Акционная цена на главной странице не жирная!")
        campaign_price_color = driver.find_element_by_css_selector("div.well strong").value_of_css_property("color")
        m = re.search('(\d+), (\d+), (\d+)', campaign_price_color)
        if int(m.group(2)) != 0 or int(m.group(3)) != 0 :
            raise Exception ("Акционная цена на главной странице не красная!")




