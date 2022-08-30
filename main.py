from scraper.JlScraper import JlScraper


if __name__ =='__main__':
    
    john_lewis=JlScraper()
    john_lewis.search('dune slippers')
    product_list=john_lewis.find_all_search_result_links()

    new_dic={}
    i=1
    for product in product_list:
        product_dic=john_lewis.create_prodcut_dic(product)
        # john_lewis.save_product_info(product_dic)
        new_dic[i]=product_dic
        
        for src_link in product_dic['src links']:
        
            name=product_dic['product id']+'_'+str(product_dic['src links'].index(src_link))
            john_lewis.upload_file(src_link,'aicoredb',name)
        
        i=i+1
    
    john_lewis.upload_data_to_RDS(new_dic)


    
