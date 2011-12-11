from fabric.api import *
from .constants import DB_ROLE
from .postgres import install_postgres
from .django import update_db, setup_python_env, update_python_libs
from .git import get_source

@task
@roles(DB_ROLE)
def setup_db():
    from .servers import setup_common
    execute(setup_common)
    execute(get_source)
    execute(install_postgres)


