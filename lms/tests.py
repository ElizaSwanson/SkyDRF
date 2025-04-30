from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Lesson
from users.models import Users


class CourseAPITestCase(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя с использованием email
        self.user = Users.objects.create_user(
            email="testuser@example.com",
            username="testusername",
            password="password",
            is_staff=True,
        )

        # Создаем тестовый курс
        self.course_data = {
            "title": "Test Course",
            "description": "Test Description",
            "owner": self.user,
        }
        self.course = Course.objects.create(**self.course_data)

        # URL для получения курса и подписки
        self.course_url = reverse("lms:course-detail", args=[self.course.id])
        self.subscription_url = reverse("lms:subscription")

    def test_course_creation(self):
        """Тестирование создания курса"""
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(self.course.title, "Test Course")

    def test_get_course_details(self):
        """Тестирование получения деталей курса"""
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.get(self.course_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Course")
        self.assertEqual(response.data["owner"], self.user.id)


class LessonAPITestCase(APITestCase):

    def setUp(self):
        # Создаем тестового пользователя с использованием email
        self.user = Users.objects.create_user(
            email="testuser@example.com",
            username="testusername",
            password="password",
            is_staff=True,
        )

        self.course = Course.objects.create(
            title="Test Course", description="Test Description", owner=self.user
        )

        # Создаем тестовый урок
        self.lesson_data = {
            "title": "Test Lesson",
            "description": "Test Description",
            "course": self.course,
            "owner": self.user,
        }
        self.lesson = Lesson.objects.create(**self.lesson_data)

        # URL для получения урока
        self.lesson_url = reverse("lms:lesson-detail", args=[self.lesson.id])

    def test_lesson_creation(self):
        """Тестирование создания урока"""
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(self.lesson.title, "Test Lesson")

    def test_get_lesson_details(self):
        """Тестирование получения деталей урока"""
        self.client.login(email="testuser@example.com", password="password")
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Lesson")
        self.assertEqual(response.data["owner"], self.user.id)

