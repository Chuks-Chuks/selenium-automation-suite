
import sys
sys.path.append('C:/Users/phili/selenium-exercise')
from pages.login import Login
    

def test_login(driver):
    login = Login(driver=driver)
    login.login_user()

    assert 'Products' in driver.page_source


# driver.quit()