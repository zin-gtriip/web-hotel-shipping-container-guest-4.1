from django.apps                import AppConfig
from guest_facing.core.mixins   import DependentAppConfigMixin


class RegistrationOcrRequired(DependentAppConfigMixin, AppConfig):
    name            = 'guest_facing.registration_ocr_required'
    dependencies    = [
        'guest_facing.registration',
    ]
