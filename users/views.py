import generics
from django_filters.rest_framework import DjangoFilterBackend
from requests import Response
from rest_framework import viewsets, generics, permissions, status
from rest_framework import filters

from lms.models import Course, Lesson
from .models import Payment, Users
from .serializers import PaymentSerializer, UserSerializer
from rest_framework.generics import CreateAPIView

from .utils import create_product_course, create_price, create_product_lesson, create_checkout_session


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

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        global price, product_price
        product_type = serializer.validated_data['product_type']
        product_id = serializer.validated_data['product_id']
        if product_type == 'course':
            product = Course.objects.get(id=product_id)
            product_title = product.title
            product_price = product.price
            stripe_product = create_product_course(product_title)
            price = create_price(stripe_product.id, product_price)

            product.stripe_price_id = price.id
            product.save()

        elif product_type == 'lesson':
            product = Lesson.objects.get(id=product_id)
            product_title = product.title
            product_price = product.price
            stripe_product = create_product_lesson(product_title)
            price = create_price(stripe_product.id, product_price)

            product.stripe_price_id = price.id
            product.save()

        session = create_checkout_session(price.id)

        payment = serializer.save(
            user=self.request.user,
            amount=product_price,
            session_id=session.id,
            payment_link=session.url)

        return Response({'checkout_url': session.url,'payment_id': payment.id}, status=status.HTTP_201_CREATED)
