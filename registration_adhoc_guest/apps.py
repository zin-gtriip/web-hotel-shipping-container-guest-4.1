from django.apps import AppConfig
from core.mixins import DependentAppConfigMixin


class RegistrationAdhocGuestConfig(AppConfig):
    name            = 'registration_adhoc_guest'
    version         = '1.3.4'
    dependencies    = [
        'registration.apps.RegistrationConfig',
        'registration_ocr_required.apps.RegistrationOcrRequiredConfig',
    ]
