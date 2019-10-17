import json
import sys

if __name__ == '__main__':
    with open('scraped_data.json', mode='r') as f:
        items = json.load(f)

    def get_spec(item, prop):
        specs = item["props"]["specs"]
        matching_specs = [x for x in specs if x["name"].lower() == prop.lower()]
        if len(matching_specs) == 0:
            return None
        
        return matching_specs[0]["values"][0]

    def parsed_packed_weight_str_to_float(item):
        packaged_weight = get_spec(item, "packaged weight")
        tokens = packaged_weight.split(' ')
        pounds = float(tokens[0])
        if len(tokens) >= 4:
            pounds = pounds + (float(tokens[2])/16.0)
        return pounds

    def get_weight_safe(item):
        try:
            return parsed_packed_weight_str_to_float(item)
        except:
            return None

    def get_sleeping_capacity(item):
        return get_spec(item, "sleeping capacity")

    def get_price(item):
        return item["price_data"]["max"]

    items = [{
        "link": x["link"], 
        "weight": get_weight_safe(x), 
        "sleeping capacity": get_sleeping_capacity(x),
        "price": get_price(x)} for x in items]

    with open('results.csv', mode='w') as f:
        keys = [x for x in items[0]]
        f.write(','.join(keys) + '\n')
        for item in items:
            item_line = ','.join([str(item[k]) for k in keys])
            f.write(item_line + '\n')    