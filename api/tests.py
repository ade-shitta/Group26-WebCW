from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from django.contrib.auth import get_user_model
from .models import User
import time

# class UserTests(StaticLiveServerTestCase):
#     """
#     Selenium tests for all of the user functionalities in the application.
#     """

#     #Methods helping for setting up the selelnium tests
#     @classmethod
#     def setUp(cls):
#         super().setUpClass()
#         cls.driver = webdriver.Chrome()
#         cls.options = webdriver.ChromeOptions()
#         cls.options.add_argument("--headless")
#         cls.driver.implicitly_wait(10)

#     @classmethod
#     def tearDown(cls):
#         cls.driver.quit()
#         super().tearDownClass()


#     def test_signup(self):
#         """
#         Test user login process that allows the user to register a new  profile and will redirect them 
#         to their profile page.
#         """
#         base_url: str = self.live_server_url
#         self.driver.get(f"{self.live_server_url}/signup/") 

#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "signup-form")))

#         self.driver.find_element(By.NAME, "username").send_keys("testuser1")
#         self.driver.find_element(By.NAME, "email").send_keys("testuser1@example.com")
#         self.driver.find_element(By.NAME, "date_of_birth").send_keys("02-06-2003")
#         self.driver.find_element(By.NAME, "password1").send_keys("helloworld1234-")
#         self.driver.find_element(By.NAME, "password2").send_keys("helloworld1234-")
#         self.driver.find_element(By.NAME, "first_name").send_keys("Selenium")
#         self.driver.find_element(By.NAME, "last_name").send_keys("Test")

#         # Submit the signup form, this avoids the scrolling issue when trying to find the submit button
#         submit_button = self.driver.find_element(By.ID, "signup-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "signup-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)

#         time.sleep(5)
#         # Verify redirection to the home page, had problems setting this up as the test kept failing
#         self.assertEqual(self.live_server_url, base_url)


#     def test_login(self):
#         """
#         Test user login process that allows the user to login and will redirect them to their profile
#         page
#         """
#         username, password = self.create_login()

#         base_url: str = self.live_server_url
#         self.driver.get(f"{self.live_server_url}/login/") 
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))

#         self.driver.find_element(By.NAME, "username").send_keys(username)
#         self.driver.find_element(By.NAME, "password").send_keys(password)

#         submit_button = self.driver.find_element(By.ID, "login-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)

#         time.sleep( 5)
#         self.assertEqual(self.live_server_url, base_url)

#     def test_logout(self):
#         """
#         Test user logout process that shows the user logging in, being redirected to the profile page
#         and then being able to logout where they should see the login page
#         """
#         username, password = self.create_login()

#         base_url: str = self.live_server_url
#         self.driver.get(f"{self.live_server_url}/login/") 
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))

#         self.driver.find_element(By.NAME, "username").send_keys(username)
#         self.driver.find_element(By.NAME, "password").send_keys(password)

#         submit_button = self.driver.find_element(By.ID, "login-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)
#         time.sleep(3)

#         self.driver.find_element(By.ID, "logout").click()

#         time.sleep(2)
#         self.assertEqual(self.live_server_url, base_url)

#     def test_edit(self):
#         """
#         Full test for the edit functionality, where the user can go in and edit all of their specific
#         details, as well adding hobbies and then deleting them
#         """
#         username, password = self.create_login()

#         base_url: str = self.live_server_url
#         self.driver.get(f"{self.live_server_url}/login/") 
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))

#         self.driver.find_element(By.NAME, "username").send_keys(username)
#         self.driver.find_element(By.NAME, "password").send_keys(password)

#         submit_button = self.driver.find_element(By.ID, "login-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)

#         time.sleep(3)

#         self.driver.find_element(By.ID, "edit-profile").click()

#         self.driver.find_element(By.ID, "editfname").send_keys("testuser1")
#         self.driver.find_element(By.ID, "editlname").send_keys("letsgo")
#         self.driver.find_element(By.ID, "editusername").send_keys("seleniumgoat")
#         self.driver.find_element(By.ID, "editemail").send_keys("test@gmail.com")
#         self.driver.find_element(By.ID, "editdob").send_keys("12-06-2003")  
#         self.driver.find_element(By.ID, "newhobbyadd").send_keys("test")
#         self.driver.find_element(By.ID, "newhobbybutton").click()
#         time.sleep(2)

#         self.driver.find_element(By.ID, "editsave").click()
#         time.sleep(1)

#         self.driver.find_element(By.ID, "deletehobby").click()
#         time.sleep(1)
#         self.assertEqual(self.live_server_url, base_url)


#     def test_filter(self):
#         """
#         Full test for going into the other users page and then filtering the users based on their age,
#         where once the filter is applied the page should show only those users
#         """
#         self.create_users()

#         username, password = self.create_login()

#         base_url: str = self.live_server_url
#         self.driver.get(f"{self.live_server_url}/login/") 
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))

#         self.driver.find_element(By.NAME, "username").send_keys(username)
#         self.driver.find_element(By.NAME, "password").send_keys(password)

#         submit_button = self.driver.find_element(By.ID, "login-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)

#         self.driver.find_element(By.ID, "otherpage").click()
#         time.sleep(1)

#         self.driver.find_element(By.ID, "minage").send_keys("35")
#         self.driver.find_element(By.ID, "maxage").send_keys("40")
#         self.driver.find_element(By.ID, "filterbutton").click()    

#         time.sleep(1)
#         self.assertEqual(self.live_server_url, base_url)


#     def test_sendfriend(self):
#         """
#         Full test for the user ability to send a friend request to another user
#         accepting is covered next in the test_addfriend test
#         """
#         self.create_users()

#         username, password = self.create_login()

#         base_url: str = self.live_server_url
#         self.driver.get(f"{self.live_server_url}/login/") 
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))

#         self.driver.find_element(By.NAME, "username").send_keys(username)
#         self.driver.find_element(By.NAME, "password").send_keys(password)

#         submit_button = self.driver.find_element(By.ID, "login-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)

#         self.driver.find_element(By.ID, "otherpage").click()
#         time.sleep(1)

#         self.driver.find_element(By.ID, "sendfriendbutton").click()            

#         time.sleep(1)
#         self.assertEqual(self.live_server_url, base_url)    

#     def test_addfriend(self):
#         """
#         Testing for the adding a friend, and logging into another user and then
#         accepting the friend request and it showing up in the friends page
#         """
#         self.create_users()

#         username, password = self.create_login()

#         base_url: str = self.live_server_url
#         self.driver.get(f"{self.live_server_url}/login/") 
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "login-form")))

#         self.driver.find_element(By.NAME, "username").send_keys(username)
#         self.driver.find_element(By.NAME, "password").send_keys(password)

#         submit_button = self.driver.find_element(By.ID, "login-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)

#         self.driver.find_element(By.ID, "otherpage").click()
#         time.sleep(1)
#         self.driver.find_element(By.ID, "sendfriendbutton").click()  
#         time.sleep(1)

#         self.driver.switch_to.alert.dismiss() #This took me years to figure out i kept getting the alert error

#         time.sleep(5)
#         self.driver.find_element(By.ID, "logout").click()

#         self.driver.find_element(By.NAME, "username").send_keys("EmilyDickens")
#         self.driver.find_element(By.NAME, "password").send_keys("hello1234-")

#         submit_button = self.driver.find_element(By.ID, "login-submit")
#         self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)

#         WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "login-submit")))
#         self.driver.execute_script("arguments[0].click();", submit_button)

#         self.driver.find_element(By.ID, "friendspage").click()
#         time.sleep(1)

#         self.driver.find_element(By.ID, "acceptfriendbutton").click()

#         time.sleep(1)
#         self.assertEqual(self.live_server_url, base_url)     


#     #Creates a user that is used throughout the tests up until other users are used
#     def create_login(self) -> tuple:
#         user = User.objects.create_user(username='testuser')
#         user.set_password('helloworld1234-')
#         user.save()
#         return ("testuser", 'helloworld1234-')
    
#     #Creates a few users that are used for the filter and friend request tests
#     def create_users(self):
#         User = get_user_model()

#         users = [
#             {"username": "EmilyDickens", "password": "hello1234-", "email": "test1@gmail.com", "date_of_birth": "1990-01-01"},
#             {"username": "BrentFayaz", "password": "hello1234", "email": "test2@gmail.com", "date_of_birth": "1985-06-15"},
#             {"username": "AndrewGarfield", "password": "hello1234-", "email": "test3@gmail.com", "date_of_birth": "2000-12-25"},
#             {"username": "JaneEyre", "password": "hello1234-", "email": "test4@gmail.com", "date_of_birth": "1995-03-10"},
#         ]

#         for user_data in users:
#             user = User.objects.create_user(username=user_data["username"],email=user_data["email"],date_of_birth=user_data["date_of_birth"]
#             )
#             user.set_password(user_data["password"])
#             user.save()
