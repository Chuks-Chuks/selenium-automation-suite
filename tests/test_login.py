
import sys
sys.path.append('C:/Users/phili/selenium-exercise')
from pages.login import Login
from .base_test import BaseTest
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

class TestLogin(BaseTest):
    def test_login(self):
        logging.info("Starting the test")
        login = Login(driver=self.driver)
        login.login_user()
        logging.info("logging attempted")

        # Adding a screenshot after successfully logging in
        self.driver.save_screenshot('../screenshots/passed/login_attempt.png')

        logging.info("Screenshot saved.")

        assert 'Products' in self.driver.page_source


# driver.quit()