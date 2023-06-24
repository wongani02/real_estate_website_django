import pytz
from apscheduler.schedulers.background import BackgroundScheduler

from .tasks import update_bookings

dt_africa = pytz.timezone('Africa/Maputo')

#this fuction will trigger the tasks every day at exactly 15:00
def start():
    scheduler = BackgroundScheduler(timezone=dt_africa)
    scheduler.add_job(update_bookings, trigger='cron', hour='15',minute='00')
    scheduler.start()
    