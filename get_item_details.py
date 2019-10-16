import requests
from lxml import etree
import time
import json

sleep_amount = 0.3

def get_html(link):
    response = requests.get(link)

    if response.status_code != 200:
        print("unable to get OK HTTP response, status was {0}".format(str(response.status_code)))

    return response.content.decode(encoding='utf-8')

def parse_html(html):
    parser = etree.HTMLParser()
    return etree.fromstring(html, parser)

def get_search_results(link):
    search_page_body = get_html(link)
    tree = parse_html(search_page_body)
    search_results = tree.xpath('//div[@id=\'search-results\']/ul[1]/li')
    return search_results

def get_search_results_with_retries(link):
    max_tries = 10
    search_results = None
    for _ in range(0,max_tries):
        try:
            search_results = get_search_results(link)
            if search_results == None:
                raise Exception()
            else:
                return search_results
        except:
            time.sleep(sleep_amount)

    if (search_results == None):
        print("After {} tries, still could not get search results".format(str(max_tries)))
        exit

def get_item_properties(link):
    response = get_html(link)
    page = parse_html(response)
    properties_elem = page.xpath('//script[@data-client-store=\'product-details\']')[0]
    return json.loads(properties_elem.text)

def get_item_props_with_retries(link):
    max_tries = 1
    for _ in range(0,max_tries):
        try:
            item_props = get_item_properties(link)
            return item_props
        except:
            time.sleep(sleep_amount)

    print("Could not get the item properties for {}".format(link))
    return None


if __name__ == '__main__':
    links = [
        'https://www.rei.com/c/backpacking-tents?pagesize=90',
        'https://www.rei.com/c/backpacking-tents?page=2&pagesize=90',
        'https://www.rei.com/c/backpacking-tents?page=3&pagesize=90',
        'https://www.rei.com/c/camping-tents?pagesize=90',
        'https://www.rei.com/c/tents?page=2&pagesize=90',
        'https://www.rei.com/c/tents?page=3&pagesize=90',
        'https://www.rei.com/c/tents?page=4&pagesize=90',
        'https://www.rei.com/c/tents?page=5&pagesize=90',
        'https://www.rei.com/c/tents?page=6&pagesize=90',
        'https://www.rei.com/c/tents?page=7&pagesize=90'

    ]
    search_results = []
    for link in links:
        result = list(get_search_results_with_retries(link))
        search_results.extend(result)

    search_results = set(search_results)
    
    items = []
    for search_result in search_results:
        link_node = search_result.xpath('a[1]')[0]
        link = "https://www.rei.com" + link_node.attrib["href"]

        if 'rei-garage' in link:
            continue

        item_props = get_item_props_with_retries(link)

        print("Link: {}\n".format(link))

        if item_props == None:
            continue

        item_obj = { "link": link, "props": item_props }
        items.append(item_obj)
        time.sleep(sleep_amount)

    with open('result.json', mode='w') as f:
        json_serialized = json.dumps(items)
        f.write(json_serialized)