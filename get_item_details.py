import requests
from lxml import etree
import xml.etree.ElementTree as ET

base_url = 'https://www.rei.com/c/backpacking-tents?r=c%3Bbest-use%3ABackpacking&pagesize=90&ir=category%3Abackpacking-tents&sort=max-price'

if __name__ == '__main__':
    search_page_resonse = requests.get(base_url)

    if search_page_resonse.status_code != 200:
        print("unable to get search page response, status was {0}".format(str(search_page_resonse.status_code)))
        exit
    else:
        print("got website content successfully")
    
    search_page_body = search_page_resonse.content.decode(encoding='utf-8')
    # as_split = search_page_body.splitlines()
    parser = etree.HTMLParser()
    tree = etree.fromstring(search_page_body, parser)
    search_results = tree.xpath('//div[@id=\'search-results\']/ul[1]/li')
    for c in search_results:
        pass
    # for search_result in search_results:
    #     link_node = search_results.xpath('/a[0]')
    #     link = "https://www.rei.com/" + link_node.attributes
    pass