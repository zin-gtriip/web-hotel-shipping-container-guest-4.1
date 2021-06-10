from django.apps                import AppConfig
from guest_facing.core.mixins   import DependentAppConfigMixin


class ChatConfig(DependentAppConfigMixin, AppConfig):
    name            = 'guest_facing.chat'
    dependencies    = [
        'guest_facing.core',
    ]
