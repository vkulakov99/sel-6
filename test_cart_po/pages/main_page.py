from selenium.webdriver.support.wait import WebDriverWait

class MainPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart")
        return self

    def cart_quantity(self):
        return int(self.driver.find_element_by_css_selector("#cart .quantity").get_attribute("textContent"))

    def get_products(self):
        return self.driver.find_elements_by_css_selector("a.link")

