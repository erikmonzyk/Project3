import logging
import azure.functions as func
import psycopg2
import os
from datetime import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def main(msg: func.ServiceBusMessage):

    notification_id = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s',notification_id)

    # TODO: Get connection to database
  
    connection = psycopg2.connect(dbname="techconfdb", user="erikmonzyk@migrationudacity", password="Carson2013$$", host="project3server.postgres.database.azure.com")
    cursor = connection.cursor()
    try:
        #cursor = connection.cursor()
        notification_search = cursor.execute("SELECT message,subject FROM notification WHERE id=%s;",(notification_id,))
        #messagePlain, subject = cursor.fetchone()

        # TODO: Get attendees email and name

        cursor.execute("SELECT email, first_name FROM attendee;")
        attendees = cursor.fetchall()

        # Loop through attendees

        for attendee in attendees:
                    Mail('{}, {}, {}'.format({'erikmonzyk@techconf.com'}, {attendee[2]}, {notification_search}))

        notification_completed_date = datetime.utcnow
        
        notification_status = 'Notified {} attendees'.format(len(attendees))
         
        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        all_attendees = 'Notified {} attendees'.format(len(attendees))
        #cursor.execute("UPDATE notification SET status = %s WHERE id=%s;", (all_attendees,notification_id))
        update_query = cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notification_status, notification_completed_date, notification_id))
        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        connection.rollback()
    finally:
        connection.close()