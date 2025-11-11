"""
Email sending helper: prefer SendGrid Web API (HTTP) and fall back to SMTP.
Set SENDGRID_API_KEY and MAIL_DEFAULT_SENDER in env for Web API mode.
If SENDGRID_API_KEY is not present, configure MAIL_SERVER/MAIL_PORT/MAIL_USERNAME/MAIL_PASSWORD for SMTP fallback.
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
    SENDGRID_AVAILABLE = True
except Exception:
    SENDGRID_AVAILABLE = False


def send_email(to_email, subject, body, html_body=None):
    """Send an email. Returns True on success, raises on failure."""
    sendgrid_key = os.getenv('SENDGRID_API_KEY')
    sender = os.getenv('MAIL_DEFAULT_SENDER', os.getenv('MAIL_USERNAME', 'noreply@example.com'))

    # Try SendGrid Web API first
    if SENDGRID_AVAILABLE and sendgrid_key:
        try:
            sg = SendGridAPIClient(sendgrid_key)
            message = Mail(from_email=sender, to_emails=to_email, subject=subject, plain_text_content=body)
            if html_body:
                message.html = html_body
            response = sg.send(message)
            print(f"SendGrid API sent email to {to_email}: status {response.status_code}")
            return True
        except Exception as e:
            print(f"SendGrid API error: {e}")
            # fall through to SMTP fallback

    # SMTP fallback (works with SendGrid SMTP relay if SENDGRID_API_KEY is provided)
    mail_server = os.getenv('MAIL_SERVER')
    mail_port = int(os.getenv('MAIL_PORT', 587))
    mail_username = os.getenv('MAIL_USERNAME')
    mail_password = os.getenv('MAIL_PASSWORD')
    use_tls = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes', 'on')

    # If no MAIL_SERVER but sendgrid key present, use SendGrid SMTP defaults
    if not mail_server and sendgrid_key:
        mail_server = 'smtp.sendgrid.net'
        mail_port = 587
        mail_username = 'apikey'
        mail_password = sendgrid_key
        use_tls = True

    if not mail_server:
        raise RuntimeError('No email configuration found: set SENDGRID_API_KEY or MAIL_SERVER env vars')

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to_email
    msg.attach(MIMEText(body, 'plain'))
    if html_body:
        msg.attach(MIMEText(html_body, 'html'))

    try:
        with smtplib.SMTP(mail_server, mail_port, timeout=20) as server:
            server.ehlo()
            if use_tls:
                server.starttls()
                server.ehlo()
            if mail_username and mail_password:
                server.login(mail_username, mail_password)
            server.send_message(msg)
        print(f"SMTP email sent to {to_email}")
        return True
    except Exception as e:
        print(f"SMTP send error: {e}")
        raise
