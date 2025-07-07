from pages.forms import Forms
from .base_test import BaseTest
import pytest

@pytest.mark.usefixtures('driver', 'logger')
class TestForms:
    
    def test_forms(self, driver, logger):
        forms = Forms(driver=driver)
        logger.info('Starting browser and filling out forms')
        forms.fill_form_texts()
        forms.fill_form_gender_clicks()
        forms.click_dob()
        logger.info('asserting dob text field is a string')
        assert isinstance(forms.click_dob(), str)
        forms.fill_form_hobbies_click()
        forms.click_state_city()
        logger.info('Finalising form and taking screenshot')
        driver.save_screenshot('../screenshots/passed/login_attempt.png')
        forms.click_submit()
        logger.info('Process completed.')
