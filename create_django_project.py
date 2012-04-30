#!/usr/bin/env python
import os
import sys
import string
from string import Template

if len(sys.argv) != 3:
    print 'Usage: ./create-django-script.py <projectName> <domainName>'
    sys.exit(1)

def _write_string(t):
    f = open(t[0], "w")
    f.write(t[1])
    f.flush()
    f.close()

def _get_install(env):
    s = Template("""
#!/bin/bash
cd ..
virtualenv .
source bin/activate
cd $project_name
# echo "$project_name.settings.$env" > .django-settings
pip install -r setup/requirements.txt
python manage.py syncdb --settings=taskie.settings.$env
python manage.py migrate tasks --settings=taskie.settings.$env
python manage.py migrate more_info --settings=taskie.settings.#env
    """)
    val = s.substitute(project_name=PROJECT_NAME, env=env)
    return ('$s-install.sh', val)

PROJECT_NAME = string.lower(sys.argv[1])
DOMAIN_NAME = string.lower(sys.argv[2])
PROJECT_DIRS = [
        'backup',
        'bin',
        'cache',
        'include',
        'lib',
        'local',
        'logs',
        'pid',
        'share',
        PROJECT_NAME,
        'tmp',
        'uploads',
    ]
NOT_GIT_IGNORED = [
        PROJECT_NAME,
]

os.mkdir(DOMAIN_NAME)
for dir in PROJECT_DIRS:
    os.mkdir(os.path.join(DOMAIN_NAME, dir))

_write_string(_get_install('prod'))
_write_string(_get_install('dev'))

