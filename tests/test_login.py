from pages.login import Login
from .base_test import BaseTest
import pytest 



@pytest.mark.usefixtures('driver', 'logger')
class TestLogin(BaseTest):
    def test_login(self, logger, driver):
        logger.info("Starting the test")
        login = Login(driver=driver)
        login.login_user()
        logger.info("logging attempted")

        # # Adding a screenshot after successfully logging in
        # self.driver.save_screenshot('../screenshots/passed/login_attempt.png')

        logger.info("Screenshot saved.")

        assert 'Naira' in driver.page_source
