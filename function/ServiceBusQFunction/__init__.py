import os
import logging
import azure.functions as func
import psycopg2
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def main(msg: func.ServiceBusMessage):
    notification_id = msg.get_body().decode('utf-8')
    #notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s', notification_id)

    # TODO: Get connection to database

    db = psycopg2.connect(dbname="techconfdb", user="erikmonzyk@project3server", password="Carson2013$$", host="project3server.postgres.database.azure.com")
    
    try:
        cur = db.cursor()
        cur.execute("SELECT subject, message FROM public.notification WHERE id = %s", (notification_id,))
        notification_records = cur.fetchall()
        notification_records = notification_records[0]
        subject = str(notification_records[0])
        email_body = str(notification_records[1])

        # TODO: Get attendees email and name
        cur.execute("SELECT email, first_name FROM attendee;")
        attendees = cur.fetchall()

        # # Loop through attendees
        for attendee in attendees:
            Mail('{}, {}, {}'.format({'erikmonzyk@techconf.com'}, {attendee[2]}, {notification_records}))
            
        notification_completed_date = datetime.utcnow()
        
        count_attendees = "Notified {} attendees".format(len(attendees))
        cur.execute(
            "UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(count_attendees,
                                                                                                 datetime.utcnow(),
                                                                                                 notification_id, ))

        db.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        db.rollback()
    finally:
        cur.close()
        db.close()
