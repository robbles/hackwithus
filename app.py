# Required to make bottle work with gevent
import gevent.monkey
gevent.monkey.patch_all()

import bottle
import os


@bottle.route('/')
def index():
    return "Hello SnakWasdforld"


# Runserver

prod_port = os.environ.get('PORT', None)

if prod_port:
    bottle.run(server='gevent', port=prod_port)
else:
    bottle.debug(True)
    bottle.run(host='localhost', port=8080)
