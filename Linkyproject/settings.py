import os
from pathlib import Path
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Use dev-friendly defaults if env vars are not set
DEBUG = os.environ.get('DEBUG', 'False') == 'True'  # Default is False for production
SECRET_KEY = os.environ.get('SECRET_KEY', 'insecure-key-for-dev')  # Set a real secret key in production
ALLOWED_HOSTS = ['linkydrop.onrender.com', 'localhost', '127.0.0.1']



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'linky',  # Your app name
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # OK for both dev & prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Linkyproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'linky', 'templates')],
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

WSGI_APPLICATION = 'Linkyproject.wsgi.application'

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # Optional, but good to have in production:
    # 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # 'django.contrib.auth.password_validation.NumericPasswordValidator',
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'linky', 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Static files handling in production
if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security settings
SECURE_SSL_REDIRECT = not DEBUG  # Redirect all HTTP to HTTPS in production
CSRF_COOKIE_SECURE = not DEBUG  # Use secure cookies in production
SESSION_COOKIE_SECURE = not DEBUG  # Use secure cookies in production
X_FRAME_OPTIONS = 'DENY'  # Security best practice

# For using the `django-environ` package or similar for environment variables:
# Make sure to set environment variables on Render for:
# - SECRET_KEY
# - DATABASE_URL
# - ALLOWED_HOSTS
# - DEBUG (False for production)
