import logging
import azure.functions as func
import psycopg2
import os
#from web.app.models import Attendee, Conference, Notification
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id_int = int(msg.get_body().decode('utf-8'))
    #print('notification_id: {} enqueued to queue: {}'.format(msg.get_body().decode('utf-8')))
    
    notification_id = str(msg.get_body().decode('utf-8'))
    completed_date = datetime.utcnow()
    
    logging.info('Here is the completed date:%s', completed_date)
    logging.info('Python ServiceBus queue trigger processed message: %s, %s', notification_id, notification_id_int)

    # TODO: Get connection to database

    db = psycopg2.connect(host="project3server.postgres.database.azure.com", dbname="techconfdb", user="erikmonzyk@project3server", password="Carson2013$$")
    cursor = db.cursor()
    
    
    try:
    
        #cursor.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))

        logging.info('Fetching attendees email and name...')
        cursor.execute("SELECT email, first_name FROM attendee;")
        attendees = cursor.fetchall()

        # # Loop through attendees
        # logging.info('Sending email to attendees')
        # for attendee in attendees:
        #      Mail('{}, {}, {}'.format({'xxxx@xxxx.com'}, {attendee[2]}, {query}))

        #Try different loop 
        # for (email, first_name) in attendees:
        #     mail = Mail(
        #         from_email='erikmonzyk@techconf.com',
        #         to_emails= email,
        #         subject= subject,
        #         plain_text_content= "Hi {}, \n {}".format(first_name, body))
           # try:
            # SENDGRID_API_KEY = os.environ['SENDGRID_API_KEY']
            # send_grid = SendGridAPIClient(SENDGRID_API_KEY)
            # response = send_grid.send(mail)
            # except Exception as e:
            #     logging.error(e)
            
        # new_completed_date = datetime.utcnow()
        status = 'Notified {} attendees'.format(len(attendees))
                
        cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(status, datetime.utcnow(), notification_id))
        db.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        db.rollback()
        
    finally:
        cursor.close()
        db.close()
        

