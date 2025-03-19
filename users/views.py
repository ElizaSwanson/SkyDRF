import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics
from rest_framework import filters
from tutorial.quickstart.serializers import UserSerializer

from .models import Payment, Users
from .serializers import PaymentSerializer
from rest_framework.generics import CreateAPIView


class PaymentList(generics.ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = (DjangoFilterBackend, filters.OrderingFilter)
    filterset_fields = {
        "paid_course": ["exact"],
        "paid_lesson": ["exact"],
        "payment_method": ["exact"]}
    ordering_fields = ["payment_date"]
    ordering = ["payment_date"]


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
