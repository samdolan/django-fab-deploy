from fabric.api import env, task
from .constants import WEB_ROLE, DB_ROLE

@task
def set_group(group_name):
    """Set the group of servers to operate on."""
    group_config = env.groups[group_name]
    set_role_defs(
        web=group_config['servers'][WEB_ROLE],
        db=group_config['servers'][DB_ROLE],
    )
    env.branch = group_config['branch']
    env.subdomain = group_config.get('subdomain', 'www')


def set_role_defs(web, db):
    def get_server_ips(l):
        return list(l.itervalues())

    env.hosts = get_server_ips(web) + get_server_ips(db)
    env.webservers = get_server_ips(web)

    env.roledefs = {
        WEB_ROLE: env.webservers,
        DB_ROLE: get_server_ips(db),
    }


