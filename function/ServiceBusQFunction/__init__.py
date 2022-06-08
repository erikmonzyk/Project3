import logging
import azure.functions as func
import psycopg2
import os
#from web.app.models import Attendee, Conference, Notification
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %d',notification_id)

    # TODO: Get connection to database

    db = psycopg2.connect(host="project3server.postgres.database.azure.com", dbname="techconfdb", user="erikmonzyk@project3server", password="Carson2013$$")
    cur = db.cursor()
    
    
    try:
        
        query =  cur.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id,))
        # attendees = cur.fetchall()
        
        
        # TODO: Get attendees email and name
        logging.info('Fetching attendees email and name...')
        cur.execute("SELECT first_name, email FROM attendee;")
        
        attendees = cur.fetchall()
        logging.info('Made it past the attendees fetchall...')
        # # Loop through attendees
        logging.info('Sending email to attendees', attendees, query)
        
        for attendee in attendees:
            logging.info('THE VALUES FOR ATTENDEE AND QUERY:', attendee, query)
            #Mail('{}, {}, {}'.format({'xxxx@xxxx.com'}, {attendee[2]}, {query}))

        
        
            status = 'Notified {} attendees'.format(len(attendees))
            notification_completed_date = datetime.utcnow()
            cur.execute('UPDATE notification SET status= ?, completed_date=? WHERE id=?', (status, notification_completed_date, notification_id))
            db.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        db.rollback()
        
    finally:
        cur.close()
        db.close()
        

