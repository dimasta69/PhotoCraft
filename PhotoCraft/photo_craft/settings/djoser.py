import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
SERVER_EMAIL = os.getenv('SERVER_EMAIL')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND')

DJOSER = {
    'ACTIVATION_URL': '#/activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}
