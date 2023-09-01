from apscheduler.schedulers.background import BackgroundScheduler
from models import db, FridgeItem, User, Notifications
from datetime import datetime, timedelta
from mail_functions import send_mail
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)


def check_expirations():
    try:
        # Logic to find expired items
        now = datetime.utcnow()
        soon_to_expire = FridgeItem.query.filter(FridgeItem.expiration_date <= (now + timedelta(days=3))).all()

        for item in soon_to_expire:
            owner = User.query.filter_by(id=item.user_id).first()
            if owner:
                message = f"Your {item.item_name} is expiring soon!"

                # Create a notification
                new_notification = Notifications(message=message, user_id=owner.id)
                db.session.add(new_notification)

                # Send an email notification
                send_mail(owner.email, "Expiration Warning", message)

        db.session.commit()
        logging.info("Expiration checks completed successfully.")
    except Exception as e:
        logging.error(f"An error occurred during expiration checks: {e}")


# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_expirations, trigger="interval", seconds=3600)  # runs every hour
scheduler.start()
