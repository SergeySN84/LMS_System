import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_video_url(value):
    """
    Проверяет, что ссылка ведёт только на youtube.com или youtu.be
    """
    if value:
        youtube_regex = r"^(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/).+$"
        if not re.match(youtube_regex, value):
            raise ValidationError(
                _("Ссылка на видео должна вести только на YouTube."),
                code="invalid_video_url",
            )
