import requests

endpoint = "http://localhost:8000/api/products/1/update/"  # http://127.0.0.1:8000/
data = {
    "title":"hello world my old friend",
    "price":12000.34
}

get_response = requests.put(endpoint, json=data)

print(get_response.json())