from rest_framework.exceptions import ValidationError

from materials.constants import ALLOWED_RESOURCES


class URLValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        value = dict(value)['video_url']
        video_resource = value.strip('https://www.').split('/')[0]
        if video_resource not in ALLOWED_RESOURCES:
            raise ValidationError("Do not use prohibited hosts!!!")
