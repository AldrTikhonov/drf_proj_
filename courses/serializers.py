from rest_framework.fields import SerializerMethodField
from rest_framework import serializers

from courses.models import Course, Lesson
from courses.validators import youtube_pattern


class LessonSerializer(serializers.ModelSerializer):
    video_url = serializers.URLField(validators=[youtube_pattern], read_only=True)
    class Meta:
        model = Lesson
        fields = ["id", "title", "image", "description", "video_url", "course", "owner"]


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"

class CourseDetailSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()

    # lessons = LessonSerializer(many=True, read_only=True)

    def get_lessons_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    class Meta:
        model = Course
        fields = ["id", "name", "image", "description", "owner", "lessons_count"]
