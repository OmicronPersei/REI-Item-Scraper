import json

sort_prop = input("enter prop to sort on:")
with open('result.json', mode='r') as f:
    items = json.load(f)

items.sort(key=lambda item: item[sort_prop])

for item in items:
    print(item)