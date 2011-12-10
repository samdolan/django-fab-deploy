from .constants import ALL_ROLES, DB_ROLE, WEB_ROLE
from .database import setup_db
from .django import update_db, update_python_libs
from .nginx import stop_nginx, start_nginx
from .ssh import setup_ssh_key
from .supervisor import stop_supervisor, start_supervisor, update_supervisor
from .utils import get_ip
from .webserver import setup_web
from fabric.colors import green
from fabric.api import *
from .git import get_source
from .nginx import update_nginx
import cuisine

COMMON_PACKAGES = [
    'subversion', 'mercurial', 'git-core', 'vim', 'python-dev', 'ufw',
    'python-setuptools', 'htop', 'ntp', 'colordiff', 'python-software-properties',
    'psmisc',
    'libpq-dev', # postgres
]


@task
@roles(DB_ROLE)
@runs_once
def set_database_ip(interface='eth1'):
    """Set the ip of the database."""
    env.db_ip = get_ip(interface)


@task
@roles(WEB_ROLE)
@runs_once
def set_web_server_ips(interface='eth1'):
    """Set the ips of the webservers."""
    env.webserver_internal_ips = [get_ip(interface),]


@task
def set_port(port):
    """Set the port to use for ssh connections."""
    env.port = port

@task
@roles(ALL_ROLES)
def setup_common():
    """Set common packages."""
    print(green("Running setup_common.........."))
    execute(setup_ssh_key)
    cuisine.package_install(COMMON_PACKAGES, True)

    sudo('yes | ufw enable')
    sudo('ufw logging on')
    sudo('ufw allow %(port)s' % env)
    sudo('ufw limit ssh')
    sudo('ufw default deny')

@task
@roles(ALL_ROLES)
def setup_run_dirs():
    for d in (env.log_location, env.socket_location):
        with settings(warn_only=True):
            sudo('mkdir %s' % d)
        sudo('chown -R %s: %s' % (env.deploy_user, d))


@task
def setup():
    """Setup the servers."""
    execute(setup_run_dirs)
    execute(setup_db)
    execute(setup_web)


@task
def update():
    """Update the servers w/the latest source code + migrations."""
    execute(stop_supervisor)
    execute(stop_nginx)

    execute(get_source)
    execute(update_python_libs)
    execute(update_db)
    execute(update_supervisor)
    execute(update_nginx)

    execute(start_supervisor)
    execute(start_nginx)


