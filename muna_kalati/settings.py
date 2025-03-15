import os

# Use environment variables for sensitive settings
SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")  # Replace with a secure key
DEBUG = os.getenv("DEBUG", "False") == "True"

# Allow all hosts for now (update for production)
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Static files configuration for Whitenoise
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Enable Whitenoise middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ...existing middleware...
]

# Database configuration (SQLite for now)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
