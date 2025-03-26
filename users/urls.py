from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .apps import UsersConfig
from .views import PaymentList, UserCreateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

app_name = UsersConfig.name

from users.views import UserCreateAPIView

urlpatterns = [
    path("payments/", PaymentList.as_view(), name="payment-list"),
    path('register/',UserCreateAPIView.as_view(), name= 'register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]



