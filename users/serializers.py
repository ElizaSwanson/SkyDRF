from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, Users


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
