from fabric.api import *
from .constants import WEB_ROLE
import cuisine
import os

def get_our_key():
    """Get our local ssh key."""
    the_key = None
    with open(os.path.expanduser(env.our_key_path)) as key:
        the_key = key.read()
    return the_key

@task
@runs_once
def setup_ssh_key():
    """Install your ssh key for the root user on all hosts."""
    with settings(warn_only=True):
        sudo('mkdir /root/.ssh/')
    cuisine.ssh_authorize(env.user, get_our_key())


@task
@roles(WEB_ROLE)
def setup_repo_key():
    if env.get('repo_private_key') and env.get('repo_public_key'):
        ssh_dir = '%(deploy_user_home)s.ssh' % env
        with settings(warn_only=True):
            from .django import deploy_user

            deploy_user('mkdir %s' % ssh_dir)

        sudo('chown -R %s: %s' % (env.deploy_user, ssh_dir))
        put(env.repo_private_key, '%s/id_rsa' % ssh_dir, use_sudo=True)
        put(env.repo_public_key, '%s/id_rsa.pub' % ssh_dir, use_sudo=True)
        sudo('chown -R %s: %s' % (env.deploy_user, ssh_dir))
        sudo('chmod 700 %s' % ssh_dir)
        sudo('chmod 600 %s/*' % ssh_dir)
