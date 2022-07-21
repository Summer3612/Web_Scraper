from ast import main
from cgitb import text
from lib2to3.pgen2 import driver
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

class Scraper():

    def __init__(self,URL,items_to_seach) -> None:
        self.URL = URL
        self.items_to_search = items_to_seach
        
        # not to close window once the method is running
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chr_options)

        self.path = self.driver.get(self.URL)
        self.delay = 5
        self.if_next_page=True
        
        time.sleep(0.5)

     
    def accept_cookies(self):
        
        try:
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@data-test="allow-all"]')))
            accept_cookies_button.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

        # return self.driver 

    def scroll(self):
        # self.search()
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the middle of the page 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")
            
            # Wait to load page
            time.sleep(0.8)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def search(self):
        
        try: 
            search_bar= WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@name="search-term"]')))
            search_bar.send_keys(self.items_to_search)
            time.sleep(0.8)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(0.8)
        
        except TimeoutException:
            
            print("Loading took too much time! Maybe there is no cookies to accept!")
        
    

    def go_to_next_page(self):

        try: 
            # next= WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="js-plp-body"]/div[2]/nav/ul/li[2]/a/img')))
            # next[0].click()
            next= WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@aria-label="Next"]')))
            next[0].click()
        
        except TimeoutException:
            print("Loading took too much time! Seems there is no more page!")
            self.if_next_page=False
        
    
    def find_all_links(self):
        
        self.accept_cookies()
        time.sleep(0.8)
        
        self.search()
        time.sleep(0.8)

        link_list=[]
        page=0

        while self.if_next_page==True: 
            # page number
            page +=1
            print(f'page {page}')
            
            # scroll down to the bottom for items to load
            self.scroll()
            time.sleep(0.5)
            
            # extract item link from the current page
            links = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-content"]//div[@data-test="product-image-container"]//a[@href]')))
    
            for link in links:
                print (link)
                link_list.append(link.get_attribute('href'))
            
            # go to next page if there is any 
            self.go_to_next_page()
            time.sleep(0.5)
        
        print (len(link_list)) 

        return link_list
    
    # def extract_src(self):
    #     self.search()
    #     src=self.driver.find_element(by=By.XPATH, value='//img[@class="logo-logo--5b465"]')
    #     print(src.get_attribute('src'))
    
           

if __name__ =='__main__':
    url = 'https://www.johnlewis.com'
    item_to_search = 'dune shoes'
    Scraper(url,item_to_search).find_all_links()
   
    


