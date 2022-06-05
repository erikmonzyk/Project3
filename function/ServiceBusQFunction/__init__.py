import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
def main(msg: func.ServiceBusMessage):

    # notification_id_int = int(msg.get_body().decode('utf-8'))
    #print('notification_id: {} enqueued to queue: {}'.format(msg.get_body().decode('utf-8')))
    
    notification_id = (msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database

    db = psycopg2.connect(host="project3server.postgres.database.azure.com", dbname="techconfdb", user="erikmonzyk@project3server", password="Carson2013$$")
    cursor = db.cursor()
    
    
    try:
    
        notification_query = cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))

        rows = cursor.fetchall()
        # rows = rows [0]
        # subject = str(rows[0])
        # body = str(rows[1])
        
        # TODO: Get attendees email and name
        logging.info('Fetching attendees email and name...')
        attendees = cursor.execute("SELECT email, first_name FROM attendee;")
        attendees = cursor.fetchall()

        # # Loop through attendees
        # logging.info('Sending email to attendees')
        for attendee in attendees:
              Mail('{}, {}, {}'.format({'xxxx@xxxx.com'}, {attendee[2]}, {notification_query}))

          
        new_completed_date = datetime.utcnow()
        status = 'Notified {} attendees, via email'.format(len(attendees))
                
        cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(status, new_completed_date, notification_id))
        db.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        db.rollback()
        
    finally:
        cursor.close()
        db.close()
        

