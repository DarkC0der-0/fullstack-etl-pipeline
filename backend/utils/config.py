import os

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
SLACK_TOKEN = os.getenv('SLACK_TOKEN', 'your-slack-token')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.getenv('EMAIL_PORT', 587)
EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'your-email@example.com')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'your-email-password')