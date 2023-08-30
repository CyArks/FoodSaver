from apscheduler.schedulers.background import BackgroundScheduler
from your_app.models import db, Fridge, User, Notifications
from datetime import datetime, timedelta
from your_app import your_mail_function  # assume you have a function to send email


def check_expirations():
    # Logic to find expired items
    now = datetime.utcnow()
    soon_to_expire = Fridge.query.filter(Fridge.expiration_date <= (now + timedelta(days=3))).all()

    for item in soon_to_expire:
        owner = User.query.filter_by(id=item.user_id).first()
        if owner:
            message = f"Your {item.item_name} is expiring soon!"
            
            # Create a notification
            new_notification = Notifications(message=message, user_id=owner.id)
            db.session.add(new_notification)

            # Send an email notification (assuming you have this function)
            your_mail_function(owner.email, "Expiration Warning", message)

    db.session.commit()


# Initialize the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(func=check_expirations, trigger="interval", seconds=3600)  # runs every hour
scheduler.start()
