from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from courses.models import Course, CourseSubscription, Lesson
from courses.validators import YouTubeValidator


class LessonSerializer(serializers.ModelSerializer):
    """Сериализатор для уроков."""

    video_url = serializers.URLField(validators=[YouTubeValidator()], read_only=True)

    class Meta:
        model = Lesson
        fields = ["id", "title", "image", "description", "video_url", "course", "owner"]


class CourseSerializer(serializers.ModelSerializer):
    """Сериализатор для курсов."""

    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для просмотра курса."""

    lessons_count = serializers.SerializerMethodField()

    # lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ["id", "name", "image", "description", "owner", "lessons_count"]


class CourseSubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписки на курсы."""

    class Meta:
        model = CourseSubscription
        fields = ["user", "course", "subscribed_at"]
