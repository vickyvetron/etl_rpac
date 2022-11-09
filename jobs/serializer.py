from rest_framework import serializers
from .models import Company, Corporate, GlobalConfiguration, JobDetail


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class CorporateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Corporate
        fields = ["id", "brand", "email", "no_pods", "company"]

    def to_representation(self, instance):
        data = super(CorporateSerializer, self).to_representation(instance)
        data.update({"company": CompanySerializer(instance.company).data})
        return data

    def create(self, validated_data):
        obj = Corporate.objects.create(brand=validated_data['brand'], email=validated_data['email'], no_pods=validated_data['no_pods'], company=validated_data['company'])
        return obj

class GlobalConfigurationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalConfiguration
        fields = ["optional_fields","required_fields", "corporate"]

    def to_representation(self, instance):
        data = super(GlobalConfigurationsSerializer, self).to_representation(instance)
        data.update({"corporate": CorporateSerializer(instance.corporate).data})
        return data

class JobDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobDetail
        fields = "__all__"

    def to_representation(self, instance):
        data = super(JobDetailsSerializer, self).to_representation(instance)
        data.update({"corporate": CorporateSerializer(instance.corporate).data})
        data.update({"comapany": CompanySerializer(instance.comapany).data})
        return data