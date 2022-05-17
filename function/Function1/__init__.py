import logging
from msilib import Binary
import azure.functions as func
import psycopg2
# import psycopg2-Binary
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
  
    DbConnection = psycopg2.connect(dbname="techconfdb", user="erikmonzyk@project3server", password="Carson2013$$", host="project3server.postgres.database.azure.com")
    cursor = DbConnection.cursor()

    try:
        logging.info('Getting notification message and subject.')
        notificationQuery = cursor.execute("SELECT message, subject FROM notification WHERE id={};".format(notification_id)) 
        
        logging.info('Getting all attendees email and names.')
        allAttendees = cursor.execute("SELECT email, first_name, last_name FROM attendee;")
        attendees = cursor.fetchall()
        # Loop through attendees
        
        logging.info('Looping through all attendees and sending emails.')
        for attendee in allAttendees:
            Mail('{}, {}, {}'.format({'admin@techconf.com'},{attendee[2]},{notificationQuery}))
            
        notification_completed_date = datetime.utcnow()
        notification_status = 'Notified {} attendee'.format(len(allAttendees))
        
        #   CustomMessage=Mail(from_email='admin@techconf.com',
        #                      to_emails=attendee[0],
        #                      subject='conference notification'.format(attendee[1], subject),
        #                      html_content=messagePlain)

  
        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        update_query = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notification_status, notification_completed_date, notification_id))        

        DbConnection.commit()
        logging.info("Notifications have been updated!")

    except (Exception, psycopg2.DatabaseError) as error:
            logging.error(error)
            connection.rollback()
    finally:
        cursor.close()
        DbConnection.close()