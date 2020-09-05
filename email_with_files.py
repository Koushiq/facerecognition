#!/usr/bin/env python3

import os
import smtplib
import mimetypes
from email.message import EmailMessage
from email.policy import SMTP


SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', '587'))
GMAIL_USERNAME = os.environ.get('GMAIL_USERNAME', 'sender@gmail.com')
GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD', 'password')


def main():
   
    directory = './dir'

    # Create the message
    msg = EmailMessage()
    msg['Subject'] = 'Unusual Activity Detected..!'
    msg['To'] = 'reciever@gmail.com'
    msg['From'] = 'sender@gmail.com'
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


if __name__ == '__main__':
    main()