import pandas as pd
import psycopg2
from scraper.scraper import Scraper
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import uuid
from pathlib import Path



class JlScraper(Scraper):

    def _get_product_id(self, xpath:str = '//jl-store-stock')->str:
        """This returns product id. """
        try: 
            name = self._find_element(xpath)
            product_id = name.get_attribute('skuid')
            return product_id
        
        except Exception as e:
            print (e)
    
    # FIXME: only certain categories of products are fine
    def _get_product_name(self,xpath:str = '//div[@class="xs-up"]//h1')->str:
        """This returns the product name."""
        try: 
            productName=self._find_element(xpath)
            return productName.text
        except Exception as e:
            print (e)

    def _get_product_rating(self, xpath:str ='//span[@data-test="rating"]')->str:    
        """This returns the rating of a product if any."""
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
    def _get_product_size_availability_price_list(self,xpath:str ='//button[@data-cy="size-selector-item"]')->list: 
        """This returns product available size and its price accordingly. Different sizes may have different prices."""
        try:
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
                
                temp_list.append(self._get_product_price_history())
                size_availability_price.append(temp_list)

            return size_availability_price
       
        except Exception as e:
            print (e)
    
    def _get_product_src(self,xpath:str='//*[@class="ImageMagnifier_image-wrapper__GhoSr"]')->list: 
        """This returns a list of srcs of a product."""
        # get src of the images of the product 
        try:
            src_elements = WebDriverWait(self.driver,self.delay).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))
            product_src_list=[]
            for i in src_elements:
                src = i.find_element(By.CSS_SELECTOR,'img')
                product_src_list.append(src.get_attribute('src'))
            
            return product_src_list
        
        except Exception as e:
            print (e)

    def _get_product_price_history(self,xpath:str='//span[@class="ProductPrice_prices-list__jbkRS"]')->str:
        """This method returns the history of price for a product. """
        try: 
            price_elements =self.driver.find_elements(By.XPATH,xpath)
            return price_elements[1].text
        except Exception as e:
            print (e)
        
    def create_prodcut_dic(self,url:str)->dict:
        """this method is to create a python dictionary to save the id, name, rating, size and price, src links of a product"""
        self._get_driver(url)
    
        product_info_dic = {'uuid':str(uuid.uuid4()), 'product id': '', 'product name': '', 'product rating': '', 'available size and price':[], 'src links':[]}
        
        product_info_dic['product id']=self._get_product_id()
        product_info_dic['product name']=self._get_product_name()
        product_info_dic['product rating'] = self._get_product_rating()
        product_info_dic['available size and price']=self._get_product_size_availability_price_list()
        product_info_dic['src links'] = self._get_product_src()

        return product_info_dic

    def save_image_locally(self,url:str, folder_name:str, file_name:str):
        """this method is to save the production information and pictures in a local folder"""
        folder_path=Path().resolve()
        raw_data_folder_path= self.create_folder('raw data', folder_path)
        product_folder_path = self.create_folder(folder_name,raw_data_folder_path)
        self.download_image(url, file_name,product_folder_path)  
    
    def upload_data_to_RDS(self, product_dic:dict):
        """This method upload scraped data to AWS RDS"""
       
        ENDPOINT = 'database-1.cizl8lhq8hlk.eu-west-2.rds.amazonaws.com' 
        USER = 'postgres'
        PASSWORD = '!Password'
        PORT = 5432
        DATABASE = 'postgres'
        
        df=pd.DataFrame.from_dict(product_dic, orient='index')
        
        uuid= df[0]['uuid']
        product_id = df[0]['product id']
        product_name = df[0]['product name']
        product_rating = df[0]['product rating']
        available_size_and_price = df[0]['available size and price']
        src_links = df[0]['src links']
        
        conn=None
        try:
            with  psycopg2.connect(host=ENDPOINT, 
                            port= PORT,
                            user=USER,
                            password=PASSWORD,
                            database=DATABASE
                            ) as conn: 
                
                with conn.cursor() as cur: 

                    # check if a record already exists. If yes, simply update the record;if not, upload the new record. 
                    cur.execute("SELECT product_id FROM dataset_test1 WHERE product_id=%s",(product_id,))

                    if cur.fetchone() is not None: 
                        update_script="UPDATE dataset_test1 SET uuid =%s, product_name=%s, product_rating = %s, available_size_and_price=%s, src_links=%s WHERE product_id=%s"
                        update_values= (uuid,product_name,product_rating, available_size_and_price, src_links, product_id,)
                        cur.execute(update_script,update_values)
                        print ("Info added in database.")
                    else: 
                        insert_script = "INSERT INTO dataset_test1 (uuid, product_id, product_name, product_rating, available_size_and_price, src_links) VALUES(%s,%s,%s,%s,%s,%s)"
                        insert_values = (uuid,product_id, product_name, product_rating, available_size_and_price ,src_links,)
                        cur.execute(insert_script,insert_values) 
                        print("Info updated in database.")

        except Exception as error:
            print (error)
        
        finally:
            if conn is not None: 
                conn.close()



