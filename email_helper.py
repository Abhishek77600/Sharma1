"""
Email sending helper using SendGrid Web API.
Requires SENDGRID_API_KEY and MAIL_DEFAULT_SENDER environment variables.
"""
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_email(to_email, subject, body, html_body=None):
    """
    Send an email using SendGrid API.
    Returns True on success, raises exception on failure.
    
    Args:
        to_email: Recipient email address
        subject: Email subject
        body: Plain text email body
        html_body: Optional HTML email body
    
    Raises:
        RuntimeError: If SendGrid API key is not configured
        Exception: If email sending fails
    """
    sendgrid_key = os.getenv('SENDGRID_API_KEY')
    sender = os.getenv('MAIL_DEFAULT_SENDER')
    
    if not sendgrid_key:
        raise RuntimeError('SENDGRID_API_KEY environment variable is not set')
    
    if not sender:
        raise RuntimeError('MAIL_DEFAULT_SENDER environment variable is not set')
    
    try:
        sg = SendGridAPIClient(sendgrid_key)
        message = Mail(
            from_email=sender,
            to_emails=to_email,
            subject=subject,
            plain_text_content=body
        )
        
        if html_body:
            message.html = html_body
        
        response = sg.send(message)
        print(f"SendGrid API sent email to {to_email}: status {response.status_code}")
        return True
    except Exception as e:
        print(f"SendGrid API error: {e}")
        raise
