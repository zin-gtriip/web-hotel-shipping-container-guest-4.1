from django.apps                import AppConfig
from guest_facing.core.mixins   import DependentAppConfigMixin


class RegistrationOcrRequired(AppConfig):
    name            = 'registration_ocr_required'
    dependencies    = [
        'guest_facing.registration',
    ]
