from django.apps    import AppConfig
from guest_base     import mixins as GuestBaseMixins

class PreArrivalConfig(GuestBaseMixins.DependentAppConfigMixin, AppConfig):
    name            = 'pre_arrival'
    dependencies    = [
        'guest_base.apps.GuestBaseConfig',
    ]