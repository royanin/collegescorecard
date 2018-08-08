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

#Search settings:
WHOOSH_BASE = os.path.join(basedir, 'whoosh_index')

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

#Maximum number of schools to show in whoosh search
MAX_SEARCH_RESULTS = 15


#website name
WSNAME = ENV_VAR['WS_NAME']
CONTACT_RSN_LIST = ['High school student -- searching for college','Parent -- gathering college info for child','Looking to go back to school','Career counselor gathering information','K-12 administrator','College administrator',    'Data analysis/visualization enthusiast','Other']

subj_dict = {
        'PCIP01' : ('Agriculture, Agriculture Operations, and Related Sciences','247, 202, 201'),
        'PCIP03' : ('Natural Resources and Conservation','247, 120, 107'),
        'PCIP04' : ('Architecture and Related Services','145, 168, 208'),
        'PCIP05' : ('Area, Ethnic, Cultural, Gender, and Group Studies','3, 79, 132'),
        'PCIP09' : ('Communication, Journalism, and Related Programs','152, 221, 222'),
        'PCIP10' : ('Communications Technologies/Technicians and Support Services','136, 176, 75'),
        'PCIP11' : ('Computer and Information Sciences and Support Services','247, 202, 201'),
        'PCIP12' : ('Personal and Culinary Services','146, 168, 209'),
        'PCIP13' : ('Education','181, 101, 167'),
        'PCIP14' : ('Engineering','0, 155, 119'),
        'PCIP15' : ('Engineering Technologies and Engineering-Related Fields','221, 65, 36'),
        'PCIP16' : ('Foreign Languages, Literatures, and Linguistics','214, 80, 118'),
        'PCIP19' : ('Family and Consumer Sciences/Human Sciences','68, 184, 172'),
        'PCIP22' : ('Legal Professions and Studies','239, 192, 80'),
        'PCIP23' : ('English Language and Literature/Letters','91, 94, 166'),
        'PCIP24' : ('Liberal Arts and Sciences, General Studies and Humanities','155, 35, 53'),
        'PCIP25' : ('Library Science','223, 207, 190'),
        'PCIP26' : ('Biological and Biomedical Sciences','85, 180, 176'),
        'PCIP27' : ('Mathematics and Statistics','225, 93, 68'),
        'PCIP29' : ('Military Technologies and Applied Sciences','127, 205, 205'),
        'PCIP30' : ('Multi/Interdisciplinary Studies','188, 36, 60'),
        'PCIP31' : ('Parks, Recreation, Leisure, and Fitness Studies','195, 68, 122'),
        'PCIP38' : ('Philosophy and Religious Studies','152, 180, 212'),
        'PCIP39' : ('Theology and Religious Vocations','76, 106, 146'),
        'PCIP40' : ('Physical Sciences','146, 182, 213'),
        'PCIP41' : ('Science Technologies/Technicians','131, 132, 135'),
        'PCIP42' : ('Psychology','185, 58, 50'),
        'PCIP43' : ('Homeland Security, Law Enforcement, Firefighting and Related Protective Services','175, 148, 131'),
        'PCIP44' : ('Public Administration and Social Service Professions','173, 93, 93'),
        'PCIP45' : ('Social Sciences','0, 110, 81'),
        'PCIP46' : ('Construction Trades','216, 174, 71'),
        'PCIP47' : ('Mechanic and Repair Technologies/Technicians','158, 70, 36'),
        'PCIP48' : ('Precision Production','183, 107, 163'),
        'PCIP49' : ('Transportation and Materials Moving','46, 74, 98'),
        'PCIP50' : ('Visual and Performing Arts','180, 183, 186'),
        'PCIP51' : ('Health Professions and Related Programs','192, 171, 142'),
        'PCIP52' : ('Business, Management, Marketing, and Related Support Services','240, 237, 229'),
        'PCIP54' : ('History','121, 199, 83'),
        'other'  : ('Other subjects','250, 224, 60' ),
    
}

