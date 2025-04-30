from django.urls import path, include
from rest_framework.routers import SimpleRouter, DefaultRouter

from lms.apps import LmsConfig
from lms.views import (CourseViewSet, LessonViewSet, SubscriptionView)

app_name = "lms"

router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"lessons", LessonViewSet, basename="lesson")

urlpatterns = [path("", include(router.urls)),
               path("subscription/", SubscriptionView.as_view(), name="subscription")]

