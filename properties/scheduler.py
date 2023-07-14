from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import register_events, DjangoJobStore

from .tasks import delete_temp_media, ticket_expiry_notification


def configure_scheduler():
    scheduler = BackgroundScheduler()
    # scheduler.add_jobstore(DjangoJobStore())

    # create job ids
    job1 = 'media'
    job2 = 'tickets'

    # create time values
    seconds = 59
    minutes = 0
    hours = 0

    # add the deletion job to run daily at a 12:00 AM
    scheduler.add_job(delete_temp_media, 'cron', hour=hours, minute=minutes, id=job1)

    # add the e-ticket notification job
    scheduler.add_job(ticket_expiry_notification, 'cron', hour=hours, minute=minutes, id=job2)

    # register the scheduler with djangos event system
    register_events(scheduler)

    # start scheduler
    scheduler.start()
