from rest_framework.serializers import ValidationError


class YouTubeValidator:
    """ Класс-валидатор для проверки ссылок. """
    def __call__(self, value):
        if not value.startswith("https://www.youtube.com"):
            raise ValidationError("Можно прикреплять только ссылки на YouTube.")

    def __fields__(self):
        return ["video_url"]
