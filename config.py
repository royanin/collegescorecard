from instances import ENV_VAR
import os
basedir = os.path.abspath(os.path.dirname(__file__))
print basedir

CSRF_ENABLED = True
SECRET_KEY = ENV_VAR['CSRF_KEY']    #CSRF secret -- this should be as protected as the email password mentioned below

#db = SQLAlchemy(server)
#con=db.engine.connect().connection

SQLALCHEMY_TRACK_MODIFICATIONS = False
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@localhost/{}'.format(ENV_VAR['DB_USER'],ENV_VAR['PASSWD'],ENV_VAR['DB_1'])
SQLALCHEMY_BINDS = {
    'message':      'mysql://{}:{}@localhost/{}'.format(ENV_VAR['DB_USER'],ENV_VAR['PASSWD'],ENV_VAR['DB_2'])
    #'message' : 'sqlite:///' + os.path.join(basedir, 'app_data.db')
}
"""

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data/app.db')
SQLALCHEMY_BINDS = {
    'email':        'sqlite:///' + os.path.join(basedir, 'data/app_data.db'),
    'message':        'sqlite:///' + os.path.join(basedir, 'data/app_data.db'),    
    #'appmeta':      'sqlite:////path/to/appmeta.db'
}
"""
# mail server settings
MAIL_SERVER = ENV_VAR['MAIL_SERVER']  
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME =  ENV_VAR['MAIL_USERNAME']   #If running locally, change this to your Gmail, in ''
MAIL_PASSWORD =  ENV_VAR['MAIL_PASSWORD']    #The password goes of the above email account, in ''

# administrator list
ADMINS = [MAIL_USERNAME]       #Some more email if you want to define
URGENT_EMAIL = ENV_VAR['URGENT_EMAIL']

#Warning level to raise color flag in the numbers panel
WARN_LEVEL = 20.0   #this means that particular number in that school is in the lowest 20 percentile in the category, or missing.

#website name
WSNAME = ENV_VAR['WS_NAME']
CONTACT_RSN_LIST = ['High school student -- searching for college','Parent -- gathering college info for child','Looking to go back to school','Career counselor gathering information','K-12 administrator','College administrator',    'Data analysis/visualization enthusiast','Other']

