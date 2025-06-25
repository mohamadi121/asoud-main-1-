from django.urls import path

from apps.category.views.user_views import(
    GroupListAPIView, SubCategoryListAPIView, CategoryListAPIView,
    ProductGroupListAPIView, ProductCategoryListAPIView,
    ProductSubCategoryListAPIView
    )

app_name = 'category_general'

urlpatterns = [
    path(
        'group/list/',
        GroupListAPIView.as_view(),
        name='group-list',
    ),
    path(
        'list/<str:pk>/',
        CategoryListAPIView.as_view(),
        name='category-list',
    ),
    path(
        'sub/list/<str:pk>/',
        SubCategoryListAPIView.as_view(),
        name='sub-category-list',
    ),
    path(
        'product-group/list/',
        ProductGroupListAPIView.as_view(),
        name='group-list',
    ),
    path(
        'product/list/<str:pk>/',
        ProductCategoryListAPIView.as_view(),
        name='product-category-list',
    ),
    path(
        'product/sub/list/<str:pk>/',
        ProductSubCategoryListAPIView.as_view(),
        name='product-sub-category-list',
    ),
]
