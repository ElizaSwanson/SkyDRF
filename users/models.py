from datetime import datetime

from django.contrib.auth.models import (AbstractUser, BaseUserManager)
from django.db import models

from lms.models import Course, Lesson


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Введите почту!")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if not extra_fields.get("is_staff"):
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Users(AbstractUser):
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    email = models.EmailField(unique=True, verbose_name="почта")
    phone = models.CharField(max_length=35, verbose_name="телефон", blank=True, null=True)
    avatar = models.ImageField(upload_to="users/avatars", verbose_name="аватар", blank=True, null=True)
    town = models.CharField(max_length=50,verbose_name="город", blank=True, null=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions_set',
        blank=True,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ("BANK_TRANSFER", "Банковский перевод"),
        ("CASH", "Наличными"),
    ]

    owner = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Пользователь")
    payment_date = models.DateField(default=datetime.now, verbose_name="Дата оплаты")
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name="Оплаченный курс", blank=True, null=True)
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, verbose_name="Оплаченный урок", blank=True, null=True)
    amount = models.DecimalField(decimal_places=2, max_digits=20, verbose_name="Сумма")
    type = models.CharField(max_length=50, choices=PAYMENT_CHOICES, verbose_name="Способ оплаты")
    amount = models.DecimalField(max_digits=10, verbose_name="Сумма платежа", decimal_places=2)
    session_id = models.CharField(max_length=100, null=True, blank=True, verbose_name="ID сессии")
    payment_method = models.CharField(max_length=50, choices=PAYMENT_CHOICES, default="BANK TRANSFER", verbose_name="Варианты оплаты")
    payment_link = models.URLField(max_length=400, null=True, blank=True, verbose_name="Ссылка на платеж")

    def __str__(self):
        return f"{self.owner} - {self.get_type_display()} - {self.amount}"
