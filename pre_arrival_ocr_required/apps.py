from django.apps import AppConfig
from core.mixins import DependentAppConfigMixin


class PreArrivalOcrRequired(AppConfig):
    name            = 'pre_arrival_ocr_required'
    version         = '1.3.4'
    dependencies    = [
        'pre_arrival.apps.PreArrivalConfig',
    ]
