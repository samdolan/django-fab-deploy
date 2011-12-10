from fabric.api import *
from fabric.contrib.files import exists
from .constants import WEB_ROLE

@task
@roles(WEB_ROLE)
def get_source():
    # this doesnt seem like the right place for this, move into common
    from .django import deploy_user
    if not exists(env.repo_destination):
        deploy_user('git clone -b %(branch)s %(repo_remote_location)s %(repo_destination)s' % env)
    else:
        with cd(env.repo_destination):
            deploy_user('git reset --hard HEAD' % env)
            deploy_user('git clean -f -d' % env)
            deploy_user('git pull origin %(branch)s' % env)

