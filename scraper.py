from ast import main
from cgitb import text
from os import link
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from urllib.request import BaseHandler

class navigator():
    def __init__(self,URL) -> None:
        self.URL = URL
        
        # not to close window once the method is running
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chr_options)

        self.path = self.driver.get(self.URL)
        self.delay = 5
        
        time.sleep(1)

     
    def accept_cookies(self):
        
        try:
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@data-test="allow-all"]')))
            accept_cookies_button.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

        return self.driver 

    def scroll(self):
        
        self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        time.sleep(1)
        return self.driver
    
    def search(self):
        self.accept_cookies()
        try: 
            search_bar= WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@name="search-term"]')))
            search_bar.send_keys("ladies shoes")
            time.sleep(1)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

        return self.driver

    def go_to_next_page(self):
        try: 
            next= WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="js-plp-body"]/div[2]/nav/ul/li[2]/a/img')))
            next[0].click()
        
        except TimeoutException:
            print("Loading took too much time!")
        
        return self.driver
    
    def find_all_links(self):

        links = self.driver.find_elements(by=By.XPATH, value='//a[@href]')
        link_list=[]
        for link in links:
            link_list.append(link)
        return link_list
    
    def extract_src(self):
        self.search()
        src=self.driver.find_element(by=By.XPATH, value='//img[@class="logo-logo--5b465"]')
        print(src.get_attribute('src'))
        print (src.text)
           

if __name__ =='__main__':
    url = 'https://www.johnlewis.com'
    navigator(url).extract_src()

    


