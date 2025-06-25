from rest_framework import serializers
from apps.users.models import User, UserBankInfo, BankInfo


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id', 
            'mobile_number'
        ]


class BankInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankInfo
        fields = (
            'id',
            'name',
            'logo'
        )


class UserBankInfoCreateSerializer(serializers.ModelSerializer):
    bank_info = serializers.SerializerMethodField()
    class Meta:
        model = UserBankInfo
        fields = (
            'bank_info',
            'card_number',
            'account_number',
            'iban',
            'full_name',
            'branch_id',
            'branch_name'
        )
    def get_bank_info(self, obj):
        return obj.bank_info.name

class UserBankInfoUpdateSerializer(UserBankInfoCreateSerializer):
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    

class UserBankInfoListSerializer(serializers.ModelSerializer):
    bank_info = serializers.SerializerMethodField()
    class Meta:
        model = UserBankInfo
        fields = '__all__'
    def get_bank_info(self, obj):
        return obj.bank_info.name
