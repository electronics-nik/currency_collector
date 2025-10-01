from celery import Celery
from celery.schedules import crontab

from main import go_collect

app = Celery(
    "celery_app",
    broker="redis://broker:6379/0",
    backend="redis://broker:6379/1"
)

@app.task
def collector():
    go_collect()
    print("🔥 Task is done!")

app.conf.beat_schedule = {
    "run-collector-job": {
        "task": "celery_app.collector",
        # "schedule": crontab(hour="*/3"),  # каждые три часа
        # "schedule": crontab(minute="*/1"),  # каждую минуту
        "schedule": crontab(hour='6,12,18', minute=0),
    },
}
app.conf.timezone = "UTC"
