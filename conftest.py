import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from pages.login_page import LoginPage


@pytest.fixture(scope="class")
def setup(request):
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )
    request.cls.driver = driver
    try:
        yield driver
    finally:
        print("Shutting down the WebDriver...")
        driver.quit()
        print("WebDriver shut down successfully.")

@pytest.fixture(scope="class")
def login(request):
    login_page = LoginPage(request.cls.driver)
    login_page.load()
