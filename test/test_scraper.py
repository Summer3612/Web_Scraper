
from scraper.JlScraper import JlScraper
from scraper.Scraper import Scraper
import unittest
from unittest.mock import patch, Mock
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TestScraper:

    def test_search(self):
        self.test_Scraper = Scraper() 
        self.delay = 2
        self.test_Scraper.search('kdoeld')
        element = WebDriverWait(self.test_Scraper.driver, self.delay).until(EC.presence_of_element_located((By.XPATH, '//h1[@tabindex="-1"]/span')) )     
        assert element.text=="Sorry, we couldn't find any results for ‘kdoeld’"

    def test_find_all_search_result_links(self):
        
        delay=2
        test=JlScraper('https://www.johnlewis.com/search?search-term=bedding%20sets&suggestion=true')
        list = test.find_all_search_result_links()
        element = WebDriverWait(test.driver, delay).until(EC.presence_of_element_located((By.XPATH, '//span[@id="screen-reader-updates"]')) )
        assert element.text.split(' ')[2] == str(len(list))
    
    def tearDown(self) -> None:
        return super().tearDown()

if __name__=='__main__':
    unittest.main(argv=[''],verbosity = 2, exit=True)
    