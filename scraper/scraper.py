import urllib.request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import json
from pandas import json_normalize
import uuid 
import os


# from urllib.request import BaseHandler

class Scraper:

    def __init__(self, URL: str='https://www.johnlewis.com'):
        self.URL = URL
        
        # not to close window once the method is running
        chr_options = Options()
        chr_options.add_experimental_option("detach", True)
        chr_options.add_argument("--disable-notifications")

        self.driver = webdriver.Chrome(options=chr_options)
        self.driver.get(self.URL)
        self.delay = 1
        self.if_next_page=True
    
    
    @staticmethod
    def create_folder(folder_name,folder_path:str='/Users/shubosun/Desktop/'):

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
    def save_dic_in_json(dic_to_save:dict, file_name:str,folder_path:str='/Users/shubosun/Desktop/'): 

        file=f"{folder_path}/{file_name}.json"
        with open(file,"w") as f:
            json.dump (dic_to_save,f, indent=2)


    @staticmethod
    def download_image_locally(image_url:str, image_name:str, folder_path:str='/Users/shubosun/Desktop/'):
            # need to find the local path to save image but currently downloading is fine
        name=f"{folder_path}/{image_name}.jpg"
        urllib.request.urlretrieve(image_url,name)

    
    def accept_cookies(self,path:str='//*[@data-test="allow-all"]'):
    
        try:
            accept_cookies_button = WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, path)))
            accept_cookies_button.click()
        except TimeoutException:
            print("Loading took too much time! Cookies are already accepted")

    
    # FIXME:it is not working. 
    def close_live_chat_box(self):
        
        # self.accept_cookies()
        try:
            chat_box= WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, '//span[@id="closeButtonId"]')))
            chat_box.click()
        
        except TimeoutException:
            print("Loading took too much time! Maybe there is no live chat box!")


    def scroll_down(self):

        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight-2000);")


    
    def scroll_down_till_bottom(self):

        """
        This method is for website to keep scrolling down until the page is no longer loading. 

        """
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to the middle of the page 
            self.scroll_down()
            # Wait to load page
            time.sleep(0.3)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    def search(self, item_to_search:str, xpath:str = '//input[@name="search-term"]'):
        
        search_bar= WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        search_bar.send_keys(item_to_search)
        time.sleep(0.5)
        search_bar.send_keys(Keys.ENTER)
        time.sleep(0.5)


    def go_to_next_page(self, xpath:str='//a[@aria-label="Next"]'):

        next= WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        next.click()
    
    def find_all_search_result_links(self)->list:

        """This method is to get the link of all products of search result"""

        link_list=[]
        page=0
    

        while True: 
            # page number
            page +=1
            print(f'page {page}')
            
            # scroll down to the bottom for items to load
            self.scroll_down_till_bottom()
            time.sleep(0.5)
            
            # extract item link from the current page
            links = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="main-content"]//div[@data-test="product-image-container"]//a[@href]')))
    
            for link in links:
                print (link.get_attribute('href'))
                link_list.append(link.get_attribute('href'))
            
            # go to next page if there is any 
            try: 
                self.go_to_next_page()
                time.sleep(0.5)
         
            except TimeoutException:
                print("Loading took too much time! Seems this is the last page!")
                break
        
        print (len(link_list)) 

        return link_list

class JlScraper(Scraper):

    def get_product_id(self, xpath:str = '//jl-store-stock')->str:
        name = WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        product_id = name.get_attribute('skuid')
        return product_id
    
    # FIXME: only certain categories of products are fine
    def get_product_name(self,xpath:str = '//div[@class="xs-up"]//*[@class="ProductTitle_title__JiefQ"]')->str:
        productName=WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH, xpath)))
        return productName.text


    def get_product_rating(self, xpath:str ='//span[@data-test="rating"]')->str:    
        # get rating - some products' rating is not availabe so try is used.
        
        rating = ''
        try:
            productRating=WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            rating=productRating[1].text
        
        except TimeoutException: 
            rating='no rating available'
        
        return rating

    # FIXME: only certain categories of products are fine
    # different size has different availability and price so the below is created in one method
    def get_product_size_availability_price_list(self,xpath:str ='//button[@data-cy="size-selector-item"]')->list: 
        self.accept_cookies()
        
        size_list = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

        size_availability_price=[]

        for size in size_list:
            temp_list=[]
            
            try:
                size.click()
                time.sleep(0.5)
                
            except Exception as e: 
                print(f'cannot click {size_list.index(size)}')
                print(e.args)
            
            # the attribute 'aria-label' of size is in the format like '4. This size is selected' if available or ' 8. This size is selected but unavailable'
            # split is used to get separated information of size and whether it is available
            size.get_attribute('aria-label').split('.')[0]
            temp_list.append(size.get_attribute('aria-label').split('.')[0])

            if 'unavailable' in size.get_attribute('aria-label').split('.')[1]:
                temp_list.append('unavailable')
            else: 
                temp_list.append('available')
            
            temp_list.append(self.get_product_price_history())


            size_availability_price.append(temp_list)

        return size_availability_price
   
    def get_product_src(self,xpath:str='//*[@class="ImageMagnifier_image-wrapper__GhoSr"]')->list: 
        # get src of the images of the product 
        src_elements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

        product_src_list=[]
        for i in src_elements:
            src = i.find_element(By.CSS_SELECTOR,'img')
            product_src_list.append(src.get_attribute('src'))
        
        return product_src_list
    
    # # FIXME: only certain categories of products are fine
    

    def get_product_price_history(self,xpath:str='//span[@class="ProductPrice_prices-list__jbkRS"]')->str:
        # price_element = WebDriverWait(self.driver,self.delay).until(EC.presence_of_element_located((By.XPATH,class_name)))
        price_elements =self.driver.find_elements(By.XPATH,xpath)
        # price=""
        # for element in price_elements:
        #     print (element.text)
        return price_elements[1].text

    def create_prodcut_dic(self,url:str)->dict:
        self.driver.get(url)
        time.sleep(1)
        self.close_live_chat_box()
    
        product_info_dic = {'uuid':str(uuid.uuid4()), 'product id': '', 'product name': '', 'product rating': '', 'available size and price':[], 'src links':[]}
        
        product_info_dic['product id']=self.get_product_id()
        product_info_dic['product name']=self.get_product_name()
        product_info_dic['product rating'] = self.get_product_rating()
        product_info_dic['available size and price']=self.get_product_size_availability_price_list()
        product_info_dic['src links'] = self.get_product_src()


        return product_info_dic

    def save_product_info(self,product_info_dic:dict):

        raw_data_folder_path= self.create_folder('raw data', '/Users/shubosun/Desktop/')
        product_folder_path = self.create_folder(product_info_dic['product id'],raw_data_folder_path)
        
        
        for src_link in product_info_dic['src links']:
            # need to find the local path to save image but currently downloading is fine
            name=product_info_dic['product id']+'_'+str(product_info_dic['src links'].index(src_link))
            self.download_image_locally(src_link,name ,product_folder_path)

        
        # df=pd.DataFrame.from_dict(product_info_dic, orient='index')
        self.save_dic_in_json(product_info_dic, product_info_dic['product id'],product_folder_path)
        df=json_normalize(product_info_dic)
        print(df)


        


  
    