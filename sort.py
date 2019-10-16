import json

if __name__ == '__main__':
    with open('result.json', mode='r') as f:
        items = json.load(f)

    def get_packed_weight(item):
        specs = item["props"]["specs"]
        packaged_weight = [x for x in specs if x["name"] == "Packaged Weight"][0]["values"][0]
        tokens = packaged_weight.split(' ')
        pounds = float(tokens[0])
        if len(tokens) >= 4:
            pounds = pounds + (float(tokens[2])/16.0)
        return pounds

    def get_weight_safe(item):
        try:
            return get_packed_weight(item)
        except:
            return 9999

    items_to_sort = [{"link": x["link"], "weight": get_weight_safe(x)} for x in items]

    items_to_sort.sort(key=lambda x: x["weight"])

    for item in items_to_sort:
        print(item)