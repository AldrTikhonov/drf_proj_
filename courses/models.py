from django.conf import settings
from django.db import models

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название курса", help_text="Укажите название курса"
    )
    image = models.ImageField(
        upload_to="courses/image",
        **NULLABLE,
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание", help_text="Опишите курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="Владелец",
        help_text="Укажите владельца",
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"
        ordering = ["name"]


class Lesson(models.Model):
    title = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Укажите название урока"
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        verbose_name="Курс",
        help_text="Укажите название курса",
    )
    image = models.ImageField(
        upload_to="courses/image",
        **NULLABLE,
        verbose_name="Картинка",
        help_text="Загрузите картинку",
    )
    description = models.TextField(
        **NULLABLE, verbose_name="Описание", help_text="Опишите урок"
    )
    video_url = models.URLField(
        **NULLABLE, verbose_name="Ссылка на видео", help_text="Укажите ссылку на видео"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="владелец",
        help_text="Укажите владельца",
    )

    def __str__(self):
        return f"{self.title} ({self.course.name})"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
        ordering = ["title", "course"]


class CourseSubscription(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions"
    )
    course = models.ForeignKey(
        "Course", on_delete=models.CASCADE, related_name="subscriptions"
    )
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} подписан на {self.course.title}"