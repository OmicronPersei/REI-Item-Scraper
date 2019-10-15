import requests
from lxml import objectify

base_url = 'https://www.rei.com/c/backpacking-tents?r=c%3Bbest-use%3ABackpacking&pagesize=90&ir=category%3Abackpacking-tents&sort=max-price'

if __name__ == '__main__':
    search_page_resonse = requests.get(base_url)

    if search_page_resonse.status_code != 200:
        print("unable to get search page response, status was {0}".format(str(search_page_resonse.status_code)))
        return
    
    search_page_body = search_page_resonse.content.decode()
    search_page = objectify.from_string(search_page_body)