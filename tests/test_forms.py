import sys
sys.path.append('C:/Users/phili/selenium-exercise')
from pages.forms import Forms
from .base_test import BaseTest


class TestForms:

    def test_forms(self, driver):
        forms = Forms(driver=driver)
        forms.fill_form_texts()
        forms.fill_form_gender_clicks()
        forms.click_dob()
        assert isinstance(forms.click_dob(), str)
        forms.fill_form_hobbies_click()
        forms.click_state_city()
        driver.save_screenshot('../screenshots/passed/login_attempt.png')
        forms.click_submit()

