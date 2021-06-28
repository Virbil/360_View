import requests
import json

response = requests.get('https://fakestoreapi.com/products')

data = json.loads(response.text)
json_formatted_str = json.dumps(data, indent=2)
print(json_formatted_str)