import config
from datetime import datetime
import os.path

# Module to get the file list
import glob

# Modules to send emails
import smtplib
#from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Get files of directory with day and month matching to the current date. finish, if there are noch matching files.
today = datetime.now().strftime('%m-%d')
files_of_today = glob.glob(config.directory + "*-" + today + "*.*")

# Set up an email with embedded pictures/movies
msg = MIMEMultipart()
msg['Subject'] = 'Zeitreise'
msg['From'] = config.mail_from
msg['To'] = ', '.join(config.mail_to)

for file in files_of_today:
    (filedir, filename) = os.path.split(file)
    msgText = MIMEText('<img src="cid:%s"><br>' % (filename), 'html') 
    msg.attach(msgText)

    with open(file, 'rb') as fp:
        img = MIMEImage(fp.read())
    
    img.add_header('Content-ID', '<{}>'.format(filename))
    msg.attach(img)

# Send mail.
with smtplib.SMTP(config.smtp_server, config.smtp_port) as s:
    s.login(config.smtp_user, config.smtp_pass)
    s.send_message(msg)