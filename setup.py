import re

from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages

REQUIREMENTS_FILE = 'requirements.pip'

# requirements parsing from https://github.com/cburgmer/pdfserver/blob/master/setup.py
def parse_requirements(file_name):
    requirements = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'(\s*#)|(\s*$)', line):
            continue
        if re.match(r'\s*-e\s+', line):
            # TODO support version numbers
            requirements.append(re.sub(r'\s*-e\s+.*#egg=(.*)$', r'\1', line))
        elif re.match(r'\s*-f\s+', line):
            pass
        else:
            requirements.append(line)

    return requirements

def parse_dependency_links(file_name):
    dependency_links = []
    for line in open(file_name, 'r').read().split('\n'):
        if re.match(r'\s*-[ef]\s+', line):
            dependency_links.append(re.sub(r'\s*-[ef]\s+', '', line))

    return dependency_links


setup(
    name = "django-fab-deploy",
    version = "0.1",
    packages = find_packages(),
    author = "Sam Dolan",
    author_email = "samdolan@gmail.com",
    description = "A set of fabric deployment scripts for django setups.",
    url = "https://github.com/samdolan/django-fab-deploy",
    install_requires = parse_requirements(REQUIREMENTS_FILE),
    dependency_links = parse_dependency_links(REQUIREMENTS_FILE),
)

