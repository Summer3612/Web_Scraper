
from scraper.JlScraper import JlScraper
import unittest
from unittest.mock import patch, Mock
import psycopg2
from pathlib import Path
import os


class TestScraper:

    def setup(self):
        self.test_JlScraper = JlScraper() 

    @patch('scraper.JlScraper.uuid.uuid4')
    @patch('scraper.JlScraper.JlScraper._get_driver')
    @patch('scraper.JlScraper.JlScraper._get_product_src')
    @patch('scraper.JlScraper.JlScraper._get_product_size_availability_price_list')
    @patch('scraper.JlScraper.JlScraper._get_product_rating')
    @patch('scraper.JlScraper.JlScraper._get_product_name')
    @patch('scraper.JlScraper.JlScraper._get_product_id')
    def test_create_product_dic(self,
        mock_id:Mock,
        mock_name:Mock,
        mock_rating:Mock,
        mock_size_and_price:Mock,
        mock_src:Mock,
        mock_get_driver:Mock,
        mock_uuid:Mock
        ):
   
        self.test_JlScraper.create_prodcut_dic('https://www.johnlewis.com/fitflop-iqushion-ergonomic-flip-flops/p3943629')

        mock_id.assert_called_once()
        mock_name.assert_called_once()
        mock_rating.assert_called_once()
        mock_size_and_price.assert_called_once()
        mock_src.assert_called_once()
        mock_uuid.assert_called_once()
        mock_get_driver.assert_called_with('https://www.johnlewis.com/fitflop-iqushion-ergonomic-flip-flops/p3943629')
    

    def test_upload_data_to_RDS(self):
        dict =   {"uuid": "0cb1725e-07ed-483b-a7de-2b7206cbc501",
                "product id": "238963910",
                "product name": "Dune Snuggled Slippers, Leopard Print",
                "product rating": "Product review details, This product has received, on average, 5.00 star reviews,",
                "available size and price": [
                    [
                    "6",
                    "unavailable",
                    "\u00a335.00"
                    ],
                    [
                    "7",
                    "unavailable",
                    "\u00a335.00"
                    ]
                ],
                "src links": [
                    "https://johnlewis.scene7.com/is/image/JohnLewis/005124003?$rsp-pdp-port-640$",
                ] }
        
        self.test_JlScraper.upload_data_to_RDS(dict)

        ENDPOINT = 'database-1.cizl8lhq8hlk.eu-west-2.rds.amazonaws.com' 
        USER = 'postgres'
        PASSWORD = '!Password'
        PORT = 5432
        DATABASE = 'postgres'

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
                    cur.execute("SELECT product_id FROM dataset_test1 WHERE product_id=%s",('238963910',))
                    record = cur.fetchall() 
                    assert len(record)==1
                    for row in record: 
                        assert row[2]=="Dune Snuggled Slippers, Leopard Print"       

        except Exception as error:
            print (error)
            
        finally:
            if conn is not None: 
                conn.close()
        
    def test_save_image_locally(self):
         self.test_JlScraper.save_image_locally('https://johnlewis.scene7.com/is/image/JohnLewis/005124003?$rsp-pdp-port-640$','test','test_image')
         folder_path=Path().resolve()
         test_image_path = f"{str(folder_path)}/raw data/test/test_image.jpg"
         assert os.path.exists(test_image_path)==True
         os.remove(test_image_path)
         os.rmdir(f"{str(folder_path)}/raw data/test")
    
        
    def tearDown(self) -> None:
        return super().tearDown()

if __name__=='__main__':
    unittest.main(argv=[''],verbosity = 2, exit=True)
    