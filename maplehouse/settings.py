"""
Django settings for maplehouse project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd&)gwsv!q==l^)n1@73ipmwcdurxfe-$#c+44i%!z-_uz!p*x8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'renting.apps.RentingConfig',
    "rest_framework",
    'haystack',
    "stark.apps.StarkConfig"
]

MIDDLEWARE = [
    # 缓存头
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 缓存尾
    'django.middleware.cache.FetchFromCacheMiddleware',
]

ROOT_URLCONF = 'maplehouse.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'maplehouse.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'maplehouse',
        'HOST': '127.0.0.1',
        'POST': 3306,
        'USER': 'root',
        'PASSWORD': '123'
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# 静态文件配置
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# auth模块配置
AUTH_USER_MODEL = "renting.UserInfo"

# media文件夹配置
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# redis在django中的配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
            # "PASSWORD": "123",
        }
    }
}

# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'  # 如果是 163 改成 smtp.163.com
EMAIL_PORT = 465
EMAIL_HOST_USER = 'ffm1110@qq.com'  # 帐号
EMAIL_HOST_PASSWORD = 'vctehqndwrnjbgda'  # 授权密码,不是你登入的密码
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
# 这样收到的邮件，收件人处就会这样显示
# DEFAULT_FROM_EMAIL = 'lqz<'306334678@qq.com>'
EMAIL_USE_SSL = True  # 使用ssl
# EMAIL_USE_TLS = False # 使用tls

# EMAIL_USE_SSL 和 EMAIL_USE_TLS 是互斥的，即只能有一个为 True

# 全文检索配置
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
    },
}

# 自动更新索引,自动跟更新和信号量有关(有django的orm插入数据才会更新)
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

# 设置session保存时间
SESSION_COOKIE_AGE = 60 * 60 * 24

# 访问ip频率限制
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': ['renting.utils.VisitThrottle', ],
    'DEFAULT_THROTTLE_RATES': {
        'maplehouse': '30/minute'
    }
}

# 缓存超时时间
CACHE_MIDDLEWARE_SECONDS=20