from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

from .tasks import delete_temp_images


def configure_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore())

    # add the deletion job to run daily at a 12:00 AM
    scheduler.add_job(delete_temp_images, 'cron', year=2023, hour=0, minute=0)

    # register the scheduler with djangos event system
    register_events(scheduler)

    # start scheduler
    scheduler.start()