import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os

# Configuration
sender_email = os.environ['SENDER_EMAIL']
receiver_email = os.environ['RECEIVER_EMAIL']
app_password = os.environ['OUTLOOK_APP_PASSWORD']
smtp_server = "smtp.office365.com"
smtp_port = 587

# LinkedIn job search parameters
search_terms = os.environ.get('SEARCH_TERMS', 'software engineer')
geo_id = "101174742"  # Set to US
time_filter = "r3600"  # Last hour

def generate_link():
    keywords = "%20".join(search_terms.split(","))
    return f"https://www.linkedin.com/jobs/search/?f_TPR={time_filter}&geoId={geo_id}&keywords={keywords}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true"

def send_email():
    job_url = generate_link()
    subject = "Hourly Job Search Reminder - LinkedIn"
    body = f"Apply to jobs within the last hour:\n\n{job_url}"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❗ Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
