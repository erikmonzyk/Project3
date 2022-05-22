import os
import logging
import azure.functions as func
import psycopg2
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):
    try: 
        notification_id = int(msg.get_body().decode('utf-8'))
        logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

        # TODO: Get connection to database
    
        DbConnection = psycopg2.connect(dbname="techconfdb", user="erikmonzyk@migrationudacity", password="Carson2013$$", host="project3server.postgres.database.azure.com")
                
        with DbConnection.cursor() as cur:
            
            notification = cur.execute("SELECT message, subject FROM public.notification WHERE id = %s", (notification_id,))
            
            # TODO: Get attendees email and name

            cur.execute("SELECT email, first_name FROM attendee;")
            attendees = cur.fetchall()

            # # Loop through attendees

            # for attendee in attendees:
            #             Mail('{}, {}, {}'.format({'erikmonzyk@techconf.com'}, {attendee[2]}, {notification_search}))

            notification_completed_date = datetime.utcnow
            CountOfAttendees = len(attendees)
            cur.execute("UPDATE public.notification SET completed_date = %s, status = %s WHERE id = %s", (notification_completed_date, 'Notified {} attendees'.format(CountOfAttendees), notification_id,))
            
            DbConnection.commit()
            DbConnection.close()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        DbConnection.rollback()
    finally:
        DbConnection.close()
        

def send_email(email, subject, body):
    if not app.config.get('SENDGRID_API_KEY'):
        message = Mail(
            from_email=app.config.get('ADMIN_EMAIL_ADDRESS'),
            to_emails=email,
            subject=subject,
            plain_text_content=body)
        sg = SendGridAPIClient(app.config.get('SENDGRID_API_KEY'))
        sg.send(message)