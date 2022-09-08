
from scraper.JlScraper import JlScraper
import unittest
from unittest.mock import patch, Mock
import psycopg2
import boto3


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
        
    def test_save_image_remotely(self):
        
        src_link='https://johnlewis.scene7.com/is/image/JohnLewis/005124003?$rsp-pdp-port-640$'
    
        assert self.test_JlScraper.save_image_remotely(src_link,'aicoredb','test')=='success'
        assert self.test_JlScraper.save_image_remotely(src_link,'aicoredb','test')=='Image already exists in the bucket.'
        
        s3=boto3.resource('s3')
        obj = s3.Object("aicoredb", "test.jpg")
        obj.delete()


    # @patch('scraper.JlScraper.JlScraper._save_dic_in_json')
    # @patch('scraper.JlScraper.JlScraper._download_image_locally')
    # @patch('scraper.JlScraper.JlScraper._create_folder')
    # def test_save_image_locally(self,
    #     mock_create_folder:Mock,
    #     mock_download:Mock,
    #     mock_save_dic_in_json:Mock
    
    #     ):

    #     dict =   {"uuid": "0cb1725e-07ed-483b-a7de-2b7206cbc501",
    #             "product id": "238963910",
    #             "product name": "Dune Snuggled Slippers, Leopard Print",
    #             "product rating": "Product review details, This product has received, on average, 5.00 star reviews,",
    #             "available size and price": [
    #                 [
    #                 "6",
    #                 "unavailable",
    #                 "\u00a335.00"
    #                 ],
    #                 [
    #                 "7",
    #                 "unavailable",
    #                 "\u00a335.00"
    #                 ]
    #             ],
    #             "src links": [
    #                 "https://johnlewis.scene7.com/is/image/JohnLewis/005124003?$rsp-pdp-port-640$",
                    
    #             ] }

    #     self.test_JlScraper.save_product_info(dict)
        
    #     expected_1=[('raw data', '/Users/shubosun/Desktop/Data_Collection'),('238963910','/Users/shubosun/Desktop/Data_Collection/raw data')]
    #     mock_create_folder.call_args_list== expected_1

    #     expected_2=[("https://johnlewis.scene7.com/is/image/JohnLewis/005124003?$rsp-pdp-port-640$","238963910_0",'/Users/shubosun/Desktop/Data_Collection/raw data')]
    #     mock_download.call_args_list ==expected_2
    
    #     expected_3=[(dict,'238963910','/Users/shubosun/Desktop/Data_Collection/raw data')]
    #     mock_save_dic_in_json.call_args_list==expected_3

        
    def tearDown(self) -> None:
        return super().tearDown()

if __name__=='__main__':
    unittest.main(argv=[''],verbosity = 2, exit=True)
    