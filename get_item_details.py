import requests
from lxml import etree
import xml.etree.ElementTree as ET
import time
import json

def get_html(link):
    response = requests.get(link)

    if response.status_code != 200:
        print("unable to get OK HTTP response, status was {0}".format(str(response.status_code)))

    return response.content.decode(encoding='utf-8')

def parse_html(html):
    parser = etree.HTMLParser()
    return etree.fromstring(html, parser)

def get_search_results():
    base_url = 'https://www.rei.com/c/backpacking-tents?r=c%3Bbest-use%3ABackpacking&pagesize=90&ir=category%3Abackpacking-tents&sort=max-price'
    search_page_body = get_html(base_url)
    tree = parse_html(search_page_body)
    search_results = tree.xpath('//div[@id=\'search-results\']/ul[1]/li')
    return search_results

def get_item_properties(link):
    response = get_html(link)
    page = parse_html(response)
    properties_elem = page.xpath('//script[@data-client-store=\'product-details\']')[0]
    return json.loads(properties_elem.text)

def get_packed_weight(item_properties):
    specs = item_properties["specs"]
    packed_weight = [x for x in specs if x["name"] == "Packaged Weight"][0]
    value = packed_weight["values"][0]
    tokens = value.split(' ')
    pounds = int(tokens[0])
    if len(tokens) == 4:
        pounds = pounds + (float(tokens[2])/16.0)
    return pounds



if __name__ == '__main__':
    
    max_tries = 10
    i = 0
    search_results = None
    while (search_results == None) or (i == max_tries):
        search_results = get_search_results()
        if search_results == None:
            time.sleep(5)
            i = i + 1

    if (search_results == None):
        print("After {} tries, still could not get search results".format(str(max_tries)))
        exit
    
    items = []
    for search_result in search_results:
        link_node = search_result.xpath('a[1]')[0]
        link = "https://www.rei.com/" + link_node.attrib["href"]
        item_props = get_item_properties(link)
        packed_weight = get_packed_weight(item_props)
        print("Link: {}\nPacked Weight: {}".format(link, packed_weight))
        item_obj = { "link": link, "packaged weight": packed_weight }
        items.append(item_obj)
        time.sleep(2)
    pass