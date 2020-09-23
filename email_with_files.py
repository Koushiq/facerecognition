import os
import smtplib
import mimetypes
from email.message import EmailMessage
from email.policy import SMTP


def mail(path,title):
    
    sender = open('senderemail.txt','r')
    sender = sender.read()
    
    
    
    senderpassword = open('senderemailpassword.txt','r')
    senderpassword = senderpassword.read()
    
    receiver = open('receiveremail.txt','r')
    receiver = receiver.read()
    
    print("sender "+sender)
    print("password "+senderpassword)
    print("receiver "+receiver)
    
    
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
    #insert sender credentials here
    GMAIL_USERNAME = os.environ.get('GMAIL_USERNAME', sender)
    GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', senderpassword)
    directory = path

    # Create the message
    msg = EmailMessage()
    msg['Subject'] = title
    #insert sender receiver here 
    msg['To'] = receiver
    msg['From'] = sender
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'

    for filename in os.listdir(directory):
        path = os.path.join(directory, filename)
        if not os.path.isfile(path):
            continue

        ctype, encoding = mimetypes.guess_type(path)
        if ctype is None or encoding is not None:

            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        with open(path, 'rb') as fp:
            msg.add_attachment(fp.read(),
                               maintype=maintype,
                               subtype=subtype,
                               filename=filename)
            

    #sending mail
    session = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    session.send_message(msg)
