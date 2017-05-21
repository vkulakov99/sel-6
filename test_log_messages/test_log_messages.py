import pytest
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


@pytest.fixture
def driver(request):
    # Если нужен более детальный уровень логирования:
    #d = DesiredCapabilities.CHROME
    #d['loggingPrefs'] = { 'performance':'ALL' }
    # или
    #d['loggingPrefs'] = { 'browser':'ALL' }
    #wd = webdriver.Chrome(desired_capabilities=d)

    # Если нужен стандартный уровень логирования:
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_log_messages(driver):
    driver.implicitly_wait(10)
    driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_name("password").send_keys(Keys.ENTER)

    # Ищем все ссылки на товары
    links = driver.find_elements_by_css_selector("img + a")

    number_of_links = len(links)

    # для каждой ссылки
    for i in range(0,number_of_links):
        driver.get("http://localhost/litecart/admin/?app=catalog&doc=catalog&category_id=1")
        # Ссылки на товары протухли, поэтому ищем их ещё раз
        links = driver.find_elements_by_css_selector("img + a")
        links[i].click()

        # ждем пока страница загрузится и появится нижний элемент
        WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".btn-group")))

        for message in driver.get_log("browser"):
            print(message)
            raise Exception("Сообщение в логе браузера!")

