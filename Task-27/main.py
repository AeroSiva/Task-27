from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import datetime
from locators import OrangeHRM_Locators,Zen_locators
from data import OrangeHrm_Data,Zen_Data
from excel_functions import Excel_Functions
from time import sleep

class Login:
    def __init__(self):
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
        self.wait = WebDriverWait(self.driver, 20)
        self.excel_func = Excel_Functions(OrangeHrm_Data().excel_file_name, OrangeHrm_Data().excel_sheet_name)
        self.row = self.excel_func.row_count()
        self.action = ActionChains(self.driver)
        self.date = datetime.datetime.now()

    def access_url(self):
        try:
            self.driver.maximize_window()
            self.driver.get(Zen_Data().url)
        except Exception as e:
             print("Selenium Exception : ",e)
    
    def login_logout_test(self):
        try: 
            for row in range(2, self.row+1):
                username = self.excel_func.read_data(row, 7)
                password = self.excel_func.read_data(row, 8)
                date = self.date.strftime("%x")
                self.excel_func.write_data(row, 4, date)
                time = self.date.strftime("%X")
                self.excel_func.write_data(row,5,time)

                user_box = self.wait.until(EC.visibility_of_element_located((By.NAME,Zen_locators.username_ip_box_name)))
                user_box.clear()
                user_box.send_keys(username)
                password_box = self.wait.until(EC.visibility_of_element_located((By.NAME,Zen_locators.password_pw_box_name)))
                password_box.send_keys(password)
                self.wait.until(EC.visibility_of_element_located((By.XPATH,Zen_locators.login_button_Xpath))).click()
                sleep(5)

                # test PASS or FAIL
                if (Zen_Data().url != self.driver.current_url):
                    print("SUCCESS : Login success with \n username :{a} and password {b}".format(a=username, b=password))
                    self.excel_func.write_data(row, 9, "TEST PASS")
                    print("Test passed written in Excel")

                    drop_down = self.wait.until(EC.element_to_be_clickable((By.XPATH, Zen_locators().drop_down_on_click_Xpath)))
                    self.action.click(on_element=drop_down).perform()
                    self.wait.until(EC.visibility_of_element_located((By.XPATH,Zen_locators().logout_button_Xpath))).click()

                elif(Zen_Data().url in self.driver.current_url):
                    print("FAIL : Login failure with \n username :{a} and password {b}".format(a=username, b=password))
                    self.excel_func.write_data(row, 9, "TEST FAIL")
                    self.driver.refresh()

        except Exception as selenium_error:
            print("Selenium Error in Login/ Logout test: ",selenium_error)

'''finally:
    driver.quit()'''

'''orange = Login()
orange.access_url()
orange.login_logout_test()'''
