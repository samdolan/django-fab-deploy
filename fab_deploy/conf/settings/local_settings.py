DATABASES = {
    'default': {
        'ENGINE': '{{ env.db_engine }}',
        'NAME': '{{ env.db_name }}',
        'USER': '{{ env.db_user }}',
        'PASSWORD': '{{ env.db_password }}',
        'HOST': '{{ env.db_ip }}',
        'PORT': '{{ env.db_port }}',
    }
}

{% for setting, value in extra_local_settings.items() %}{{ setting }} = {{ value }}
{% endfor %}

