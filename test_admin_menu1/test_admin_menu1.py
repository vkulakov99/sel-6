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


def test_admin_menu1(driver):
    driver.implicitly_wait(10)
    driver.get("http://localhost/litecart/admin/login.php")
    driver.find_element_by_name("username").send_keys("admin")
    driver.find_element_by_name("password").send_keys("admin")
    driver.find_element_by_css_selector('button[name="login"]').click()
    WebDriverWait(driver, 10).until(EC.title_is("My Store"))


    number_of_menu_items = len(driver.find_elements_by_css_selector("li#app-")) # находим количество пунктов меню

    print() # начинаем печатать названия пунктов меню и подменю с новой строки
    for i in range(0,number_of_menu_items):
        menu_li_items = driver.find_elements_by_css_selector("li#app-")
        menu_li_item = menu_li_items[i]
        print(menu_li_item.text) # выводим название очередного пункта меню
        menu_li_item.click() # открываем очередной пункт меню

        wait = WebDriverWait(driver, 10) # seconds
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))) # ждем пока появится заголовок h1

        menu_li_items = driver.find_elements_by_css_selector("li#app-") #после клика menu_li_item уже протух, поэтому находим его снова
        menu_li_item = menu_li_items[i]

        number_of_submenu_items = len(menu_li_item.find_elements_by_css_selector("ul.docs .name")) #ищем количество пунктов подменю
        # print (number_of_submenu_items)
        for j in range(0,number_of_submenu_items):
            menu_li_items = driver.find_elements_by_css_selector("li#app-")
            menu_li_item = menu_li_items[i]
            submenu_items = menu_li_item.find_elements_by_css_selector("ul.docs .name") #ищем все подменю
            submenu_item = submenu_items[j]
            print("    " + submenu_item.text)  # выводим название очередного пункта подменю
            submenu_item.click()
            wait = WebDriverWait(driver, 10) # seconds
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h1")))
