import os
import dj_database_url
from .settings import *

# Security configuration
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'your-fallback-default-secret-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Render dynamically assigns the host domain via environment variables
ALLOWED_HOSTS = ['*']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Production Databases: Render PostgreSQL Manager
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Production Celery + Redis Configuration 
CELERY_BROKER_URL = os.environ.get("REDIS_URL")
CELERY_RESULT_BACKEND = os.environ.get("REDIS_URL")

# Security Headers for SaaS production-grade applications
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'False') == 'True'