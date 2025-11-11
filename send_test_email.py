"""
Run locally to test email sending. Requires .env with SENDGRID_API_KEY or SMTP settings.
"""
import os
from dotenv import load_dotenv
load_dotenv()

from email_helper import send_email

if __name__ == '__main__':
    to_addr = os.getenv('TEST_EMAIL_TO') or input('Recipient email: ')
    subject = 'Render-demo test email'
    body = 'This is a test email from the render-demo app.'
    try:
        send_email(to_addr, subject, body)
        print('Email send attempted successfully')
    except Exception as e:
        print('Email send failed:', e)
