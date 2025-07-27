from rest_framework import views, status, permissions
from rest_framework.response import Response
from django.shortcuts import render
from django.http import HttpResponse
from utils.response import ApiResponse

from apps.market.models import Market
from apps.market.serializers.user_serializers import (
    MarketListSerializer,
    MarketDetailSerializer
)
from apps.product.models import Product
from apps.product.serializers.owner_serializers import ProductDetailSerializer
from apps.advertise.models import Advertisement
from apps.advertise.serializers import AdvertiseSerializer
from apps.users.models import UserBankInfo
from apps.users.serializers import UserBankInfoListSerializer
import re
# Create your views here.


class MarketDetailView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        market_id = request.GET.get('id')
        if not market_id:
            return Response(
                ApiResponse(
                    success=False,
                    code=400,
                    error="Market Id Not Provided"
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            market = Market.objects.get(id=market_id)
        except Market.DoesNotExist:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Market Not Found"
                ),
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = MarketListSerializer(market)
        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serializer.data
            )
        )
        

class ProductDetailView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        product_id = request.GET.get('id')
        if not product_id:
            return Response(
                ApiResponse(
                    success=False,
                    code=400,
                    error="Product Id Not Provided"
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Product Not Found"
                ),
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = ProductDetailSerializer(product)

        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serializer.data
            )
        )


class AdvertizeDetailView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ad_id = request.GET.get('id')
        if not ad_id:
            return Response(
                ApiResponse(
                    success=False,
                    code=400,
                    error="Advertisement Id Not Provided"
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            ad = Advertisement.objects.get(id=ad_id)
        except Advertisement.DoesNotExist:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Advertisement Not Found"
                ),
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AdvertiseSerializer(ad)

        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serializer.data
            )
        )


class VisitCardView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def _is_asoud_app_request(self, request):
        """
        تشخیص درخواست از اپ آسود بر اساس User-Agent و headers
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # بررسی User-Agent patterns مخصوص اپ آسود
        asoud_patterns = [
            r'asoud',
            r'flutter',
            r'dart',
            r'http\/\d\.\d',  # Dart HTTP client pattern
            r'okhttp',        # OkHttp used by Flutter
        ]
        
        for pattern in asoud_patterns:
            if re.search(pattern, user_agent):
                return True
        
        # بررسی custom headers که اپ میتونه بفرسته
        asoud_headers = [
            'HTTP_X_ASOUD_APP',
            'HTTP_X_FLUTTER_APP',
            'HTTP_X_MOBILE_APP',
        ]
        
        for header in asoud_headers:
            if request.META.get(header):
                return True
        
        # بررسی Accept header - اگر فقط JSON میخاد
        accept_header = request.META.get('HTTP_ACCEPT', '')
        if 'application/json' in accept_header and 'text/html' not in accept_header:
            return True
            
        return False

    def _is_web_browser_request(self, request):
        """
        تشخیص درخواست از مرورگر وب
        """
        user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
        
        # Browser patterns
        browser_patterns = [
            r'mozilla',
            r'chrome',
            r'safari',
            r'firefox',
            r'edge',
            r'opera',
            r'webkit',
        ]
        
        for pattern in browser_patterns:
            if re.search(pattern, user_agent):
                return True
        
        # بررسی Accept header - اگر HTML قبول میکنه
        accept_header = request.META.get('HTTP_ACCEPT', '')
        if 'text/html' in accept_header:
            return True
            
        return False

    def get(self, request, business_id):
        try:
            # پیدا کردن market با business_id
            market = Market.objects.get(business_id=business_id)
            
            # تشخیص نوع client
            is_asoud_app = self._is_asoud_app_request(request)
            is_web_browser = self._is_web_browser_request(request)
            
            # اگر از اپ آسود میاد، JSON برگردون
            if is_asoud_app and not is_web_browser:
                serializer = MarketDetailSerializer(market)
                return Response(
                    ApiResponse(
                        success=True,
                        code=200,
                        data=serializer.data
                    )
                )
            
            # اگر از مرورگر میاد، HTML template برگردون
            elif is_web_browser:
                context = {
                    'market': market,
                    'business_id': business_id,
                    'page_title': f'{market.name} - کارت ویزیت دیجیتال',
                }
                return render(request, 'business_card.html', context)
            
            # پیش‌فرض: JSON برای درخواست‌های نامشخص
            else:
                serializer = MarketDetailSerializer(market)
                return Response(
                    ApiResponse(
                        success=True,
                        code=200,
                        data=serializer.data
                    )
                )
        
        except Market.DoesNotExist:
            # اگر market پیدا نشد
            if self._is_web_browser_request(request):
                # برای مرورگر، یک صفحه 404 زیبا
                context = {
                    'error_message': 'فروشگاه مورد نظر یافت نشد',
                    'business_id': business_id,
                }
                return render(request, 'business_card_404.html', context, status=404)
            else:
                # برای اپ، JSON error
                return Response(
                    ApiResponse(
                        success=False,
                        code=404,
                        error="Business not found"
                    ),
                    status=status.HTTP_404_NOT_FOUND
                )
        
        except Exception as e:
            # خطای سرور
            if self._is_web_browser_request(request):
                # برای مرورگر، صفحه خطای زیبا
                context = {
                    'error_message': 'خطایی در سرور رخ داده است',
                    'business_id': business_id,
                }
                return render(request, 'business_card_error.html', context, status=500)
            else:
                # برای اپ، JSON error
                return Response(
                    ApiResponse(
                        success=False,
                        code=500,
                        error=str(e)
                    ),
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        

class BankCardView(views.APIView):
    # permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            bank_info = UserBankInfo.objects.get(id=pk)

            serializer = UserBankInfoListSerializer(bank_info)

            return Response(
                ApiResponse(
                    success=True,
                    code=200,
                    data=serializer.data
                )
            )
        
        except Exception as e:
            return Response(
                ApiResponse(
                    success=False,
                    code=500,
                    error=str(e)
                )
            )
