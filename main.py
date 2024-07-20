import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime

def create_email(date_str, state):
    # Convert the date string to a datetime object
    date_format = "%Y-%m-%d"  # Assuming the date format is YYYY-MM-DD
    date_obj = datetime.strptime(date_str, date_format)
    
    # Get the current date
    current_date = datetime.now()
    
    # Check if the date is less than the current date or if the state is "retraso" or "retrasoExtremo"
    if date_obj < current_date or state in ["retraso", "retrasoExtremo"]:
        # Create the email content
        email_subject = "Action Required: Urgent Issue Detected"
        email_body = f"""
        Dear User,

        We have detected an issue that requires your immediate attention.

        Details:
        - Date: {date_str}
        - State: {state}

        Please take the necessary actions to address this issue as soon as possible.

        Best regards,
        Your Monitoring Team
        """
        
        return email_subject, email_body
    
    return None, None

def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}")

# Example usage
date_str = "2024-07-18"
state = "retraso"
subject, body = create_email(date_str, state)

if subject and body:
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "italo.casanova.d@uni.pe"
    sender_password = "DwXwKPDwLz8n3GX."
    recipient_email = "ever.burga.p@uni.pe"
    
    send_email(smtp_server, smtp_port, sender_email, sender_password, recipient_email, subject, body)
else:
    print("No action required.")
