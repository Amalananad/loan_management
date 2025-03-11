"""
Django settings for loan_management project.
"""

from pathlib import Path
import os
import dj_database_url  # Import this package
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
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# ==============================
# 🔹 ALLOWED HOSTS (Fix Render Domain)
# ==============================
ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "loan-management-1-12jv.onrender.com",  # ✅ Remove "https://"
]

# ==============================
# 🔹 DATABASE CONFIG (Use Render's PostgreSQL)
# ==============================
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}

# ==============================
# 🔹 STATIC FILES
# ==============================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ==============================
# 🔹 AUTHENTICATION
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
    'SIGNING_KEY': SECRET_KEY,  # ✅ Use the `SECRET_KEY` from env
}

# ==============================
# 🔹 CSRF CONFIG (Fix Render Trusted Origins)
# ==============================
CSRF_TRUSTED_ORIGINS = [
    "https://loan-management-1-12jv.onrender.com",  # ✅ Keep only domain
]

# ==============================
# 🔹 SECURITY HEADERS (Recommended)
# ==============================
SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
SESSION_COOKIE_SECURE = True  # Use secure cookies
CSRF_COOKIE_SECURE = True  # Secure CSRF cookie
SECURE_BROWSER_XSS_FILTER = True  # XSS protection
SECURE_CONTENT_TYPE_NOSNIFF = True  # Prevent MIME-sniffing

