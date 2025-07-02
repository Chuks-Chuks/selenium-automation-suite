import sys
sys.path.append('C:/Users/phili/selenium-exercise')
from pages.login import Login
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from faker import Faker
import requests
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random


class GenerateNameAndGender:
    def __init__(self):
        self.gender_endpoint = 'https://api.genderize.io'
        self.fake = Faker()

    def generate_details(self):
        first_name = self.fake.first_name()
        last_name = self.fake.last_name()
        email = self.fake.email()
        dob = self.fake.date_of_birth(minimum_age=18, maximum_age=78)
        mobile_number = self.fake.phone_number()
        address = self.fake.address()
        return {'first_name': first_name, 'last_name': last_name, 'email': email, 'dob': dob, 'mobile': mobile_number, 'address': address}

    def generate_gender(self, first_name):
        params = {'name': first_name}
        fetch_endpoint = requests.get(self.gender_endpoint, params=params)
        return fetch_endpoint.json()['gender']

class Forms(Login):
    def __init__(self, driver):
        super().__init__(driver)
        self.gender_generator = GenerateNameAndGender()
        self.person_details = self.gender_generator.generate_details()
        self.driver = driver
        self._url = 'https://demoqa.com/automation-practice-form'
        self.load(self.driver) 
        self.wait = WebDriverWait(driver=self.driver, timeout=25)
        self.close_add = (By.CLASS_NAME, 'continue-prompt-text')
        self.first_name_locator = (By.ID, 'firstName')
        self.last_name_locator = (By.ID, 'lastName')
        self.email_locator = (By.ID, 'userEmail')
        self.male_gender = (By.ID, 'gender-radio-1')
        self.female_gender = (By.ID, 'gender-radio-2')
        self.other_gender = (By.ID, 'gender-radio-3')
        self.mobile_number_locator = (By.ID, 'userNumber')
        self.date_of_birth_locator = (By.ID, 'dateOfBirthInput')
        self.date_of_birth_locator_month = (By.CLASS_NAME, 'react-datepicker__month-select')  # if month in month select month
        self.date_of_birth_locator_year = (By.CLASS_NAME, 'react-datepicker__year-select')
        self.subject_locator = (By.ID, 'subjectsInput')
        self.hobbies_choice = random.choice(['Sports', 'Reading', 'Music']) # random.choice
        self.hobbies_one = (By.ID, 'hobbies-checkbox-1')
        self.hobbies_two = (By.ID, 'hobbies-checkbox-2')
        self.hobbies_three = (By.ID, 'hobbies-checkbox-3')
        self.current_address = (By.ID, 'currentAddress')
        self.select_state_locator = (By.ID, 'state')
        self.select_city_locator = (By.ID, 'city')
        self.state_city_map = {
                                "NCR": ["Delhi", "Gurgaon", "Noida"],
                                "Rajasthan": ["Jaipur", "Jaiselmer"],
                                "Uttar Pradesh": ["Agra", "Lucknow", "Merrut"]
                            }
        self.submit_button_locator = (By.ID, 'submit')


    def fill_form_texts(self):
        try:
            
            first_name_box = self.wait.until(EC.presence_of_element_located((self.first_name_locator)))
            last_name_box = self.wait.until(EC.presence_of_element_located((self.last_name_locator)))
            email_box = self.wait.until(EC.presence_of_element_located((self.email_locator)))
            mobile_number_box = self.wait.until(EC.presence_of_element_located((self.mobile_number_locator)))
            address_box = self.wait.until(EC.presence_of_element_located((self.current_address)))
            self._send_text_to_box(first_name_box, self.person_details['first_name'])
            self._send_text_to_box(last_name_box, self.person_details['last_name'])
            self._send_text_to_box(email_box, self.person_details['email'])
            self._send_text_to_box(mobile_number_box, random.randint(1000000000, 1500000000))
            self._send_text_to_box(address_box, self.person_details['address'])


        except NoSuchElementException:
            pass
    

    def fill_form_gender_clicks(self):
        try:
            male_gender_box = self.wait.until(EC.presence_of_element_located((self.male_gender)))
            female_gender_box = self.wait.until(EC.presence_of_element_located((self.female_gender)))
            other_box = self.wait.until(EC.presence_of_element_located((self.other_gender)))
            gender = self.gender_generator.generate_gender(self.person_details['first_name']).title()
            if gender== 'Male':
                self.driver.execute_script("arguments[0].click();", male_gender_box)

            elif gender == 'Female':
                self.driver.execute_script("arguments[0].click();", female_gender_box)
            else:
                self.driver.execute_script("arguments[0].click();", other_box)
        except NoSuchElementException:
            pass

    
    def fill_form_hobbies_click(self):
        hobbies_one_box = self.wait.until(EC.presence_of_element_located((self.hobbies_one)))
        hobbies_two_box = self.wait.until(EC.presence_of_element_located((self.hobbies_two)))
        hobbies_three_box = self.wait.until(EC.presence_of_element_located((self.hobbies_three)))
        hobbies_select = self.hobbies_choice

        if hobbies_select == 'Sports':
            self.driver.execute_script("arguments[0].click();", hobbies_one_box)
        elif hobbies_select == 'Reading':
            self.driver.execute_script("arguments[0].click();", hobbies_two_box)
        else:
            self.driver.execute_script("arguments[0].click();", hobbies_three_box)

    def click_dob(self) -> str:
        date_box = self.wait.until(EC.presence_of_element_located((self.date_of_birth_locator)))
        dob_formatted = ''.join(self.person_details['dob'].strftime('%Y %B %d').split()[::-1])
        self.driver.execute_script("arguments[0].click();", date_box)  
        date_box.send_keys(Keys.CONTROL + 'a')
        date_box.send_keys(dob_formatted)
        date_box.send_keys(Keys.RETURN)
        return dob_formatted

    def click_state_city(self):  # Select text, select random, paste
        state = random.choice(list(self.state_city_map.keys()))
        city = random.choice(self.state_city_map[state])
        state_box = self.wait.until(EC.element_to_be_clickable((self.select_state_locator)))
        self.driver.execute_script("arguments[0].scrollIntoView();", state_box)
        state_box.click()

        # Wait for input inside the dropdown
        input_box = self.wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#state input'))
        )

        input_box.send_keys(state)  # or "Rajasthan", etc.
        input_box.send_keys(Keys.RETURN)

        city_box = self.wait.until(EC.element_to_be_clickable((self.select_city_locator)))
        city_box.click()

        city_input_box = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#city input')))
        city_input_box.send_keys(city)
        city_input_box.send_keys(Keys.RETURN)


    def click_submit(self):
        submit_box = self.wait.until(EC.element_to_be_clickable((self.submit_button_locator)))
        self.driver.execute_script("arguments[0].click();", submit_box)

    

# if __name__ == '__main__':
#     f = Forms()
#     f.click