#!/usr/bin/env python3

import os
from fabric import api


FAB_ENV = {
    'host_string': 'get-sleepy.com',
    'user': 'root',
    # 'warn_only' : True,
    'key_filename': os.path.join('/home/su/.ssh', 'id_rsa')
}
api.env.update(FAB_ENV)


# update server code base
def sync():
    with api.cd('/opt/django-apps/sleepy'), api.prefix('source /opt/env/sleepy/bin/activate'):
        api.run('git pull')
        api.run('pip install -r requirements.txt')
        api.run('./manage.py migrate')
        api.run('./manage.py collectstatic --no-input')
        # TODO uncommite the below row after adding translation
        # api.run('./manage.py compilemessages -l ru -l en')
        api.run('touch /opt/uwsgi/run/sleepy.reload')
        # api.run('./manage.py test_urls')


if __name__ == '__main__':
    sync()
