from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import unittest


class NetflixCloneTest(unittest.TestCase):

    @classmethod
    def setUp(self):
        s = Service("D:/chromedriver.exe" )
        self.driver = webdriver.Chrome(service= s)
        self.driver.get("http://localhost:3000/login")
        self.driver.maximize_window()

    def test_case_1(self):
        #1.2 , 1.3, 1.5, 1.6, 1.8, 1.9, 1.10
        try:
            uname_field = self.driver.find_element( By.ID, "email-or-phone-number")
            self.driver.find_element(By.XPATH, "//label[contains(text(), 'Email or phone number')]")

            pw_field = self.driver.find_element( By.ID, "password")
            self.driver.find_element(By.XPATH, "//label[contains(text(), 'Password')]")

            sign_in_btn = self.driver.find_element(By. XPATH, "//button[contains(text(), 'Sign In')]")

            remember_me = self.driver.find_element( By.NAME, "remember_me")

            need_help = self.driver.find_element( By.XPATH, "//*[contains(text(), 'Need help?')]")

        except NoSuchElementException:
            print("Missing UI component.(Check username/password fields, sign in button ,remember me checkbox or need help link )")
            assert False

    def test_case_2_1(self):
        #2.2
        uname_field = self.driver.find_element(By.ID, "email-or-phone-number")
        #2.3
        uname_field.send_keys( "ogulcan@bilkent.edu.tr")
        #2.4
        pw_field = self.driver.find_element( By.ID, "password")
        #2.5
        pw_field.send_keys("secret3")
        #2.6
        sgnin_btn = self.driver.find_element( By. XPATH, "//button[contains(text(), 'Sign In')]")
        sgnin_btn.click()

        #2.7
        try:
            lgn_msg = self.driver.find_element(By.XPATH, "//div[@id='notistack-snackbar' and contains(text(), 'Login succeeded.')]")
            self.assertEqual("Login succeeded.", lgn_msg.text, "Login failed with correct credentials")
        except NoSuchElementException:
            print("Login is not successful")

    def test_case_2_2(self):
        self.driver.find_element(By.ID, "email-or-phone-number").send_keys("invalid@username")

        self.driver.find_element(By.ID, "password").send_keys("verifythis")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        lgn_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                       "//div[@id='notistack-snackbar' and contains(text(), 'Please check you credentials.')]")))
        self.assertEqual("Please check you credentials.", lgn_msg.text, "Login successful with invalid credentials")

    def test_case_2_3(self):
        self.driver.find_element(By.ID, "email-or-phone-number").send_keys("ogulcan@bilkent.edu.tr")

        self.driver.find_element(By.ID, "password").send_keys("invalidpassword")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        lgn_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                       "//div[@id='notistack-snackbar' and contains(text(), 'Please check you credentials.')]")))
        self.assertEqual("Please check you credentials.",  lgn_msg.text, "Login successful with invalid credentials")

    def test_case_2_4(self):
        self.driver.find_element(By.ID, "email-or-phone-number").send_keys("invalid@username")

        self.driver.find_element(By.ID, "password").send_keys("invalidpassword")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        lgn_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                       "//div[@id='notistack-snackbar' and contains(text(), 'Please check you credentials.')]")))
        self.assertEqual("Please check you credentials.", lgn_msg.text, "Login successful with invalid credentials")

    def test_case_2_5(self):
        self.driver.find_element(By.ID, "email-or-phone-number").send_keys("invalid@username")

        self.driver.find_element(By.ID, "password").send_keys("invalidpassword")
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Sign In')]").click()

        lgn_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                       "//div[@id='notistack-snackbar' and contains(text(), 'Please check you credentials.')]")))
        self.assertEqual("Please check you credentials.", lgn_msg.text, "Login successful with invalid credentials")

    def test_case_3(self):
        #3.2 , 3.3
        pw_field = self.driver.find_element(By.ID, "password")
        pw_field.click()

        pw_field.send_keys("verifythis")
        #3.4
        pw_field.send_keys(Keys.CONTROL + "a")
        pw_field.send_keys(Keys.CONTROL + "c")

        uname_field = self.driver.find_element(By.ID, "email-or-phone-number")
        uname_field.click()

        uname_field.send_keys(Keys.CONTROL + "v")
        self.assertNotEqual( uname_field.text, "verifythis", "Password can be copied")

    def test_case_4(self):
        login_fb = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Login with Facebook')]")
        login_fb.click()
        self.driver.implicitly_wait(5)
        orig_wd = self.driver.current_window_handle

        WebDriverWait(self.driver, 5).until(EC.number_of_windows_to_be(2))

        for wd_handle in self.driver.window_handles:
            if wd_handle != orig_wd:
                self.driver.switch_to.window( wd_handle)
                break

        self.driver.find_element(By.ID, "email").send_keys("cojep66578@naluzotan.com")
        self.driver.find_element(By.ID, "pass").send_keys("123123*")
        self.driver.find_element(By.ID, "loginbutton").click()
        self.driver.switch_to.window(orig_wd)
        lgn_msg = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                       "//div[@id='notistack-snackbar' and contains(text(), 'Facebook login successful')]")))

    def test_case_5(self):
        self.driver.find_element(By.ID, "email-or-phone-number").send_keys("ogulcan@bilkent.edu.tr")

        self.driver.find_element(By.ID, "password").send_keys("secret3")

        self.driver.find_element(By.NAME, "remember_me").click()

        self.driver.find_element( By. XPATH, "//button[contains(text(), 'Sign In')]").click()

        self.driver.refresh()

        uname = self.driver.find_element(By.ID, "email-or-phone-number").get_attribute("value")

        pw = self.driver.find_element(By.ID, "password").get_attribute("value")

        self.assertEqual( uname, "ogulcan@bilkent.edu.tr", "Username saved")
        self.assertEqual( pw, "secret3", "Password saved")

    @classmethod
    def tearDown(self):
        self.driver.close()



