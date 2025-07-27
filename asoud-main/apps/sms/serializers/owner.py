import json
from rest_framework import serializers
from apps.sms.models import (
    Line, 
    Template,
    BulkSms,
    PatternSms
)


class LineListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    
    class Meta:
        model = Line
        fields = ['id', 'number', 'estimated_cost']

class TemplateListSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Template
        fields = ['id', 'template_id', 'content', 'variables']

class BulkSmsCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    cost = serializers.FloatField(required=False)
    actual_cost = serializers.FloatField(required=False)
    status = serializers.CharField(required=False)
    packId = serializers.CharField(required=False)
    
    class Meta:
        model = BulkSms
        exclude = ['user', 'message_ids']

class BulkSmsViewSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = BulkSms
        fields = [
            'id',
            'line', 
            'content',
            'to'
        ]

class PatternSmsCreateSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    template = serializers.UUIDField()
    cost = serializers.FloatField(required=False)
    actual_cost = serializers.FloatField(required=False)
    variables = serializers.JSONField(required=True)

    class Meta:
        model = PatternSms
        exclude = ['user', 'message_id']

    def to_payload(self, validated_data: dict):
        try:
            template = Template.objects.get(id=validated_data['template'])
        except Template.DoesNotExist:
            raise Exception('Template Not Found')
        
        # check variables required for the template
        variables = template.variables
        needed_variables = list( variables.keys() )
        input_variables = [v['name'] for v in validated_data['variables']]

        if len(needed_variables) != len(input_variables):
            raise Exception('Extra/Less Variables Received')
        
        errors = {}
        for v in needed_variables:
            if v not in input_variables:
                errors['v'] = "Not Provided"

        if errors:
            raise Exception(json.dumps(errors))
        
        # for v in validated_data['variables']:
        #     v['name'] = v['name'].upper()
        
        return [
            {
                "Mobile": mobile,
                "TemplateId": int(template.template_id),
                "Parameters": validated_data['variables']
            }  
            for mobile in validated_data['to']
        ]

class PatternSmsviewSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    class Meta:
        model = BulkSms
        fields = [
            'id',
            'template', 
            'to'
        ]



class SmsListSerializer(serializers.ModelSerializer):
    pass

class smsHistorySerializer(serializers.ModelSerializer):
    pass