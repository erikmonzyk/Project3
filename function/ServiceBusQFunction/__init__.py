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
  
    DbConnection = psycopg2.connect(dbname="techconfdb", user="erikmonzyk@migrationudacity", password="Carson2013$$", host="project3server.postgres.database.azure.com")
    
    try:
        cursor = DbConnection.cursor()
        cursor.execute("SELECT message,subject FROM notification WHERE id=%s;",(notification_id,))
        messagePlain, subject = cursor.fetchone()

        # TODO: Get attendees email and name

        cursor.execute("SELECT email, first_name FROM attendee;")
        attendees = cursor.fetchall()

        # Loop through attendees

        for attendee in attendees:
            CustomMessage = Mail(
                from_email='from_email@techconf.com',
                to_emails=attendee[0],
                subject='{}: {}'.format(attendee[1], subject),
                html_content=messagePlain)

            try:
                SendGrid = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                email = SendGrid.send(message)
                print(email.status_code)
                print(email.body)
                print(email.headers)

            except (Exception, psycopg2.DatabaseError) as error:
                    logging.error(error)


        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        all_attendees = 'Notified {} attendees'.format(len(attendees))
        cursor.execute("UPDATE notification SET status = %s WHERE id=%s;", (all_attendees,notification_id))
        DbConnection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
    finally:
        DbConnection.close()