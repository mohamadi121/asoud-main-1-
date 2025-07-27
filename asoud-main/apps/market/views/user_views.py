from rest_framework import views, status
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _

from utils.response import ApiResponse

from apps.market.models import (
    Market,
    MarketBookmark,
)

from apps.market.serializers.user_serializers import (
    MarketListSerializer,
    MarketReportCreateSerializer,
)


class MarketListAPIView(views.APIView):
    def get(self, request, format=None):
        user_obj = self.request.user

        market_list = Market.objects.filter(
            user=user_obj,
        )

        serializer = MarketListSerializer(
            market_list,
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


class MarketReportAPIView(views.APIView):
    def post(self, request, pk):
        try:
            market = Market.objects.get(id=pk)
        except:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Market Not Found"
                )
            )
        
        user = self.request.user

        serializer = MarketReportCreateSerializer(
            data=request.data,
            context={'request': request},
        )

        if serializer.is_valid(raise_exception=True):
            serializer.save(
                market=market,
                creator=user,
            )

            success_response = ApiResponse(
                success=True,
                code=200,
                data={
                    **serializer.data,
                },
                message='Market report created successfully.',
            )

            return Response(success_response, status=status.HTTP_201_CREATED)

        response = ApiResponse(
            success=False,
            code=500,
            error={
                'code': 'server_error',
                'detail': 'Server error',
            }
        )

        return Response(response, status=status.HTTP_200_OK)


class MarketBookmarkAPIView(views.APIView):
    def post(self, request, pk):
        user = self.request.user
        try:
            market = Market.objects.get(id=pk)
        except:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Market Not Found"
                )
            )
        
        market_bookmark, is_created = MarketBookmark.objects.get_or_create(
            user=user,
            market=market,
        )

        # If the market is already bookmarked by the user
        # Then deactivate the bookmark
        if not is_created:
            if market_bookmark.is_active == False:
                market_bookmark.is_active = True
                market_bookmark.save()

                success_response = ApiResponse(
                    success=True,
                    code=200,
                    data={},
                    message='Market bookmarked successfully.',
                )

                return Response(success_response, status=status.HTTP_201_CREATED)
            
            market_bookmark.is_active = False
            market_bookmark.save()

            response = ApiResponse(
                success=True,
                code=200,
                data={},
                message='Market unbookmarked successfully.',
            )

            return Response(response, status=status.HTTP_200_OK)

        success_response = ApiResponse(
            success=True,
            code=200,
            data={},
            message='Market bookmarked successfully.',
        )

        return Response(success_response, status=status.HTTP_201_CREATED)

    def get(self, request):
        user = self.request.user

        market_bookmark_list = MarketBookmark.objects.filter(
            user=user,
            is_active=True,
        ).select_related('market')

        market_list = [book_mark.market for book_mark in market_bookmark_list]

        serializer = MarketListSerializer(
            market_list,
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
