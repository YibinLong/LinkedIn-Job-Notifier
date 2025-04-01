import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# First check GitHub Actions environment variables, and fall back to .env if not found
sender_email = os.environ['SENDER_EMAIL'] 
receiver_email = os.environ['RECEIVER_EMAIL']
gmail_app_password = os.environ['GMAIL_APP_PASSWORD']

# Edit this list to change your job search terms
search_terms = "junior software engineer,junior software developer,associate software engineer,associate software developer,software engineer,software developer"

# Gmail Configuration
smtp_server = "smtp.gmail.com"
smtp_port = 587

# LinkedIn job search parameters
geo_id = "101174742"  # Set to US
time_filter = "r3600"  # Last hour

def generate_links():
    links_by_term = {}
    for term in search_terms.split(","):
        term_stripped = term.strip()
        # Format term in title case
        title = term_stripped.title()
        # Replace spaces with %20 and ensure term is properly formatted for URL
        keywords = term_stripped.replace(" ", "%20")
        # Create two links - one for US and one for Canada
        us_link = f"https://www.linkedin.com/jobs/search/?f_TPR={time_filter}&geoId={geo_id}&keywords={keywords}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&spellCorrectionEnabled=true"
        canada_link = f"https://www.linkedin.com/jobs/search/?f_TPR={time_filter}&geoId=101174742&keywords={keywords}&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&spellCorrectionEnabled=true"
        
        # Store by term for grouped display
        links_by_term[title] = [
            (f"USA {title}", us_link),
            (f"Canada {title}", canada_link)
        ]
    
    return links_by_term

def send_email():
    links_by_term = generate_links()
    subject = "Hourly Job Search Reminder - LinkedIn"
    
    # Create HTML message with hyperlinks
    html_body = """
    <html>
    <head></head>
    <body>
    <p><a href="https://www.gmail.com">Gmail Link</a></p>
    <p>Apply to jobs released within the last hour:</p>
    """
    
    # Group links by job title with section breaks
    for title, links in links_by_term.items():
        html_body += f'<h3>{title}:</h3>\n<ul>\n'
        for link_title, link_url in links:
            html_body += f'<li><a href="{link_url}">{link_title}</a></li>\n'
        html_body += '</ul>\n<hr>\n'
    
    html_body += """
    </body>
    </html>
    """
    
    # Plain text version as fallback with same grouping
    text_body = "Gmail: https://www.gmail.com\n\n"
    text_body += "Apply to these jobs released within the last hour:\n\n"
    
    for title, links in links_by_term.items():
        text_body += f"{title}:\n\n"
        for link_title, link_url in links:
            text_body += f"- {link_title}: {link_url}\n"
        text_body += "\n------------------------------\n\n"

    msg = MIMEMultipart('alternative')
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    # Attach both plain text and HTML versions
    msg.attach(MIMEText(text_body, 'plain'))
    msg.attach(MIMEText(html_body, 'html'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, gmail_app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❗ Failed to send email: {e}")

if __name__ == "__main__":
    send_email()
