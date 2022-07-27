# from ast import main
# from cgitb import text
# from lib2to3.pgen2 import driver
# from os import link
import requests
# from bs4 import BeautifulSoup
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import json
import uuid 
import os

# from urllib.request import BaseHandler

class Scraper:

    def __init__(self, URL: str, items_to_seach: str):
        self.URL = URL
        self.items_to_search = items_to_seach
        
        # not to close window once the method is running
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chr_options)

        self.path = self.driver.get(self.URL)
        self.delay = 5
        self.if_next_page=True
        
        # Create target Directory
       
        try:
            dirName = 'raw data'
            os.mkdir(dirName)
            print("Directory " , dirName ,  " Created ") 
        except FileExistsError:
            print("Directory " , dirName ,  " already exists")

     
    def _accept_cookies(self):
        
        try:
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@data-test="allow-all"]')))
            accept_cookies_button.click()
            time.sleep(1)
        except TimeoutException:
            print("Loading took too much time!")

        # return self.driver 

    def _scroll(self):
        # self.search()
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the middle of the page 
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")
            
            # Wait to load page
            time.sleep(0.3)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def _search(self):
        
        try: 
            search_bar= WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@name="search-term"]')))
            search_bar.send_keys(self.items_to_search)
            time.sleep(0.8)
            search_bar.send_keys(Keys.ENTER)
            time.sleep(0.8)
        
        except TimeoutException:
            
            print("Loading took too much time! Maybe there are no cookies to accept!")
        
    

    def _go_to_next_page(self):

        try: 
            # next= WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="js-plp-body"]/div[2]/nav/ul/li[2]/a/img')))
            # next[0].click()
            next= WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//a[@aria-label="Next"]')))
            next[0].click()
        
        except TimeoutException:
            print("Loading took too much time! Seems this is the last page!")
            self.if_next_page=False
        
    # private
    def _find_all_links(self):
        
        self._accept_cookies()
        time.sleep(0.8)
        
        self._search()
        time.sleep(0.8)

        self.link_list=[]
        page=0

        while self.if_next_page==True: 
            # page number
            page +=1
            print(f'page {page}')
            
            # scroll down to the bottom for items to load
            self._scroll()
            time.sleep(0.5)
            
            # extract item link from the current page
            links = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-content"]//div[@data-test="product-image-container"]//a[@href]')))
    
            for link in links:
                print (link.get_attribute('href'))
                self.link_list.append(link.get_attribute('href'))
            
            # go to next page if there is any 
            self._go_to_next_page()
            time.sleep(0.5)
        
        print (len(self.link_list)) 
        
    
    def _retrieve_text_from_each_page(self):
        
        self.link = 'https://www.johnlewis.com/dune-santino-nubuck-woven-trim-loafers/p5546120'
        self.driver.get(self.link)
        
        product_info_dic = {'uuid':str(uuid.uuid4()), 'product id': '', 'product name': '','product colour': '', 'product rating': '', 'available size and price':[], 'src links':[]}
        
        # get id from url e.g. https://www.johnlewis.com/dune-reid-waterproof-wellington-boots-black/p5403916
        product_info_dic['product id']=self.link.split('/')[4]
        
        # get product name and colour from the heading 'h1' of the page
        productName=WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="column-right"]/section/div[1]/div[1]/h1')))
        product_info_dic['product name']=productName.text.split(',')[0]
        product_info_dic['product colour']=productName.text.split(',')[1]
        
        # get rating - some products' rating is not availabe so try is used.
        try:
            productRating=WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="column-right"]/section/div[1]/div[2]/a/div/div[1]/div[2]/span')))
            product_info_dic['product rating']=float(productRating.text.split(' ')[9])
        
        except TimeoutException: 
            product_info_dic['product rating']='no rating available'

        # different size has different availability and price so the below is created
        size_list = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//button[@data-cy="size-selector-item"]')))
        
        size_availability_price=[]
        
        for size in size_list:
            temp_list=[]
            try:
                size.click()
                time.sleep(0.5)
            except: 
                pass
            
            # the attribute 'aria-label' of size is in the format like '4. This size is selected' if available or ' 8. This size is selected but unavailable'
            # split is used to get separated information of size and whether it is available
            size.get_attribute('aria-label').split('.')[0]
            temp_list.append(size.get_attribute('aria-label').split('.')[0])

            if 'unavailable' in size.get_attribute('aria-label').split('.')[1]:
                temp_list.append('unavailable')
            else: 
                temp_list.append('available')
            
            # get original price
            productPrice=WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="column-right"]/section/div[1]/div[2]/div/section[1]/span/span/span')))
            temp_list.append(float(productPrice.text.split('£')[1]))

            # get discounted price if on sale
            try: 
                discount_price=WebDriverWait(self.driver,0.5).until(EC.presence_of_element_located((By.XPATH,'//*[@id="column-right"]/section/div[1]/div[2]/div/section[1]/span/span[2]/span')))
                temp_list.append ('discount price '+discount_price.text)
            except TimeoutException: 
                temp_list.append ('no discount')
        
            size_availability_price.append(temp_list)

        product_info_dic['available size and price']=size_availability_price
   
        
        # get src of the images of the product 
        src_elements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@class="ImageMagnifier_image-wrapper__GhoSr"]')))

        product_src_list=[]
        for i in src_elements:
            src = i.find_element(By.CSS_SELECTOR,'img')
            product_src_list.append(src.get_attribute('src'))
        
        product_info_dic['src links'] = product_src_list

        print (product_info_dic)
        
        return product_info_dic

    def _save_image_locally(self):
        info= self._retrieve_text_from_each_page()

        for i in info['src links']:
            # need to find the local path to save image but currently downloading is fine
            urllib.request.urlretrieve(i,f"{info['product id']}_{info['src links'].index(i)}.jpg")


    

        
if __name__ =='__main__':
    url = 'https://www.johnlewis.com'
    item_to_search = 'dune shoes'
    Scraper(url,item_to_search)._save_image_locally()



    


