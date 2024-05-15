from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    URL = "https://www.globalsqa.com/angularJs-protractor/BankingProject/#/login"

    def __init__(self, driver):
        self.driver = driver

    def load(self):
        self.driver.get(self.URL)

    def is_customer_login_button_visible(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//button[text()='Customer Login']")))

    def go_to_customer_login(self):
        wait = WebDriverWait(self.driver, 10)
        customer_login_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Customer Login']")))
        customer_login_button.click()

    def is_customer_select_visible(self):
        wait = WebDriverWait(self.driver, 10)
        return wait.until(
            EC.visibility_of_element_located((By.ID, "userSelect")))

    def select_customer(self, customer_name):
        wait = WebDriverWait(self.driver, 10)
        select_element = wait.until(
            EC.presence_of_element_located((By.ID, "userSelect")))
        select = Select(select_element)
        select.select_by_visible_text(customer_name)

    def click_login(self):
        wait = WebDriverWait(self.driver, 10)
        login_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[text()='Login' and @type='submit']")))
        login_button.click()
