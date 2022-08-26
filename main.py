from scraper.JlScraper import JlScraper
from pandas import json_normalize
import pandas as pd

if __name__ =='__main__':
    
    john_lewis=JlScraper()
    # john_lewis.search('dune slipper')
    # product_list=john_lewis.find_all_search_result_links()
    
    # # df_new=pd.DataFrame()
    # for product in product_list:
    #     product_dic=john_lewis.create_prodcut_dic(product)
    #     john_lewis.save_product_info(product_dic)
    
    print (john_lewis.create_prodcut_dic('https://www.johnlewis.com/fitflop-iqushion-ergonomic-flip-flops/p3943629'))

    #     normalize_dic=json_normalize(product_dic)
    #     df=pd.DataFrame.from_dict(normalize_dic)
    #     df_new=pd.concat([df_new,df],axis=0)

        
    # print(df_new)