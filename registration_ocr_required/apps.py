from django.apps import AppConfig
from core.mixins import DependentAppConfigMixin


class RegistrationOcrRequired(AppConfig):
    name            = 'registration_ocr_required'
    version         = '1.3.5'
    dependencies    = [
        'registration.apps.RegistrationConfig',
    ]
