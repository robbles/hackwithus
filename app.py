# Required to make bottle work with gevent
import gevent.monkey
gevent.monkey.patch_all()

import bottle
import os


@bottle.route('/')
def index():
    return "Hello SnakWasdforld"


# Runserver

is_production = os.environ.get('POST', None)

if is_production:
    bottle.run(server='gevent', port=os.environ.get('PORT', 5000))
else:
    bottle.debug(True)
    bottle.run(host='localhost', port=8080)
