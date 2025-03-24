import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from utils.config import SLACK_TOKEN, EMAIL_HOST, EMAIL_PORT, EMAIL_ADDRESS, EMAIL_PASSWORD

def send_email(subject, body, to):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

def send_slack_message(channel, message):
    client = WebClient(token=SLACK_TOKEN)
    try:
        response = client.chat_postMessage(channel=channel, text=message)
    except SlackApiError as e:
        print(f"Failed to send Slack message: {e.response['error']}")