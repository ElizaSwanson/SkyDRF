from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Course, Subscription, Lesson
from users.models import Users


class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.user = Users.objects.create_user(
            email='testemail@mail.ru',
            username='test2',
            password='testpassword2',
            is_staff=True)

        # Создаем тестовый курс
        self.course_data = {'title': 'Course2',
            'description': 'Desc',
            'owner': self.user}
        self.course = Course.objects.create(**self.course_data)
        self.course_url = reverse('lms:course-detail', args=[self.course.id])
        self.subscription_url = reverse('lms:subscription')

    def test_course_creation(self):
        self.assertEqual(Course.objects.count(), 1)
        self.assertEqual(self.course.title, 'Course2')

    def test_get_course_details(self):
        self.client.login(email='testemail@mail.ru', password='testpassword2')
        response = self.client.get(self.course_url)
        self.assertEqual(response.data['title'], self.course_data.title)
        self.assertEqual(response.data['owner'], self.user.id)

    def test_create_subscription(self):
        self.client.login(email='testemail@mail.ru', password='testpassword2')
        response = self.client.post(self.subscription_url, {
            'course_id': self.course.id,
            'username': 'test2'})
        self.assertEqual(response.data['message'], "Подписка добавлена")


class LessonAPITestCase(APITestCase):
    def setUp(self):
        self.user = Users.objects.create_user(
            email='testemail@mail.ru',
            username='test2',
            password='testpassword2',
            is_staff=True)

        self.course = Course.objects.create(
            title='Test3',
            description='Test3',
            owner=self.user
        )

        # Создаем тестовый урок
        self.lesson_data = {
            'title': 'Lesson1',
            'description': 'lesson1',
            'course': self.course,
            'owner': self.user
        }
        self.lesson = Lesson.objects.create(**self.lesson_data)

        self.lesson_url = reverse('lms:lesson-detail', args=[self.lesson.id])

    def test_lesson_creation(self):
        self.assertEqual(Lesson.objects.count(), 1)
        self.assertEqual(self.lesson.title, self.lesson_data['title'])

    def test_get_lesson_details(self):
        self.client.login(email='testemail@mail.ru', password='testpassword2')
        response = self.client.get(self.lesson_url)
        self.assertEqual(response.data['title'], 'Lesson1')
        self.assertEqual(response.data['owner'], self.user.id)

