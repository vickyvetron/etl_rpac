from rest_framework import serializers
from .models import Company, Corporate, GlobalConfiguration


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CorporateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporate
        fields = ["id", "brand", "email", "no_pods", "company"]

    def create(self, validated_data):
        obj = Corporate.objects.create(brand=validated_data['brand'], email=validated_data['email'], no_pods=validated_data['no_pods'], company=validated_data['company'])
        return obj

class GlobalConfigurationsSerializer(serializers.ModelSerializer):
    corporate = CorporateSerializer()
    class Meta:
        model = GlobalConfiguration
        fields = ["optional_fields","required_fields", "corporate"]