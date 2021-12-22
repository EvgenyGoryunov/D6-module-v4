import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ih%n$n4g-&dyjs0nlo1u^+=6^@q!mtqmka8hy8r+r1lmpb6f5t'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Модуль Д5
ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # приложения для модуля Д1-3
    'django.contrib.sites',
    'django.contrib.flatpages',

    # приложения для модуля Д4
    'newapp',
    'django_filters',  # чтоб фильтра поддерживались нужно устанавливать

    # приложения для модуля Д5
    'sign',
    'protect',

    # чтоб возможно было авторизоваться через сторонние сервисы, такие как гугл, мы устанавливаем
    # дополнительный пакет pip install django-allauth и прописываем все приложения в данном файле
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    # модуль Д6
    'appointments',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware'
]

ROOT_URLCONF = 'project.urls'

# это все, что относится по части шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # путь, где лежат нами созданные шаблоны
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                # требуется удостовериться, что в конфигурации шаблонов присутствует контекстный процессор
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "newapp/static"
]

# используется в случае, если данный проект управляет несколькими сайтами, но для нас сейчас это не является
# принципиальным. Достаточно явно прописать значение 1 для этой переменной.
SITE_ID = 1

# для модуля Д5 (прошлая версия ссылки)

# Django перенаправляет неавторизованных пользователей на страницу входа, указанного по данному пути
LOGIN_URL = 'sign/login/'

# Чтобы возможно было авторизоваться через сторонние сервисы, такие как гугл, мы создаем другую форму и
# соответсвенно указываем другой адрес, первая форма лучше, чем эта, эта никакая вообще
# LOGIN_URL = '/accounts/login/'


# При корректных данных для входа, пользователь перенаправляется на страницу, указанною по данному пути
# страница, куда перенаправляется пользователь после успешного входа на сайт, в данном случае корневая страница сайта
LOGIN_REDIRECT_URL = '/news/'

# модуль Д5, чтоб можно было авторизоваться через сторонние сервисы, грубо говоря, нам нужно «включить»
# аутентификацию как по username, так и специфичную по email или сервис-провайдеру
AUTHENTICATION_BACKENDS = [

    # добавить бэкенды аутентификации: встроенный бэкенд Django, реализующий аутентификацию по username
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # бэкенд аутентификации, предоставленный пакетом allauth
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Первые два указывают на то, что поле email является обязательным и уникальным, а третий, наоборот, говорит,
# что username теперь необязательный. Следующий параметр указывает, что аутентификация будет происходить
# посредством электронной почты. Напоследок мы указываем, что верификация почты отсутствует. Обычно на почту
# отправляется подтверждение аккаунта, после подтверждения которого восстанавливается полная функциональность
# учетной записи. Для тестового примера нам не обязательно это делать.
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'none'

# Чтобы allauth распознал нашу форму как ту, что должна выполняться вместо формы по умолчанию
ACCOUNT_FORMS = {'signup': 'sign.models.BasicSignupForm'}

# ОБАЗЯТЕЛЬНО СДЕЛАТЬ МИГРАЦИИ ЧТОБЫ ДОБАВИЛИСЬ В АДМИНКУ SOCIAL ACCOUNTS!!!


# Блок Д6 - настройка отправки почты

EMAIL_HOST = 'smtp.yandex.ru'  # адрес сервера Яндекс-почты для всех один и тот же
EMAIL_PORT = 465  # порт smtp сервера тоже одинаковый
EMAIL_HOST_USER = 'factoryskill'  # ваше имя пользователя, например, если ваша почта user@yandex.ru, то сюда надо
# писать user, иными словами, это всё то что идёт до собачки (@)
EMAIL_HOST_PASSWORD = 'qazwsx963852'  # пароль от почты
EMAIL_USE_SSL = True  # Яндекс использует ssl, включать обязательно