import email
import os
import logging
import azure.functions as func
import psycopg2
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from web.app.models import Attendee, Notification


def main(msg: func.ServiceBusMessage):
    notification_id = (msg.get_body().decode('utf-8'))
    #notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)

    # TODO: Get connection to database

    db = psycopg2.connect(dbname="techconfdb", user="erikmonzyk@project3server", password="Carson2013$$", host="project3server.postgres.database.azure.com")
    cur = db.cursor()
    
    try:
    
        get_msg_subject = cur.execute("SELECT subject, message FROM notification WHERE id = {};".format(notification_id,))

        # TODO: Get attendees email and name
        logging.info('Fetching attendees email and name...')
        cur.execute("SELECT email, first_name FROM attendee;")
        attendees = cur.fetchall()

        # # Loop through attendees
        for attendee in attendees:
            Mail('{}, {}, {}'.format({'john@doe.com'}, {attendee[2]}, {get_msg_subject}))
    
        completed_date = datetime.utcnow()
        
        notify_attendees = "Notified {} attendees".format(len(attendees))
        
        update_notifications = cur.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notify_attendees, completed_date, notification_id))
        db.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        db.rollback()
        
    finally:
        cur.close()
        db.close()
        
#SendGrid Email brought over from routes.py        
        
def send_email(email, subject, body):
    if not app.config.get('SENDGRID_API_KEY')
        message = Mail(
            from_email=app.config.get('ADMIN_EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)

        sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
        sg.send(message)
