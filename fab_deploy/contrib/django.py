from .constants import ALL_ROLES, CONF_DIR, WEB_ROLE
from contextlib import contextmanager as _contextmanager
from fabric.api import *
from fabric.colors import green, yellow
from fabric.contrib.files import exists, upload_template
import os

@task
@roles(WEB_ROLE)
def setup_python_env():
    sudo('easy_install pip')
    pip_packages = ['virtualenv', 'virtualenvwrapper']
    sudo('pip install {0}'.format(' '.join(pip_packages)))

    deploy_profile = os.path.join(env.deploy_user_home, '.profile')
    #put(os.path.join(CONF_DIR, 'bashrc'), deploy_profile, use_sudo=True)
    #sudo('chown %s: %s' % (env.deploy_user, deploy_profile))

    from .django import deploy_user
    #deploy_user('source %s' % deploy_profile)

    if not exists(env.virtual_env_loc):
        print(green("Setting up virtual environment @ %(virtual_env_name)s" % env))
        deploy_user('mkdir -p %(workon_home)s' % env)
        deploy_user('export WORKON_HOME=%(workon_home)s && source /usr/local/bin/virtualenvwrapper.sh && mkvirtualenv %(virtual_env_name)s' % env)
        sudo('chown -R %(deploy_user)s: %(workon_home)s' % env)
        sudo('chmod 755 %(workon_home)s' % env)
    else:
        sudo('chown -R %(deploy_user)s: %(workon_home)s' % env)
        sudo('chmod 755 %(workon_home)s' % env)
        print(yellow("Environment already exists @ %(virtual_env_loc)s." % env))

@task
def update_python_libs():
    # TODO: We shouldn't do this, but it fails on writing to
    # /home/%(user)s/.pip
    with settings(warn_only=True):
        with virtualenv():
            deploy_user('pip install -r %(requirements_file)s' % env)

@task
@roles(WEB_ROLE) # The webserver is connected the db
@runs_once
def update_db():
    from .servers import set_web_server_ips
    execute(set_web_server_ips)

    with virtualenv():
        manage_py('syncdb --noinput')
        for app in env.apps_to_migrate:
            manage_py('migrate {0}'.format(app))


@task
@roles(WEB_ROLE)
def install_settings():
    from .servers import set_database_ip
    execute(set_database_ip)
    upload_template(os.path.join(CONF_DIR, 'settings', 'local_settings.py'),
                    os.path.join(env.app_root, 'local_settings.py'),
                    use_sudo=True, context=env)

@_contextmanager
def virtualenv():
    activate_cmd = 'source %(virtual_env_activate)s' % env
    with prefix(activate_cmd):
        yield

def manage_py(cmd, *args, **kwargs):
    with virtualenv():
        return deploy_user('source %s && python %s/manage.py %s' % (env.virtual_env_activate, env.app_root, cmd), *args, **kwargs)

def deploy_user(cmd, *args, **kwargs):
    kwargs['user'] = env.deploy_user
    return sudo(cmd, *args, **kwargs)

def pip(package, use_sudo=True):
    cmd = sudo if use_sudo else run
    return cmd('pip install %s' % package)


