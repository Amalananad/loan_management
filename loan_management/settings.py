"""
Django settings for loan_management project.
"""

from pathlib import Path
import os
import dj_database_url  # For database configuration
from datetime import timedelta
from dotenv import load_dotenv  # Load environment variables

# Load environment variables from `.env` file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ==============================
# 🔹 SECRET KEY (Security Fix)
# ==============================
SECRET_KEY = os.getenv('SECRET_KEY', 'your-default-secret-key')

# ==============================
# 🔹 DEBUG MODE (Set False in Production)
# ==============================
DEBUG = os.getenv('DEBUG', 'False') == 'True'  # Default is False

# ==============================
# 🔹 ALLOWED HOSTS
# ==============================
ALLOWED_HOSTS = ["loan-management-1-12jv.onrender.com"]


# ==============================
# 🔹 DATABASE CONFIG (Use PostgreSQL)
# ==============================

DATABASE_URL = os.getenv('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600,
        ssl_require=True  # Ensure SSL is enabled for security on Render
    )
}

# ==============================
# 🔹 STATIC FILES
# ==============================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ==============================
# 🔹 INSTALLED APPS
# ==============================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'loans',
    'django_extensions',
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_otp',
    'django_otp.plugins.otp_email',
]

# ==============================
# 🔹 TEMPLATES CONFIGURATION (FIXED)
# ==============================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Ensure this path exists
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ==============================
# 🔹 MIDDLEWARE
# ==============================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

# ==============================
# 🔹 ROOT URL CONF & WSGI
# ==============================
ROOT_URLCONF = 'loan_management.urls'
WSGI_APPLICATION = 'loan_management.wsgi.application'

# ==============================
# 🔹 AUTHENTICATION BACKENDS
# ==============================
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# ==============================
# 🔹 REST FRAMEWORK & JWT SETTINGS
# ==============================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
}

# ==============================
# 🔹 CSRF CONFIG
# ==============================
CSRF_TRUSTED_ORIGINS = [
    "https://loan-management-1-12jv.onrender.com",
]

# ==============================
# 🔹 SECURITY HEADERS (Recommended)
# ==============================
SECURE_SSL_REDIRECT = True  # Force HTTPS
SESSION_COOKIE_SECURE = True  # Secure cookies
CSRF_COOKIE_SECURE = True  # Secure CSRF cookie
SECURE_HSTS_SECONDS = 31536000  # Enable HTTP Strict Transport Security (HSTS)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True


