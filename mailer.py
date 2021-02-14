import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import logging.config
import datetime

from constants import *


def sendmail_with_attached(
    sender_email, sender_pass, receiver_email, attach_file, cc_mail=None
):
    """ """
    try:
        subject = "High temperature alert from [{}]".format(IDENTIFIER)

        # Create a multipart message and set headers
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        # message["Bcc"] = cc_mail

        # Add body to email
        # message.attach(MIMEText(body, "plain"))

        html = """\
        <html>
        <body>
            <h1 style="font-size: 24px; margin: 0;">Location/Identifier: {}</h1>
            <h4>{}</h4>
        </body>
        </html>
        """.format(
            IDENTIFIER, datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        )
        message.attach(MIMEText(html, "html"))

        # Open PDF file in binary mode
        with open(attach_file, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode file in ASCII characters to send by email
        encoders.encode_base64(part)

        # Add header as key/value pair to attachment part
        part.add_header(
            "Content-Disposition",
            "attachment; filename= captured.jpg",
        )

        # Add attachment to message and convert message to string
        message.attach(part)
        text = message.as_string()

        # Log in to server using secure context and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, sender_pass)
            server.sendmail(sender_email, receiver_email, text)
        logging.warning("Email sent successfully to {}".format(receiver_email))

    except Exception as error:
        logging.error(error, exc_info=True)
