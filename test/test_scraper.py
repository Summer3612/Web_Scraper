
from scraper.Scraper import Scraper
import unittest
from unittest.mock import patch, Mock
from selenium.webdriver.common.by import By


class TestScraper:

    def setup(self):
        
        self.test_Scraper = Scraper() 


    @patch('scraper.Scraper.time.sleep')
    @patch('scraper.Scraper.Scraper._find_element')
    def test_search(
        self,
        mock_find_element:Mock,
        mock_sleep:Mock
        ):
        self.test_Scraper.search('shoes')
        mock_find_element.assert_called_with('//input[@name="search-term"]')
        assert mock_sleep.call_count == 2

        mock_find_element.send_keys= Mock()
        # FIXME: how to test send_keys in search()
        # assert mock_find_element.send_keys.call_count==2

    def test_find_all_search_result_links(self):
        
        self.test_Scraper.search('bedding sets')
        list = self.test_Scraper.find_all_search_result_links()
        element = self.test_Scraper.driver.find_element(by = By.XPATH, value='//span[@id="screen-reader-updates"]')
        assert element.text.split(' ')[2] == str(len(list))
    
    def tearDown(self) -> None:
        return super().tearDown()

if __name__=='__main__':
    unittest.main(argv=[''],verbosity = 2, exit=True)
    