
from scraper.Scraper import Scraper
import unittest
from unittest import mock
from unittest.mock import patch, Mock, call
from selenium.webdriver.common.keys import Keys



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
        assert mock_find_element.call_count==1
        mock_find_element.send_keys = 

    
    
    def tearDown(self) -> None:
        
        return super().tearDown()

if __name__=='__main__':
    unittest.main(argv=[''],verbosity = 2, exit=True)
    