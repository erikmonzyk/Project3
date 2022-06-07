import os

app_dir = os.path.abspath(os.path.dirname(__file__))

class BaseConfig:
    DEBUG = True
    POSTGRES_URL = "project3server.postgres.database.azure.com"  #TODO: Update value
    POSTGRES_USER = "erikmonzyk@project3server" #TODO: Update value
    POSTGRES_PW = "Carson2013$$"   #TODO: Update value
    POSTGRES_DB = "techconfdb"   #TODO: Update value
    DB_URL = 'postgresql://{user}:{pw}@{url}/{db}'.format(user=POSTGRES_USER,pw=POSTGRES_PW,url=POSTGRES_URL,db=POSTGRES_DB)
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI') or DB_URL
    CONFERENCE_ID = 1
    SECRET_KEY = 'LWd2tzlprdGHCIPHTd4tp5SBFgDszm'
    SERVICE_BUS_CONNECTION_STRING ='Endpoint=sb://projecthree.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=+ffDTbtzTdMs1rvDkfnyubSUZJ0iwYeELoNOhoeN0G8=' #Update value
    SERVICE_BUS_QUEUE_NAME ='notificationqueue'
    ADMIN_EMAIL_ADDRESS: 'em7272@techcondb.com'
    SENDGRID_API_KEY =  #Configuration not required, required SendGrid Account 'oSueuMzOQsmWxk34GXY1rw'

class DevelopmentConfig(BaseConfig):
    DEBUG = True


class ProductionConfig(BaseConfig):
    DEBUG = False