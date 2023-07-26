from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ModifiedTrackingAnalyzerAppConfig(AppConfig):
    name = 'modified_tracking_analyzer'
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = _('Django Tracking Analyzer')

    def ready(self):
        # pylint: disable=import-outside-toplevel
        # pylint: disable=unused-import
        from . import conf
