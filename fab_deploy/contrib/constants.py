import os

# HOSTS
#
WEB_ROLE = 'web'
DB_ROLE = 'db'
ALL_ROLES = [DB_ROLE, WEB_ROLE]

FABFILE_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(os.path.join(__file__), os.pardir, os.pardir))
CONF_DIR = os.path.join(REPO_ROOT, 'conf')

