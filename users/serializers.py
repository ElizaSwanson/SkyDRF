from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Payment, Users


class PaymentSerializer(serializers.ModelSerializer):
    product_type = serializers.ChoiceField(choices=[('course', 'Course'), ('lesson', 'Lesson')])
    product_id = serializers.IntegerField()

    class Meta:
        model = Payment
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = "__all__"
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = Users(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user
