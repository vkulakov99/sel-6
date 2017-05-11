import pytest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import datetime


@pytest.fixture
def driver(request):
    wd = webdriver.Chrome()
    request.addfinalizer(wd.quit)
    return wd


def test_create_account(driver):
    driver.implicitly_wait(10)
    driver.get('http://localhost/litecart/en/create_account')
    firstname = driver.find_element_by_css_selector("input[name=firstname]")
    firstname.click()
    firstname.send_keys("Ivan")
    lastname = driver.find_element_by_css_selector("input[name=lastname]")
    lastname.click()
    lastname.send_keys("Ivanov")
    address = driver.find_element_by_css_selector("input[name=address1]")
    address.click()
    address.send_keys("Selenium str.")
    postcode = driver.find_element_by_css_selector("input[name=postcode]")
    postcode.click()
    postcode.send_keys("12345")
    # страна USA, штат произвольный
    country = Select(driver.find_element_by_name('country_code'))
    country.select_by_visible_text("United States")
    email = driver.find_element_by_css_selector("main input[name=email]")
    email.click()
    # генерируем уникальный адрес по дате и времени
    now_time = datetime.datetime.now()
    new_email_address = now_time.strftime("Ivan%d%m%Y%I%M%S@gmail.com")
    print(new_email_address)
    email.send_keys(new_email_address)
    passwd = driver.find_element_by_css_selector("main input[name=password]")
    passwd.click()
    passwd.send_keys("123")
    confirmed_passwd = driver.find_element_by_css_selector("main input[name=confirmed_password]")
    confirmed_passwd.click()
    confirmed_passwd.send_keys("123" + Keys.ENTER)

    #time.sleep(5)
    logout = driver.find_element_by_css_selector("#box-account li:nth-child(3) a")
    logout.click()
    #time.sleep(5)
    registered_email = driver.find_element_by_css_selector("form[name=login_form] input[name=email")
    registered_email.click()
    registered_email.send_keys(new_email_address)
    registered_passwd = driver.find_element_by_css_selector("form[name=login_form] input[name=password]")
    registered_passwd.click()
    registered_passwd.send_keys("123" + Keys.ENTER)
    #time.sleep(5)
    logout = driver.find_element_by_css_selector("#box-account li:nth-child(3) a")
    logout.click()
    #time.sleep(5)

