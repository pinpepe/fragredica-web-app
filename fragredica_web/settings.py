"""
Django settings for fragredica_web project.

Generated by 'django-admin startproject' using Django 5.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

# SECURITY WARNING: keep the secret key used in production secret!
# En producción, este valor se leerá de una variable de entorno en Render.
# Para desarrollo local, puedes dejar esta clave de ejemplo o crear un archivo .env.
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-a-default-key-for-local-development')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG será True localmente, y False cuando se despliegue en Render.
# Render establece la variable de entorno 'RENDER' a 'true' automáticamente.
DEBUG = 'RENDER' not in os.environ

# Configuración de los hosts permitidos.
# Localmente, permitimos cualquier host. En Render, se añadirá automáticamente
# el dominio de la aplicación.
ALLOWED_HOSTS = []

# Render provee el hostname en esta variable de entorno
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)


# Application definition
INSTALLED_APPS = [
    # Aplicaciones por defecto de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Aplicaciones de terceros
    'rest_framework',
    'corsheaders',
    
    # Tus aplicaciones
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise Middleware para servir archivos estáticos en producción
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # CORS Middleware debe ir antes de CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'fragredica_web.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'fragredica_web.wsgi.application'


# ==============================================================================
# DATABASE SETTINGS
# ==============================================================================

# Usaremos dj_database_url para leer la configuración de la base de datos
# desde la variable de entorno DATABASE_URL que nos proporciona Render.
DATABASES = {
    'default': dj_database_url.config(
        # Si DATABASE_URL no está definida, usará la base de datos SQLite local.
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600 # Mantiene las conexiones abiertas por 10 minutos
    )
}


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'es-es' # Cambiado a español
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC & MEDIA FILES
# ==============================================================================

# URL para referirse a los archivos estáticos desde las plantillas
STATIC_URL = '/static/'
# URL para referirse a los archivos subidos por los usuarios
MEDIA_URL = '/media/'
# Ruta en el disco donde se guardarán los archivos subidos (ej. los MP3)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Configuración para producción (Render)
if not DEBUG:
    # Directorio donde `collectstatic` reunirá todos los archivos estáticos.
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # Almacenamiento optimizado para WhiteNoise.
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ==============================================================================
# CELERY (Task Queue) SETTINGS
# ==============================================================================

# Usaremos la variable de entorno REDIS_URL que nos proporciona Render.
# Localmente, asumirá que Redis está en localhost.
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# ==============================================================================
# THIRD-PARTY LIBRARIES SETTINGS
# ==============================================================================

# Django REST Framework
REST_FRAMEWORK = {
    # Por defecto, requerimos que los usuarios estén autenticados para acceder a la API.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # Aquí configurarías la autenticación por Token o JWT en el futuro.
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],
}

# CORS Headers
# Para desarrollo, permitimos peticiones desde cualquier origen.
# En producción, deberías restringir esto a la URL de tu frontend.
CORS_ALLOW_ALL_ORIGINS = True
# O de forma más segura:
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "https://tu-frontend.onrender.com",
# ]


# ==============================================================================
# DEFAULT PRIMARY KEY
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
