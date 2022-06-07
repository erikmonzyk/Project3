import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

        notification_id =str(msg.get_body().decode('utf-8'))
        logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)
        

        # TODO: Get connection to database

        connection = psycopg2.connect(host="project3server.postgres.database.azure.com", dbname="techconfdb", user="erikmonzyk@project3server", password="Carson2013$$")
        
        cur = connection.cursor()
        
        try:
    
            # Get notification message and subject from database using the notification_id
            logging.info('Fetching notification message and subject...')
            notification_query = cur.execute("SELECT message, subject FROM notification WHERE id = {};".format(notification_id))

            logging.info('Fetching attendees email and name...')
            cur.execute("SELECT email, first_name FROM attendee;")
            attendees = cur.fetchall()
            
            # Loop through each attendee and send an email with a personalized subject
            logging.info('Sending emails...')
            for attendee in attendees:
                Mail('{}, {}, {}'.format({'john@doe.com'}, {attendee[2]}, {notification_query}))
            
                #Update notification table by setting completed_date
                completed_date = datetime.utcnow()
                #total_attendees = len(attendees)
                logging.info('Updating notifications...')
                notification_status = 'Notified {} attendees'.format(len(attendees))
                update_query = cur.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notification_status, completed_date, notification_id))
                connection.commit()

        except (Exception, psycopg2.DatabaseError) as error:
                logging.error(error)
                connection.rollback()
            
        finally:
            cur.close()
            connection.close()
        

