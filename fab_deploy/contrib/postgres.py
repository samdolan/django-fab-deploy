from fabric.api import *
from .constants import DB_ROLE, CONF_DIR
from fabric.contrib.files import upload_template
from .utils import package_exists
import cuisine
import os

@task
@roles(DB_ROLE)
def setup_db():
    """Setup the database servers."""
    execute(setup_common)
    execute(install_postgres)

@task
@roles(DB_ROLE)
def update_db_conf():
    """Update the database configuration."""
    # TODO: Move this these into a common module, so we don't have to bury it like this.
    from .servers import set_database_ip
    from .servers import set_web_server_ips
    execute(set_database_ip)
    execute(set_web_server_ips)

    # Update the configuration files

    upload_template('pg_hba.conf', '/etc/postgresql/9.1/main/pg_hba.conf',
                    template_dir=os.path.join(CONF_DIR, 'postgres'),
                    context={'env': env}, use_sudo=True, use_jinja=True)

    upload_template('postgresql.conf', '/etc/postgresql/9.1/main/postgresql.conf',
                    template_dir=os.path.join(CONF_DIR, 'postgres'),
                    context={'env': env}, use_sudo=True, use_jinja=True)

    with settings(warn_only=True):
        sudo('/etc/init.d/postgresql start')

    sudo('/etc/init.d/postgresql reload')

    for web_server_ip in env.webserver_internal_ips:
        sudo('ufw allow from %s proto tcp to any port %s' % (web_server_ip, env.db_port))

@task
@roles(DB_ROLE)
def install_postgres():
    """Install the postgres server."""
    # TODO: Move this these into a common module, so we don't have to bury it like this.
    from .servers import set_database_ip
    execute(set_database_ip)

    if not package_exists('postgresql-9.1'):
        sudo('add-apt-repository ppa:pitti/postgresql')
        cuisine.package_install([
            'python-software-properties', 'postgresql-9.1', 'postgresql-contrib-9.1',
            'postgresql-server-dev-9.1', 'libpq-dev', 'libpq5'
        ], update=True)

    execute(update_db_conf)
    cuisine.user_ensure(env.db_user)
    sudo('/etc/init.d/postgresql restart')
    with settings(warn_only=True):
        sudo('''su postgres -c 'createdb -T template0 -O postgres -h %(db_ip)s -p %(db_port)s -E UTF8 %(db_name)s' ''' % env)


@task
@roles(DB_ROLE)
def backup_db():
    """Backup the database to the locations specified in env['db_backup_location']"""
    execute(set_database_ip)
    with settings(warn_only=True):
        sudo('mkdir -p %s' % env.db_backup_location)

    dump_cmd = "pg_dump  -a -h %(db_ip)s -p %(db_port)s %(db_name)s" % env
    sudo('su postgres -c "%s" > %sdata_%d.bak' % (dump_cmd, env.db_backup_location, time.time()))


