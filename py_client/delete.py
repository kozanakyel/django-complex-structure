import requests

product_id = input("waht is product deleted: \n")
try: 
    product_id = int(product_id)
except:
    print(f'{product_id} not a valid id')

if product_id:
    endpoint = f"http://localhost:8000/api/products/{product_id}/delete/"  # http://127.0.0.1:8000/

    get_response = requests.delete(endpoint)

print(get_response.status_code, get_response.status_code==204)