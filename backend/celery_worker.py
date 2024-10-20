# celery_worker.py
from celery import Celery
from app import create_app
import yfinance
from models import Alert, User
from utils import send_email_alert
import datetime
from celery.schedules import crontab
from extensions import cache


app = create_app()

celery = Celery(app.import_name, broker='redis://redis:6379/1',beat_schedule = {
    'fetch_stock_data_every_minute': {
        'task': 'celery_worker.check_alerts',
        'schedule': crontab(hour="9-16",day_of_week="mon-fri"),
    },
    'clear_price_cache': {
        'task': 'celery_worker.clear_cache',
        'schedule': crontab(hour="9",minute="15",day_of_week="mon-fri"),
    },
})

celery.conf.update(app.config)



@celery.task
def check_alerts():
    app = create_app()
    with app.app_context():
        alerts = Alert.query.all()
        for alert in alerts:
            user = User.query.get(alert.user_id)
            ticker = yfinance.Ticker(alert.stock_symbol)
            price = ticker.history(start=datetime.datetime.utcnow()-datetime.timedelta(minutes=1),period="1m")
            current_price = price['Close'][-1]
            if alert.alert_type == "above" and current_price > alert.price_threshold:
                send_email_alert(user.email, alert.stock_symbol, current_price, alert.price_threshold)
            elif alert.alert_type == "below" and current_price < alert.price_threshold:
                send_email_alert(user.email, alert.stock_symbol, current_price, alert.price_threshold)


@celery.task
def clear_cache():
    app = create_app()
    with app.app_context():
        cache.clear()


if __name__ == '__main__':
    celery.start()

