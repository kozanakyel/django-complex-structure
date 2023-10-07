import requests

headers = {
    "Authorization": "Bearer 9d7510dca3de182f68a21766c3634aebf4f3babd"
}

endpoint = "http://localhost:8000/api/products/"  
# http://127.0.0.1:8000/admin/
# session > post data
# selenium

data = {
    "title": "this field is Done",
    "price": 32.99,
    
}

get_response = requests.post(endpoint, json=data, headers=headers)

print(get_response.json())