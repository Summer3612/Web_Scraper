from scraper.JlScraper import JlScraper
import boto3
from boto3 import exceptions
import sqlalchemy
from sqlalchemy import String, create_engine,Column,MetaData,Table




if __name__ =='__main__':
    
    # DATABASE_TYPE = 'postgresql'
    # DBAPI = 'psycopg2'
    # ENDPOINT = 'database-1.cizl8lhq8hlk.eu-west-2.rds.amazonaws.com' 
    # USER = 'postgres'
    # PASSWORD = '!Password'
    # PORT = 5432
    # DATABASE = 'postgres'
        
    # engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{ENDPOINT}:{PORT}/{DATABASE}", echo=True)
    # engine.connect() 
    # meta=MetaData().
    # product_datatable=Table(
    #     'dataset_test1',meta,
    #     # Column('index', Integer, primary_key= True),
    #     Column('uuid', String),
    #     Column('product_id', String),
    #     Column('product_name', String),
    #     Column('product_rating', String),
    #     Column('available_size_and_price',String),
    #     Column('src_links', String)
    #     )
    # meta.create_all(engine)
    
    
    john_lewis=JlScraper(headless=True)
    john_lewis.search('DUNE slippers')
    product_list=john_lewis.find_all_search_result_links()
 
    i=0
    
    for product in product_list:
        if i<100:
            product_dic=john_lewis.create_prodcut_dic(product)
            
            john_lewis.upload_data_to_RDS(product_dic)
            for src_link in product_dic['src links']:
            
                folder_name=product_dic['product id']
                file_name=product_dic['product id']+'_'+str(product_dic['src links'].index(src_link))
                # save image remotely
                # john_lewis.save_image_remotely(src_link,'aicoredb',file_name)
                #  save image locallly 
                # john_lewis.save_image_locally(src_link,folder_name, file_name)
        i=i+1
