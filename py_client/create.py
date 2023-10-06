import requests

endpoint = "http://localhost:8000/api/products/"  
# http://127.0.0.1:8000/admin/
# session > post data
# selenium

data = {
    "title": "this field is Done",
    "price": 32.99,
    
}

get_response = requests.post(endpoint, json=data)

print(get_response.json())