from rest_framework import viewsets
from rest_framework import filters
from tutorial.quickstart.serializers import UserSerializer

from .models import Payment, Users
from .serializers import PaymentSerializer
from rest_framework.generics import CreateAPIView

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
    queryset = Users.objects.all()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()
