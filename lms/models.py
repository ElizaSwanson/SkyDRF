from django.db import models

from config import settings


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    description = models.TextField(max_length=250, verbose_name="Описание курса", blank=True, null=True)
    preview = models.ImageField(upload_to="lms/previews", verbose_name="Превью", blank=True, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор курса",
                              related_name="courses", null=True, blank=True)
    price = models.DecimalField(max_digits=10, null=True, blank=True, verbose_name="Цена", decimal_places=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название урока")
    description = models.TextField(max_length=250, verbose_name="Описание урока", blank=True, null=True)
    picture = models.ImageField(upload_to="lms/pictures", verbose_name="Изображение", blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="Курс", related_name="lesson_set")
    video_url = models.URLField(max_length=200, blank=True, null=True, verbose_name="Ссылка на видео")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор урока",
                              related_name="lessons", null=True, blank=True)
    price = models.DecimalField(max_digits=10, null=True, blank=True, verbose_name="Цена", decimal_places=2)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="subscriptions", on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name="subscriptions", on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "course")
