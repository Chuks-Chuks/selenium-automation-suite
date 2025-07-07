import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as chromeservice
from selenium.webdriver.firefox.service import Service as firefoxservice
from selenium.webdriver.edge.service import Service as edgeservice
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from utils.logger import setup_logger


@pytest.fixture
def logger(request):
    test_name = request.node.name
    return setup_logger(test_name)


def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests: chrome or edge or headless"
    )


@pytest.fixture
def driver(request):
    browser = request.config.getoption('--browser')

    if browser == 'chrome':
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('detach', True)
        driver = webdriver.Chrome(service=chromeservice(ChromeDriverManager().install()), options=chrome_options)
        
    elif browser == 'edge':
        edge_options = EdgeOptions()
        edge_options.add_experimental_option('detach', True)
        driver = webdriver.Edge(service=edgeservice(EdgeChromiumDriverManager().install()), options=edge_options)
        
    elif browser == 'headless':
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(service=chromeservice(ChromeDriverManager().install()), options=options)

    else:
        raise ValueError(f'Browser type not supported {browser}')
    
    driver.maximize_window()
    request.node._driver = driver
    yield driver
    driver.quit()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()

    if result.when == 'call' and result.failed:
        driver = getattr(item, '_driver', None)
        if driver:
            os.makedirs('../screenshots/failed/', exist_ok=True)
            filename = f'../screenshots/failed/{item.name}.png'
            driver.save_screenshot(filename)