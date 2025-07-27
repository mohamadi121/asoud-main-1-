from rest_framework import views, status, permissions
from rest_framework.response import Response
from utils.response import ApiResponse
from apps.advertise.serializers import (
    AdvertiseSerializer,
    AdvertiseCreateSerializer,
    AdvertiseListSerializer,
)
from apps.advertise.models import (
    Advertisement,
    AdvImage,
    AdvKeyword
)
from apps.advertise.core import AdvertisementCore

# Create your views here.

class AdvertiseCreateView(views.APIView):
    def post(self, request):
        try:
            serialized_data = AdvertisementCore.create_advertisement(request)

            return Response(
                ApiResponse(
                    success=True,
                    code=201,
                    data=serialized_data
                ),
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                ApiResponse(
                    success=False,
                    code=500,
                    error=str(e)
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class AdvertiseListView(views.APIView):
    def get(self, request):
        advertises = Advertisement.objects.filter(is_paid=True)

        if q := request.GET.get('q'):
            advertises = advertises.filter(name_icontain=q)
        
        if type := request.GET.get('type'):
            advertises = advertises.filter(type=type)

        if state := request.GET.get('state'):
            advertises = advertises.filter(state=state)
        
        if price_gt := request.GET.get('price_gt'):
            advertises = advertises.filter(price__gte=price_gt)

        if price_lt := request.GET.get('price_lt'):
            advertises = advertises.filter(price__lte=price_lt)

        serializer = AdvertiseListSerializer(advertises, many=True)

        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serializer.data
            )
        )

class AdvertiseDetailView(views.APIView):
    def get(self, request, pk):
        try:
            advertise = Advertisement.objects.get(id=pk)
        except Advertisement.DoesNotExist:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Advertisement Not Found"
                ),
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = AdvertiseSerializer(advertise)

        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serializer.data
            )
        )

class AdvertiseOwnListView(views.APIView):
    def get(self, request):
        advertises = Advertisement.objects.filter(user=request.user)
        
        serializer = AdvertiseListSerializer(advertises, many=True)

        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serializer.data
            )
        )

class AdvertiseUpdateView(views.APIView):
    def put(self, request, pk):
        try:
            advertise = Advertisement.objects.get(id=pk)
        except Advertisement.DoesNotExist:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Advertisement Not Found"
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        # remove extra fields from request before going to serializer
        data = [request.data.pop(key) for key in list(request.data.keys()) if key in ['product']]
        
        serializer = AdvertiseCreateSerializer(advertise, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        obj = serializer.save()

        serialized_data = AdvertiseSerializer(obj).data

        return Response(
            ApiResponse(
                success=True,
                code=200,
                data=serialized_data
            )
        )

class AdvertiseDeleteView(views.APIView):
    def delete(self, request, pk):
        try:
            advertise = Advertisement.objects.get(id=pk)
        except Advertisement.DoesNotExist:
            return Response(
                ApiResponse(
                    success=False,
                    code=404,
                    error="Advertisement Not Found"
                ),
                status=status.HTTP_404_NOT_FOUND
            )

        if advertise.user != request.user:
            return Response(
                ApiResponse(
                    success=False,
                    code=403,
                    error="UnAuthorized"
                ),
                status=status.HTTP_403_FORBIDDEN
            )

        advertise.delete()

        return Response(
            ApiResponse(
                success=True,
                code=204,
            ),
            status=status.HTTP_204_NO_CONTENT
        )

class AdvertisePaymentView(views.APIView):
    def get(self, request):
        adv_id = request.GET.get('advertisement')

        if not adv_id:
            return # redirect

        try:
            advertise = Advertisement.objects.get(id=adv_id)
        except Advertisement.DoesNotExist:
            return # redirect
        
        # the rest

