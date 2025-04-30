from django.views.generic import TemplateView
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .paginators import CustomPagination
from .tasks import send_email_task

from rest_framework import permissions, status, viewsets
from lms.models import Course, Lesson, Subscription
from lms.permissions import IsModerator
from lms.serializers import CourseSerializer, LessonSerializer


class HomePageView(TemplateView):
    template_name = "home.html"


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["list", "retrieve", "update"]:
            return [permissions.IsAuthenticated()]

        return super().get_permissions()

    def check_moderator_access(self):
        if not (
            self.request.user.groups.filter(name="moderators").exists()
            or self.request.user.is_staff
        ):
            raise PermissionDenied(
                "У вас недостаточно прав для доступа к этому ресурсу."
            )

    def get_queryset(self):

        self.check_moderator_access()

        if self.request.user.groups.filter(name="moderators").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["list", "retrieve", "update"]:
            return [permissions.IsAuthenticated()]

        return super().get_permissions()

    def check_moderator_access(self):
        if not (
            self.request.user.groups.filter(name="moderators").exists()
            or self.request.user.is_staff
        ):
            raise PermissionDenied(
                "У вас недостаточно прав для доступа к этому ресурсу."
            )

    def get_queryset(self):
        self.check_moderator_access()

        if self.request.user.groups.filter(name="moderators").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(self, request):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)
        subject = "Благодарим за подписку на конал"
        email_message = f"Вы подписались на следующий курс/урок: {course_item.title}."
        message = "Подписка добавлена"

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            send_email_task.delay(user.email, subject, email_message)

        return Response({"message": message})


class CourseUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subscribers = Subscription.objects.filter(course=course_item)
        subject = "Обновление курса"
        email_message = f"Курс {course_item.title} был обновлен."

        for subscription in subscribers:
            send_email_task.delay(subscription.user.email, subject, email_message)

        return Response({"message": "Курс успешно обновлен и уведомления отправлены."})