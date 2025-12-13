from rest_framework.serializers import ValidationError


def youtube_pattern(value):
    if not value.startswith("https://www.youtube.com"):
        raise ValidationError("Можно прикреплять только ссылки на YouTube.")