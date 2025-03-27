from django.views.generic import TemplateView
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from rest_framework import permissions, status
from lms.models import Course, Lesson
from lms.permissions import IsModerator
from lms.serializers import CourseSerializer, LessonSerializer


class HomePageView(TemplateView):
    template_name = "home.html"


class CourseViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["list", "retrieve", "update"]:
            return [permissions.OR(IsModerator(), permissions.IsAuthenticated())]
        return super().get_permissions()

    def get_queryset(self):

        if (
            self.request.user.groups.filter(name="moderators").exists()
            or self.request.user.is_staff
        ):
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)


class LessonViewSet(ModelViewSet):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()

    def get_permissions(self):
        if self.action in ["create", "destroy"]:
            return [permissions.IsAdminUser()]
        elif self.action in ["list", "retrieve", "update"]:
            return [permissions.OR(IsModerator(), permissions.IsAuthenticated())]
        return super().get_permissions()

    def get_queryset(self):
        if (
            self.request.user.groups.filter(name="moderators").exists()
            or self.request.user.is_staff
        ):
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)


class LessonCreateApiView(CreateAPIView):
    serializer_class = LessonSerializer

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class LessonListApiView(ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveApiView(RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonUpdateApiView(UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
