from fabric.api import *
from .constants import WEB_ROLE
from .supervisor import install_supervisor
from .ssh import setup_repo_key
from .nginx import install_nginx
from .git import get_source
from .django import install_settings, setup_python_env, update_python_libs, update_db
import cuisine

@task
@roles(WEB_ROLE)
def setup_web():
    """Setup a web server."""
    from .servers import setup_common
    from .servers import setup_run_dirs

    #execute(setup_common)
    from fabric.colors import yellow
    print yellow("Setting up web user.")

    execute(get_source)
    execute(setup_python_env)
    execute(update_python_libs)
    execute(install_settings)
    execute(update_db)
    execute(setup_run_dirs)
    execute(install_supervisor)
    sudo('ufw allow 80/tcp')
    sudo('ufw allow 443/tcp')

    execute(install_nginx)

