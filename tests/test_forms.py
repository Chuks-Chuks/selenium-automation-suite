import sys
sys.path.append('C:/Users/phili/selenium-exercise')
from pages.forms import Forms

def test_forms(driver):
    forms = Forms(driver=driver)
    forms.fill_form_texts()
    forms.fill_form_gender_clicks()
    forms.click_dob()
    assert isinstance(forms.click_dob(), str)
    forms.fill_form_hobbies_click()
    forms.click_state_city()
    forms.click_submit()

