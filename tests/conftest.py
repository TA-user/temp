import allure
import os
import pytest
from msedge.selenium_tools import Edge
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from config import MAIN_PAGE_URL
from tests.pages.main_page import MainPage, MainPageCarHireTab, MainPageSearchHotelsTab, MainPageSearchFlightsTab


def pytest_addoption(parser):
    parser.addoption("--browser_name", action="store", default="chrome",
                     help="Choose browser: chrome or firefox or edge")


@pytest.fixture(scope="package")
def browser(request):
    browser_name = request.config.getoption("browser_name")
    browser = None
    if browser_name == "chrome":
        browser = webdriver.Chrome(executable_path=ChromeDriverManager().install())
    elif browser_name == "firefox":
        browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    elif browser_name == "edge":
        desired_cap = {}
        browser = Edge(executable_path=EdgeChromiumDriverManager().install(), desired_capabilities=desired_cap)
    else:
        raise pytest.UsageError("--browser name should be chrome or firefox or edge")
    browser.maximize_window()
    yield browser
    browser.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        mode = 'a' if os.path.exists('failures') else 'w'
        try:
            with open('failures', mode) as f:
                if 'browser' in item.fixturenames:
                    web_driver = item.funcargs['browser']
                else:
                    print('Fail to take screen-shot')
                    return
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name='screenshot',
                attachment_type=allure.attachment_type.PNG
            )
        except Exception as e:
            print('Fail to take screen-shot: {}'.format(e))


@pytest.fixture(scope="module")
def main_page(browser):
    return MainPage(browser=browser, url=MAIN_PAGE_URL)


@pytest.fixture(scope="module")
def main_page_search_flights_tab(browser):
    return MainPageSearchFlightsTab(browser=browser, url=browser.current_url)


@pytest.fixture(scope="module")
def main_page_car_hire_tab(browser):
    return MainPageCarHireTab(browser=browser, url=browser.current_url)


@pytest.fixture(scope="module")
def main_page_search_hotels_tab(browser):
    return MainPageSearchHotelsTab(browser=browser, url=browser.current_url)
