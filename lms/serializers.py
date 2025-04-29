from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    count_lessons_in_course = serializers.SerializerMethodField()
    subscription_to_course = serializers.SerializerMethodField()

    def get_count_lessons_in_course(self, course):
        return Lesson.objects.filter(course=course).count()

    def get_subscription_to_course(self, course):
        return Subscription.objects.filter(course=course).exists()

    class Meta:
        model = Course
        fields = "__all__"