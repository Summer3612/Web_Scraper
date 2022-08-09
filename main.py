from scraper.Scraper import JlScraper

if __name__ =='__main__':
    
    john_lewis=JlScraper()
    # john_lewis.accept_cookies()
    # john_lewis.search('dune shoes')
    # products=john_lewis.find_all_search_result_links()
    product_dic=john_lewis.create_prodcut_dic('https://www.johnlewis.com/john-lewis-anyday-baby-flower-heart-sleepsuit-pack-of-3-pink-multi/p6202474')
    john_lewis.save_product_info(product_dic)