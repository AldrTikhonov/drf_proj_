import re

from rest_framework.serializers import ValidationError


def validate_youtube_link(value):
    """ Функция для проверки ссылок. """
    youtube_pattern = re.compile(r"^https?://(ww\.)?youtube\.com/.*$")
    if not youtube_pattern.match(value):
        raise ValidationError("Можно прикрепить только ссылки на YouTube.")


class YouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if "youtube.com" not in value:
            raise ValidationError(f"Поле {self.field} должно содержать ссылку на YouTube.")
