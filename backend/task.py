from datetime import datetime as date, timedelta
from workers import celery
from models import db, User, Booking
import smtplib
from flask import current_app as app
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

@celery.on_after_configure.connect
def set_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(30, daily_reminder.s(), name='daily reminder')
    sender.add_periodic_task(30, monthly_reminder.s(), name='monthly reminder')
    sender.add_periodic_task(10.0, just_say_hello.s(), name='add every 10')


def send_mail(message, subject, recipients):
    sender_email = 'appdev2iitm@gmail.com'
    sender_password = 'hhcuxxbztxmsoqnr'
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipients
    msg['Subject'] = subject
    body = message
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipients, msg.as_string())
    server.quit()
    
@celery.task()
def just_say_hello():
    name = "hello"
    print("INSIDE TASK")
    print("Hello {}".format(name))

@celery.task()
def daily_reminder():
    with app.app_context():
        users = User.query.all()
        curr_date = date.utcnow()
        for user in users:
            bookings = Booking.query.filter_by(user_id=user.id).all()
            for booking in bookings:
                last_booking_time = booking.timestamp
                if curr_date - last_booking_time > timedelta(hours=24):
                # send email
                    send_mail("You have not booked a ticket in the last 24 hours. Please book a ticket to continue receiving updates.", "Daily Reminder", user.email)
                else:
                    send_mail("You have booked a ticket in the last 24 hours. Thank you for using our service.", "Daily Reminder", user.email)
                
        

@celery.task()
def monthly_reminder():
    # with app.app_context():  
    with app.app_context():
        users = User.query.all()
        curr_date = date.utcnow()
        for user in users:
            bookings = Booking.query.filter_by(user_id=user.id).all()
            for booking in bookings:
                last_booking_time = booking.timestamp
                if curr_date - last_booking_time > timedelta(days=30):
                    # send email
                    send_mail("You have not booked a ticket in the last 30 days. Please book a ticket to continue receiving updates.", "Monthly Reminder", user.email)
                else:
                    send_mail("You have booked a ticket in the last 30 days. Thank you for using our service.", "Monthly Reminder", user.email)

   
def send_csv_mail(user_id):
    user = User.query.filter_by(id=user_id).first()
    bookings = Booking.query.filter_by(user_id=user_id).all()
    csv = "Booking ID, Show Name, Seats, Total Price, Booking Time\n"
    for booking in bookings:
        csv += f"{booking.id}, {booking.show.name}, {booking.seats}, {booking.total_price}, {booking.booking_time}\n"
    send_mail(csv, "Your Bookings", user.email)



