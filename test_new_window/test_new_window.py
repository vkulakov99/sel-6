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


def test_new_window(driver):
    driver.implicitly_wait(10)
    driver.get("http://localhost/litecart/admin/?app=countries&doc=countries")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("password").send_keys(Keys.ENTER)

    # Нажимаем на редактирование первой попавшейся страны
    driver.find_element_by_css_selector("[title=Edit]").click()

    links = driver.find_elements_by_css_selector(".fa-external-link")
    number_of_links = len(links)

    # запоминаем хэндл главного окна
    main_window = driver.current_window_handle

    # для каждой ссылки
    for link in links:
        old_windows = set(driver.window_handles)
        link.click()
        WebDriverWait(driver,10).until(EC.new_window_is_opened(old_windows))
        # хэндл нового окна - разность между новым множеством хэндлов и старым
        new_windows = set(driver.window_handles) - old_windows
        # переключаемся на новое окно
        driver.switch_to_window(new_windows.pop())
        # закрываем новое окно
        driver.close()
        # снова переключаемся на главное окно
        driver.switch_to_window(main_window)
