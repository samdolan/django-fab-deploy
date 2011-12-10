DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '%(db_name)s',
        'USER': '%(db_user)s',
        'PASSWORD': '',
        'HOST': '%(db_ip)s',
        'PORT': '%(db_port)s',
    }
}
TEMPLATE_DEBUG = DEBUG = False

