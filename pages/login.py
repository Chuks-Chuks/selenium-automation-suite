
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from random import choice

class BaseUrl:
    def __init__(self):
        self._url = None

    def load(self, driver):
        return driver.get(self._url)
    

class Login(BaseUrl):
    def __init__(self, driver):
        super().__init__()
        self.driver = driver
        self._url = 'https://www.saucedemo.com/'
        self.load(driver=self.driver)
        self.wait = WebDriverWait(self.driver, 20)
        self.username_locator = (By.ID, 'user-name')
        self.password_locator = (By.ID, 'password')
        self.submit = (By.ID, 'login-button')
        self.eligible_usernames = (By.ID, 'login_credentials')
        self.password = (By.CLASS_NAME, 'login_password')

    def fetch_username(self):
        usernames_available = self.wait.until(EC.presence_of_element_located((self.eligible_usernames)))
        return choice(usernames_available.text.split(':')[1].split())

    def fetch_password(self):
        password = self.wait.until(EC.presence_of_element_located((self.password)))
        return password.text.split(':')[1].strip()

    def _send_text_to_box(self, box, text):
        box.clear()
        box.send_keys(text)
        box.send_keys(Keys.RETURN)

    def login_user(self):
        try:
            username_box = self.wait.until(EC.presence_of_element_located((self.username_locator)))
            password_box = self.wait.until(EC.presence_of_element_located((self.password_locator)))
            if username_box and password_box:
                self._send_text_to_box(username_box, self.fetch_username())
                self._send_text_to_box(password_box, self.fetch_password())
                submit = self.wait.until(EC.element_to_be_clickable((self.submit)))
                self.driver.execute_script("arguments[0].click();", submit)
        except NoSuchElementException:
            pass


