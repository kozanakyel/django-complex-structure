from django.http import Http404
from rest_framework import authentication, generics, mixins, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

from api.authentication import TokenAuthentication
from api.mixins import StaffEditorPermissionMixin

from .models import Product
# from ..api.permission import IsStaffEditorPermission
from .serializers import ProductSerializer


class ProductListCreateAPIView(StaffEditorPermissionMixin, generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    # auth and permission goes to settings....
    # authentication_classes = [
    #     authentication.SessionAuthentication,
    #     TokenAuthentication,
    # ]
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = title
        serializer.save(content=content)
        # send a Django signal


product_list_create_view = ProductListCreateAPIView.as_view()


class ProductDetailAPIView(StaffEditorPermissionMixin, generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk'
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]


product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(StaffEditorPermissionMixin, generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.DjangoModelPermissions]
    lookup_field = "pk"
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ##


product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(StaffEditorPermissionMixin, generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"
    # permission_classes = [permissions.IsAdminUser, IsStaffEditorPermission]

    def perform_destroy(self, instance):
        # instance
        super().perform_destroy(instance)


product_destroy_view = ProductDestroyAPIView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#     """Not gonna use this method"""
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     # lookup_field = 'pk'


# product_list_view = ProductListAPIView.as_view()


# class CreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):
#     pass


class ProductMixinView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    generics.GenericAPIView,
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "pk"

    def get(self, request, *args, **kwargs):
        print(args, kwargs)
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):  # http > post
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        # print(serializer.validated_data)
        title = serializer.validated_data.get("title")
        content = serializer.validated_data.get("content") or None
        if content is None:
            content = "this is a single view coll staff"
        serializer.save(content=content)


product_mixin_view = ProductMixinView.as_view()


@api_view(["GET", "POST"])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method

    if method == "GET":
        if pk is not None:
            # queryset = Product.objects.filter(pk=pk)
            # if not queryset.exist():
            #     raise Http404
            obj = get_object_or_404(Product, pk=pk)  # > auto to 404
            data = ProductSerializer(obj, many=False).data
            return Response(data)
        # list view
        queryset = Product.objects.all()
        data = ProductSerializer(queryset, many=True).data
        return Response(data)

    if method == "POST":
        # create an item
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get("title")
            content = serializer.validated_data.get("content") or None
            if content is None:
                content = title
                serializer.save(content=content)
            return Response(serializer.data)
        return Response({"invalid": "not good data"}, status=400)
