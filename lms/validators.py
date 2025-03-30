from rest_framework.validators import ValidationError
from urllib.parse import urlparse


def validate_video_link(value):
    users_url = urlparse(value)
    if not (users_url.scheme and users_url.path):
        raise ValidationError("Ссылка некорректна.")

    if ("youtube.com" not in users_url.hostname
        and "youtu.be" not in users_url.hostname):
        raise ValidationError("Разрешены только ссылки на youtube.com.")
