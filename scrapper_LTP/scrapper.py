import scrapper_LTP.constants as const
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
import time


class Scrapper(webdriver.Chrome):
   
    def __init__(self, driver_path=r"C:\SeleniumDrivers", options=None):
        self.driver_path = driver_path
        os.environ['PATH'] += os.pathsep + self.driver_path
        if options is None:
            options = Options()
        service = Service(os.path.join(self.driver_path, "chromedriver.exe"))
        super(Scrapper, self).__init__(service=service,options=options)
    
    
    def load_login_page(self):
        self.get(const.LOGIN_URL)

    def login(self):
        input_element_id = self.find_element(By.CLASS_NAME,const.ID_SELECTOR)
        input_element_id.send_keys(const.ID)
        input_element_pass = self.find_element(By.CSS_SELECTOR,const.PASS_SELECTOR)
        input_element_pass.send_keys(const.PASS)
        input_element_tc = self.find_element(By.CSS_SELECTOR,const.TCSELECTOR)
        input_element_tc.click()
    
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH,"//span[text()='DashBoard']"))
                )
    
    def IdaddyBlast_page(self):
        self.get(const.IDADDYBLAST_URL)

        