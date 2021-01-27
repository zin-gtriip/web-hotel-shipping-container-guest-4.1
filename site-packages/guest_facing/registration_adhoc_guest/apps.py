from django.apps                import AppConfig
from guest_facing.core.mixins   import DependentAppConfigMixin


class RegistrationAdhocGuestConfig(AppConfig):
    name            = 'registration_adhoc_guest'
    dependencies    = [
        'guest_facing.registration',
        'guest_facing.registration_ocr_required',
    ]
