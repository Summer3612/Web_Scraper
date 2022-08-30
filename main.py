from scraper.JlScraper import JlScraper
from pandas import json_normalize
import pandas as pd
import boto3
import os

if __name__ =='__main__':
    
    john_lewis=JlScraper()
    # john_lewis.search('dune slippers')
    # product_list=john_lewis.find_all_search_result_links()

    # new_dic={}
    # i=1
    # for product in product_list:
    #     product_dic=john_lewis.create_prodcut_dic(product)
    #     john_lewis.save_product_info(product_dic)
    #     new_dic[i]=product_dic
    #     i=i+1
    #     # with open(f"/Users/shubosun/Desktop/DATA_COLLECTION/raw data/{product_dic['product id']}/{product_dic['product id']}.json",'r') as f:
    #     #     data=json.loads(f.read())
    #     #     df=pd.json_normalize(
    #     #         data,
    #     #         record_path=["available size and price"],
    #     #         meta=['uuid',
    #     #             'product id',
    #     #             'product name',
    #     #             'product rating',
    #     #             ]
    #     #         )
    #     #     print (df)
    
    
    # john_lewis._save_dic_in_json(new_dic, 'all_product', '/Users/shubosun/Desktop/Data_Collection/raw data')

    # df=pd.DataFrame.from_dict(new_dic, orient='index')
    # print (df)

    john_lewis.upload_directory('/Users/shubosun/Desktop/DATA_COLLECTION/raw data/','aicoredb')

