from scraper.JlScraper import JlScraper

if __name__ =='__main__':
    
    john_lewis=JlScraper(headless=True)
    john_lewis.search('dune slippers')
    product_list=john_lewis.find_all_search_result_links()
 
    i=0
    
    for product in product_list:
        if i<5:
            product_dic=john_lewis.create_prodcut_dic(product)
            john_lewis.upload_data_to_RDS(product_dic)

            for src_link in product_dic['src links']:
                folder_name=product_dic['product id']
                file_name=product_dic['product id']+'_'+str(product_dic['src links'].index(src_link))
                print(src_link)
                #  save image locallly 
                # john_lewis.save_image_locally(src_link,folder_name, file_name)
                john_lewis.save_image_remotely(src_link,'aicoredb', file_name)
        i=i+1
                    
