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
    # Heroku
    bottle.run(host='0.0.0.0', port=int(prod_port), server='gevent')
else:
    bottle.debug(True)
    bottle.run(host='localhost', port=8080)
