from fabric.api import *
from .constants import WEB_ROLE, CONF_DIR
from .utils import package_exists
from fabric.contrib.files import exists, upload_template
from .django import pip
import cuisine
import os

NGINX_INITD = '/etc/init.d/nginx'

@task
@roles(WEB_ROLE)
def install_nginx():
    """Install nginx + uwsgi on the web servers."""
    #sudo('apt-add-repository ppa:nginx/stable')
    #sudo('sudo apt-get update')
    sudo('apt-get install nginx --assume-yes')

    # needed to compile uwsgi
    cuisine.package_ensure('libxml2-dev')
    pip('http://projects.unbit.it/downloads/uwsgi-latest.tar.gz')

    if exists('/etc/nginx/sites-enabled/default'):
        sudo('rm /etc/nginx/sites-enabled/default')

@task
@roles(WEB_ROLE)
def update_nginx():
    """Update the nginx configuration files."""
    execute(stop_nginx)
    upload_template(os.path.join(CONF_DIR, 'nginx', 'domain.conf'),
                    '/etc/nginx/sites-enabled/%(domain_name)s' % env,
                    context=env, backup=False, use_sudo=True)
    execute(start_nginx)


@task
@roles(WEB_ROLE)
def stop_nginx():
    """Stop the nginx web server."""
    with settings(warn_only=True):
        sudo('%s stop' % NGINX_INITD)

@task
@roles(WEB_ROLE)
def restart_nginx():
    """Restart the nginx web server."""
    execute(stop_nginx)
    execute(start_nginx)

@task
@roles(WEB_ROLE)
def start_nginx():
    """Start the nginx web server."""
    sudo('%s start' % NGINX_INITD)

@task
@roles(WEB_ROLE)
def setup_web():
    """Setup a web server."""
    execute(setup_common)
    execute(setup_run_dirs)
    execute(install_supervisor)
    sudo('ufw allow 80/tcp')
    sudo('ufw allow 443/tcp')

    execute(install_nginx)


