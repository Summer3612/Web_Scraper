import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import time
import urllib.request

class Scraper:

    def __init__(self, URL: str='https://www.johnlewis.com'):
        self.URL = URL
        
        # not to close window once the method is running
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        chr_options.add_argument("--disable-notifications")
        
        self.driver = webdriver.Chrome(options=chr_options)
        self.delay = 2
        self._get_driver(self.URL)
    
    @staticmethod
    def create_folder(folder_name:str, folder_path:str='/Users/shubosun/Desktop/'):
        try:
            path = os.path.join(folder_path,folder_name)
            os.mkdir(path)
            print("Folder for product " , folder_name ,  " Created ") 
        except FileExistsError:
            print("Folder for product " , folder_name ,  " already exists")
        except FileNotFoundError: 
            print("Folder path does not exist, re-enter!")
        
        return path
    
    @staticmethod
    def download_image(image_url:str, image_name:str, folder_path:str='/Users/shubosun/Desktop/'):
        name=f"{folder_path}/{image_name}.jpg"
        urllib.request.urlretrieve(image_url,name)


    def _find_element(self, xpath:str): 
        element = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return element 

    
    def _accept_cookies(self,xpath:str='//*[@data-test="allow-all"]'):
    
        try:
            accept_cookies_button = self._find_element(xpath)
            accept_cookies_button.click()
        except TimeoutException:
            print("Loading took too much time! No cookies to accept")


    def _close_pop_up_windor(self, xpath:str='//*[@id="closeModal"]'):
        try:
            close_button = self._find_element(xpath)
            close_button.click()
        except TimeoutException:
            print("Loading took too much time! No pop-up window to close")


    def _close_live_chat_box(self, xpath: str ='//span[@id="closeButtonId"]' ):
        
        try:
            chat_box= self._find_element(xpath)
            chat_box.click()
        
        except TimeoutException:
            print("Loading took too much time! Maybe there is no live chat box!")


    def _get_driver(self,url:str):
        self.driver.get(url)
        self._close_pop_up_windor()
        self._accept_cookies()
        self._close_live_chat_box()
        


    def _scroll_down(self):

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1800);")


    def _scroll_down_till_bottom(self):

        """
        This method is for website to keep scrolling down until the page is no longer loading. 

        """
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the middle of the page 
            self._scroll_down()
            # Wait to load page
            time.sleep(0.3)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight-10")
            if new_height == last_height:
                break
            last_height = new_height
    
    def _go_to_next_page(self, xpath:str='//a[@aria-label="Next"]'):

        next= self._find_element(xpath)
        next.click()
    
    
    def search(self, item_to_search:str, xpath:str = '//input[@name="search-term"]'):
        
        search_bar= self._find_element(xpath)
        search_bar.send_keys(item_to_search)
        time.sleep(self.delay)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(self.delay)
    
    def find_all_search_result_links(self)->list:

        """This method is to get the link of all products of search result"""

        link_list=[]
        page=0
    

        while True: 
            # page number
            page +=1
            print(f'page {page}')
            
            # scroll down to the bottom for items to load
            self._scroll_down_till_bottom()
            time.sleep(0.5)
            
            # extract item link from the current page
            links = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-content"]//div[@data-test="product-image-container"]//a[@href]')))
    
            for link in links:
                print (link.get_attribute('href'))
                link_list.append(link.get_attribute('href'))
            
            # go to next page if there is any 
            try: 
                self._go_to_next_page()
                time.sleep(0.5)
         
            except TimeoutException:
                print("Loading took too much time! Seems this is the last page!")
                break
        
        print (len(link_list)) 

        return link_list





  
    