"""
Django settings for loan_management project.
"""

from pathlib import Path
import os
import dj_database_url  # Import for database config
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
DEBUG = True
# ==============================
# 🔹 ALLOWED HOSTS
# ==============================
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "loan-management-1-12jv.onrender.com",
]
#DATABASE_URL = os.getenv('60dd8e0ac7447ff28d638a817e64fd6d')  # Make sure this is set in Render's environment variables


#ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(' ') if not DEBUG else []


# ==============================
# 🔹 DATABASE CONFIG (Use PostgreSQL)
# ==============================
#DATABASES = {
DATABASE_URL = os.getenv('DATABASE_URL','postgresql://postgres1:Li5PeUNDdX0ByaHTqyPXHPzE1I9MQrMg@dpg-cv8q6pt2ng1s73cbngh0-a/loan_management_gm14')
DATABASES = {
    'default': dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=600  # Keeps database connections open for performance
    )
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'loan_management1',
#         'USER': 'postgres',
#         'PASSWORD': 'appunni0481',
#         'HOST': 'localhost',
#         'PORT': '5433',  # Make sure this matches your PostgreSQL port
#     }
# }

# ==============================
# 🔹 STATIC FILES
# ==============================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
    #'SIGNING_KEY': SECRET_KEY,
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
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
