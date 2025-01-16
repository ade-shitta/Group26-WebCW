from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.contrib.auth import get_user_model
from .models import User
import time

class SignupTests(StaticLiveServerTestCase):
    """
    Selenium-based tests for user signup functionality, ensuring redirection to the home page.
    """
    @classmethod
    def setUp(cls):
        super().setUpClass()
        cls.driver = webdriver.Chrome()
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDown(cls):
        cls.driver.quit()
        super().tearDownClass()


    def test_signup(self):
        """
        Test user signup process and redirection to the home page.
        """
        # example base_url: "http://localhost:<Asigned Port Number>"
        base_url: str = self.live_server_url
        self.driver.get(f"{self.live_server_url}/signup/")  # Navigate to the signup page

        # Wait for the signup form to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "signup-form")))

        # Fill out the signup form
        self.driver.find_element(By.NAME, "username").send_keys("testuser1")
        self.driver.find_element(By.NAME, "email").send_keys("testuser1@example.com")
        self.driver.find_element(By.NAME, "date_of_birth").send_keys("02-06-2003")
        self.driver.find_element(By.NAME, "password1").send_keys("helloworld1234-")
        self.driver.find_element(By.NAME, "password2").send_keys("helloworld1234-")
        self.driver.find_element(By.NAME, "first_name").send_keys("Selenium")
        self.driver.find_element(By.NAME, "last_name").send_keys("Test")

        # Submit the signup form
        submit_button = self.driver.find_element(By.ID, "signup-submit")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "signup-submit")))
        self.driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(1)

        # Verify redirection to the home page
        self.assertEqual(self.live_server_url, base_url)


    def test_login(self):
        """
        Test user login process using assertEqual for URL validation.
        """
        # example base_url: "http://localhost:<Asigned Port Number>"
        username, password = self.create_login()

        base_url: str = self.live_server_url
        self.driver.get(f"{self.live_server_url}/login/")  # Navigate to the signup page
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))

        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)

        submit_button = self.driver.find_element(By.ID, "login-submit")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
        self.driver.execute_script("arguments[0].click();", submit_button)

        time.sleep(10)
        self.assertEqual(self.live_server_url, base_url)

    def create_login(self) -> tuple:
        user = User.objects.create_user(username='testuser')
        user.set_password('helloworld1234-')
        user.save()
        return ("testuser", 'helloworld1234-')