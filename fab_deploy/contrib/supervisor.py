from fabric.api import *
from .constants import WEB_ROLE, CONF_DIR
from fabric.contrib.files import upload_template
import cuisine
import os

@task
@roles(WEB_ROLE)
def install_supervisor():
    """Install supervisor on the web servers."""
    from .django import pip
    # ubuntu 11.04 has a bad version
    pip('elementtree')
    cuisine.package_ensure('supervisor')
    execute(stop_supervisor)
    execute(update_supervisor)

@task
@roles(WEB_ROLE)
def update_supervisor():
    """Update the supervisor + conf.d configuration."""
    execute(stop_supervisor)
    upload_template(os.path.join(CONF_DIR, 'supervisord', 'uwsgi.conf'),
                    '/etc/supervisor/conf.d/', context=env, backup=False,
                   use_sudo=True)
    execute(start_supervisor)

@task
@roles(WEB_ROLE)
def stop_supervisor():
    """Stop supervisor if it's running."""
    with settings(warn_only=True):
        sudo('supervisorctl stop all')

@task
@roles(WEB_ROLE)
def restart_supervisor():
    """Restart supervisor."""
    execute(stop_supervisor)
    execute(start_supervisor)

@task
@roles(WEB_ROLE)
def start_supervisor():
    """Start supervisor."""
    # Try to start if we're not already running, try to...
    with settings(warn_only=True):
        sudo('/etc/init.d/supervisord start')
    with settings(warn_only=True):
        sudo('supervisorctl reread')
    with settings(warn_only=True):
        sudo('supervisorctl restart all')


