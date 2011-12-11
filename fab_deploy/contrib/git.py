from fabric.api import *
from fabric.contrib.files import exists
from .constants import WEB_ROLE
from .ssh import setup_repo_key

import cuisine

@task
@roles(WEB_ROLE)
def get_source():
    cuisine.user_ensure(env.deploy_user,
                    home=env.deploy_user_home,
                    shell='/bin/bash')

    execute(setup_repo_key)

    # this doesnt seem like the right place for this, move into common
    from .django import deploy_user
    if not exists(env.repo_destination):
        run('sudo -i -H -u web git clone -b %(branch)s %(repo_remote_location)s %(repo_destination)s' % env)
    else:
        with cd(env.repo_destination):
            deploy_user('git reset --hard HEAD' % env)
            deploy_user('git clean -f -d' % env)
            deploy_user('git pull origin %(branch)s' % env)

