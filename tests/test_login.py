
import sys
sys.path.append('C:/Users/phili/selenium-exercise')
from pages.login import Login
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def test_login(driver):
    logging.info("Starting the test")
    login = Login(driver=driver)
    login.login_user()
    logging.info("logging attempted")

    # Adding a screenshot after successfully logging in
    driver.save_screenshot('../screenshots/passed/login_attempt.png')

    logging.info("Screenshot saved.")

    assert 'Products' in driver.page_source


# driver.quit()