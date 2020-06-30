from rest_framework import serializers
from loan_approval.models import *


class AntiFraudSerializer(serializers.ModelSerializer):
    class Meta:
        # fields = '__all__'
        fields = ('sid', 'ip', 'city')
        model = Anti_Fraud_Yes


class CreditScoreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('loan_ID', 'gender', 'age')
        model = CreditScore
