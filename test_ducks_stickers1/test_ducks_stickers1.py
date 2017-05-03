import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_ducks_stickers1(driver):
    driver.implicitly_wait(10)
    driver.get("http://localhost/litecart/")

    # находим все товары
    images = driver.find_elements_by_css_selector("div.image-wrapper")

    # печать будем с новой строки
    print()

    # для каждого товара
    for image in (images):
        # находим сколько у товара стикеров
        stickers = image.find_elements_by_css_selector(".sticker")
        # image_name = image.find_element_by_css_selector("img").get_attribute("alt")
        # print (image_name, len(stickers))
        if len(stickers) != 1:
            raise Exception("Количество стикеров у товара не равно одному!")




