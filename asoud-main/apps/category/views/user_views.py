from rest_framework import views
from rest_framework.response import Response

from utils.response import ApiResponse

from apps.category.models import (
    Group, Category, SubCategory,
    ProductGroup, ProductCategory, ProductSubCategory)
from apps.category.serializers.user_serializers import (
    GroupListSerializer, CategoryListSerializer, SubCategoryListSerializer,
    ProductGroupListSerializer, ProductCategoryListSerializer,
    ProductSubCategoryListSerializer, SubCategoryImgSerializer,
    CategoryImgSerializer, GroupImgSerializer)


class GroupListAPIView(views.APIView):
    def get(self, request, format=None):
        group_list = Group.objects.all()

        serializer = GroupListSerializer(
            group_list,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class CategoryListAPIView(views.APIView):
    def get(self, request, pk, format=None):
        try:
            group_obj = Group.objects.get(id=pk)
        except:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Group Not Found"
                )
            )
        
        category_list = Category.objects.filter(group=group_obj)

        serializer = CategoryListSerializer(
            category_list,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class SubCategoryListAPIView(views.APIView):
    def get(self, request, pk, format=None):
        try:
            category_obj = Category.objects.get(id=pk)
        except:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Category Not Found"
                )
            )
        
        sub_category_list = SubCategory.objects.filter(category=category_obj)

        serializer = SubCategoryListSerializer(
            sub_category_list,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
    

class SliderImageApiView(views.APIView):
    def get(self, request, pk=None):
        try:
            sub_category_obj = SubCategory.objects.get(id=pk)
        except:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Sub Category Not Found"
                )
            )
        if sub_category_obj.market_slider_img:
            print('1111')
            serializer = SubCategoryImgSerializer(
                sub_category_obj,
            )
            success_response = ApiResponse(
                success=True,
                code=200,
                data=serializer.data,
                message='Data retrieved successfully'
            )
            return Response(success_response)
        elif sub_category_obj.category.market_slider_img:
            print('2222')
            serializer = CategoryImgSerializer(
                sub_category_obj.category,
            )
            success_response = ApiResponse(
                success=True,
                code=200,
                data=serializer.data,
                message='Data retrieved successfully'
            )
            return Response(success_response)
        elif sub_category_obj.category.group.market_slider_img:
            print('3333')
            serializer = GroupImgSerializer(
                sub_category_obj.category.group,
            )
            success_response = ApiResponse(
                success=True,
                code=200,
                data=serializer.data,
                message='Data retrieved successfully'
            )
            return Response(success_response)
        return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Market slider img Not Found"
                )
            )


class ProductGroupListAPIView(views.APIView):
    def get(self, request, format=None):
        product_group_list = ProductGroup.objects.all()

        serializer = ProductGroupListSerializer(
            product_group_list,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class ProductCategoryListAPIView(views.APIView):
    def get(self, request, pk, format=None):
        try:
            product_group_obj = ProductGroup.objects.get(id=pk)
        except:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Product Group Not Found"
                )
            )
        
        product_category_list = ProductCategory.objects.filter(product_group=product_group_obj)

        serializer = ProductCategoryListSerializer(
            product_category_list,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)


class ProductSubCategoryListAPIView(views.APIView):
    def get(self, request, pk, format=None):
        try:
            product_category_obj = ProductCategory.objects.get(id=pk)
        except:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Category Not Found"
                )
            )
        
        product_sub_category_list = ProductSubCategory.objects.filter(product_category=product_category_obj)

        serializer = SubCategoryListSerializer(
            product_sub_category_list,
            many=True,
            context={"request": request},
        )

        success_response = ApiResponse(
            success=True,
            code=200,
            data=serializer.data,
            message='Data retrieved successfully'
        )

        return Response(success_response)
