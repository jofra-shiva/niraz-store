import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# Load dot env variables
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-niraz-key-12651-74187-81247')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'core',
    'products',
    'cart',
    'orders',
    'dashboard',
    'payments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # For production static serving
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'niraz_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',  # Global cart context processor
            ],
        },
    },
]

WSGI_APPLICATION = 'niraz_project.wsgi.application'
ASGI_APPLICATION = 'niraz_project.asgi.application'

# Database Setup - PostgreSQL-ready with SQLite fallback for seamless boot-up
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL', f"sqlite:///{BASE_DIR / 'db.sqlite3'}"),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# Media Files (Cloudinary or local)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Cloudinary Integration (Configured dynamically if CLOUDINARY_URL is set)
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')

if CLOUDINARY_URL:
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
        'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
    }

# Session cart identification key
CART_SESSION_ID = 'cart'

# Login URL for owner dashboard routing
LOGIN_URL = '/dashboard/login/'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Razorpay credentials
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID', 'rzp_test_example_id_12345')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET', 'test_example_secret_abcde')

# Add WhiteNoise config to requirements if needed (recommended for static serving)
# We can include whitenoise directly in requirements.txt or handle static securely.
# Let's add whitenoise to requirements.txt for dynamic static routing on Render.
