from django.http import JsonResponse, HttpResponse
import json
from django.forms.models import model_to_dict

from products.models import Product

from rest_framework.decorators import api_view
from rest_framework.response import Response

# http response get string, Jsonresponse get dict()

@api_view(["GET"])
def api_home(request, *args, **kwargs):
    """DRF api_view"""
    # # req.body
    # # req > HttpRequest > Django
    # # print(dir(request))
    # # print(request.GET)   # url query parameters
    # # print(request.POST)   # url query parameters
    # body = request.body # byte string of JSON data
    # data = {}
    # try:
    #     data = json.loads(body)  # string of jsdon data > python dict
    # except:
    #     pass
    # # print(data)
    
    # data["params"] = request.GET
    # data['headers'] = dict(request.headers)
    # data['content_type'] = request.content_type
    
    # if request.method != "POST":
    #     return Response({"detail": "GEt not allowed"}, status=405)
    model_data = Product.objects.all().order_by("?").first()
    data = {}
    if model_data:
        data = model_to_dict(model_data, fields=['id', 'title', 'price'])
    return Response(data)
        # print(data)
        # data = dict(data)
        # data["id"] = model_data.id
        # data["title"] = model_data.title
        # seriliazition
    #     json_data_str = json.dumps(data)
    # return HttpResponse(json_data_str, headers={'content-type':'application/json'})

