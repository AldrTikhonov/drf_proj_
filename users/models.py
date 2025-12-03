from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course, Lesson

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None

    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35, **NULLABLE, verbose_name="Телефон", help_text="Укажите телефон"
    )
    city = models.CharField(
        max_length=150, **NULLABLE, verbose_name="Город", help_text="Укажите город"
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        **NULLABLE,
        verbose_name="Аватар",
        help_text="Загрузите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payments(models.Model):
    METHOD_CHOICES = [
        ("CASH", "Наличные"),
        ("BANK_TRANSFER", "Перевод"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        help_text="Укажите пользователя",
    )
    date = models.DateField(
        auto_now=True, verbose_name="Дата платежа", help_text="Укажите дату платежа"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="paid_course",
        **NULLABLE,
        verbose_name="Оплаченный курс",
        help_text="Укажите оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="paid_lesson",
        **NULLABLE,
        verbose_name="Оплаченный урок",
        help_text="Укажите оплаченный урок",
    )
    amount = models.IntegerField(
        verbose_name="Сумма платежа", help_text="Укажите сумму платежа"
    )
    payment_method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        verbose_name="метод платежа",
        help_text="Укажите метод платежа",
    )
    session_id_course = models.CharField(
        max_length=300,
        **NULLABLE,
        verbose_name="id сессии курса",
        help_text="Введите id курса",
    )
    link_course = models.URLField(
        max_length=500,
        **NULLABLE,
        verbose_name="Ссылка на оплату курса",
        help_text="Укажите ссылку на оплату курса",
    )
    session_id_lesson = models.CharField(
        max_length=300,
        **NULLABLE,
        verbose_name="id сессии урока",
        help_text="Введите id урока",
    )
    link_lesson = models.URLField(
        max_length=500,
        **NULLABLE,
        verbose_name="Ссылка на оплату урока",
        help_text="Укажите ссылку на оплату урока",
    )

    def __str__(self):
        return f"{self.user.email} - {self.amount} ₽ - {self.date}"

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
