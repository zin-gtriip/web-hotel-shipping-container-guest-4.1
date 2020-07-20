import os
import datetime
from django_cron                    import CronJobBase, Schedule
from django.conf                    import settings
from django.contrib.sessions.models import Session
from django.utils                   import timezone

class ClearSessionCronJob(CronJobBase):
    """
    Cron job that clears expired session on database after 30 days.

    The timedelta 30 days is to prevent `preload` session is being
    cleared along with `pre_arrival` session which is expired within
    `settings.PRE_ARRIVAL_SESSION_AGE` time.
    
    This job also will clear saved passport image file that saved using
    `session_key` as file name.
    """
    code        = 'pre_arrival.clear_session_cron_job'
    schedule    = Schedule(run_at_times=[settings.CLEAR_SESSION_CRON_JOB_RUN_TIME])

    def do(self):
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now() - datetime.timedelta(days=settings.EXPIRED_SESSION_TIMEDELTA))
        for session in expired_sessions:
            file_name = session.session_key +'.png'
            folder_name = os.path.join(settings.BASE_DIR, 'media', 'ocr')
            if os.path.exists(folder_name):
                saved_file = os.path.join(folder_name, file_name)
                if os.path.exists(saved_file):
                    os.remove(saved_file)
            session.delete()