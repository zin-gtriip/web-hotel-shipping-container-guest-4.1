from django.apps import AppConfig
from core.mixins import DependentAppConfigMixin


class RegistrationOcrRequired(AppConfig):
    name            = 'registration_ocr_required'
    dependencies    = [
        'guest_facing.registration',
    ]
