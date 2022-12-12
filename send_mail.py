import datetime
import csv
import smtplib
from email.message import EmailMessage
import ssl
import os
from dotenv import load_dotenv
load_dotenv()

with open('subscription.csv')as email_client:
    reader = csv.DictReader(email_client)
    get_today = datetime.datetime.now()

    for data in reader:
        targeted_date = datetime.datetime.strptime(
            data['expiry_date'], "%Y-%m-%d")

        diffrence = targeted_date - get_today
        # print(diffrence)
        if diffrence.days < abs(5):
            print('subscription expiring in 5 days !!!')
            email_sender = os.getenv('sender')
            email_password = os.getenv('password')
            email_receiver = data['email']
            subject = 'Notification About Subscription'

            body = """

            Your subscription is going to expire in 5 days !!!
            please renew your subscription soon

            """

            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)

            context = ssl.create_default_context()

            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context)as s:
                s.login(email_sender, email_password)
                s.sendmail(email_sender, email_receiver, em.as_string())
