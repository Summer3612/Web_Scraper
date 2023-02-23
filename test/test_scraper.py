
from scraper.JlScraper import JlScraper
from scraper.scraper import Scraper
import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pathlib
import os

class TestScraper:
    def setup(self):
        self.test_Scraper = Scraper() 
        self.delay = 2

    def test_search(self):
        """This tests if the function can search certain items"""
        self.test_Scraper = Scraper() 
        self.test_Scraper.search('kdoeld')
        element = WebDriverWait(self.test_Scraper.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//h1[@tabindex="-1"]/span')) )     
        assert element.text=="Sorry, we couldn't find any results for ‘kdoeld’"

    def test_find_all_search_result_links(self):
        """This test should find all the links of the search results. """
        test=JlScraper()
        test.search('bedding sets')
        list = test.find_all_search_result_links()
        element = WebDriverWait(test.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//span[@id="screen-reader-updates"]')) )
        assert element.text.split(' ')[2] == str(len(list))
    
    def test_download_image(self):
        path = pathlib.Path(__file__).parent.resolve()
        res = self.test_Scraper.download_image('https://johnlewis.scene7.com/is/image/JohnLewis/005768064alt3?$rsp-pdp-port-640$','test_image', path)
        print(path)
        path = str(path) +'/test_image.jpg'
        assert str(res) == path
        os.remove(path)    
    
    def test_create_folder(self):
        path = pathlib.Path(__file__).parent.resolve()
        
        res = self.test_Scraper.create_folder('trial',path)
        assert res == str(path)+'/trial'
        
        res = self.test_Scraper.create_folder('trial',path)
        assert res == str(path)+'/trial'

        os.rmdir(str(path)+'/trial')

        path = '/usr/1234'
        res = self.test_Scraper.create_folder('trial',path)
        assert res == 'Folder path does not exist, re-enter!'


    def tearDown(self) -> None:
        return super().tearDown()

if __name__=='__main__':
    unittest.main(argv=[''],verbosity = 2, exit=True)
    