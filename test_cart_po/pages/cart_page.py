from selenium.webdriver.support.wait import WebDriverWait

class CartPage:

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    def open(self):
        self.driver.get("http://localhost/litecart/en/checkout")
        return self

    @property
    def trash_button(self):
        return self.driver.find_element_by_css_selector("button[name='remove_cart_item'")

