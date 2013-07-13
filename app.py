# Required to make bottle work with gevent
import gevent.monkey
gevent.monkey.patch_all()

import bottle
import json
import os
import random


def _respond(response_json):
    return json.dumps(response_json)


@bottle.route('/register')
def register():
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- REGISTER ---"
    print "Game ID:", request.get('game_id')
    print "Snake ID:", request.get('snake_id')
    print "Board:"
    print "  Width:", request.get('width')
    print "  Height:", request.get('height')
    print "  Num Players:", request.get('num_players')
    print "----------------"

    return _respond({
        'name': 'Example Snake',
        'img_url': "https://secure.gravatar.com/avatar/a4c3a996a2b224de62d5c2aae1f2760b?s=50"
    })


@bottle.route('/start')
def start():
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- START ---"
    print "Game ID:", request.get('game_id')
    print "-------------"

    return _respond({})


@bottle.route('/tick')
def tick():
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- TICK", request.get('turn_num'), '---'
    print "Game ID:", request.get('game_id')
    print "Snake ID:", request.get('snake_id')
    print "Turn Num:", request.get('turn_num')
    print "Snakes:", len(request.get('snakes'))
    print "----------------"

    # Find the last move we made
    for snake in request.get('snakes'):
        if snake['id'] == request.get('snake_id'):
            my_snake = snake

    # Map
    allowed_moves = {
        'n': ['n', 'e', 'w'],
        's': ['s', 'e', 'w'],
        'e': ['e', 'n', 's'],
        'w': ['w', 'n', 's']
    }
    my_move = random.choice(allowed_moves[my_snake['last_move']])

    return _respond({
        'move': my_move,
        'message': 'Turn %d!' % (request.get('turn_num'))
    })


@bottle.route('/end')
def end():
    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- END ---"
    print "Game ID:", request.get('game_id')
    print "-------------"

    return _respond({})


## Runserver ##

prod_port = os.environ.get('PORT', None)

if prod_port:
    # Assume Heroku
    bottle.run(host='0.0.0.0', port=int(prod_port), server='gevent')
else:
    # Localhost
    bottle.debug(True)
    bottle.run(host='localhost', port=8080)
