#!/usr/bin/env python

import bottle
import os

import app

prod_port = os.environ.get('PORT', None)

if prod_port:
    # Assume Heroku
    bottle.run(host='0.0.0.0', port=int(prod_port))
else:
    # Localhost
    bottle.debug(True)
    bottle.run(host='', port=8080)
