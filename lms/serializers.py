from rest_framework import serializers

from .models import Course, Lesson, Subscription
from .validators import validate_video_link


class LessonSerializer(serializers.ModelSerializer):
    lesson_link = serializers.URLField(validators=[validate_video_link])

    class Meta:
        model = Lesson
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)


class CourseSerializer(serializers.ModelSerializer):
    count_of_lessons = serializers.SerializerMethodField()
    info_lessons = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_count_of_lessons(self, obj):
        return obj.lesson_set.count()

    def get_info_lessons(self, obj):
        lessons = obj.lesson_set.all()
        return LessonSerializer(lessons, many=True).data

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return (Subscription.objects.filter(user=user, course=obj).exists() if user.is_authenticated else False)

    class Meta:
        model = Course
        fields = ("title", "description", "preview", "count_of_lessons", "info_lessons")
