import bottle
import json
import os
import random

import ai

def _respond(response_json):
    return json.dumps(response_json)

@bottle.get('/images/<filename>')
def send_image(filename):
    return bottle.static_file(filename, root='static/img', mimetype='image/jpg')


@bottle.post('/<ai_name>/register')
def register(ai_name):
    strategy = ai.get_ai(ai_name)    

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- REGISTER ---", strategy.label
    print "Game ID:", request.get('game_id')
    print "Client ID:", request.get('client_id')
    print "Board:"
    print "  Width:", request.get('board').get('width')
    print "  Height:", request.get('board').get('height')
    print "----------------"

    return _respond({
        'name': strategy.label,
        'img_url': "https://secure.gravatar.com/avatar/a4c3a996a2b224de62d5c2aae1f2760b?s=50",
        'head_img_url': "https://secure.gravatar.com/avatar/a4c3a996a2b224de62d5c2aae1f2760b?s=50",
    })


@bottle.post('/<ai_name>/start')
def start(ai_name):
    strategy = ai.get_ai(ai_name)

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- START ---", strategy.label
    print "Game ID:", request.get('game_id')
    print "Num Players:", request.get('num_players')
    print "-------------"

    return _respond({})


@bottle.post('/<ai_name>/tick/<client_id>')
def tick(ai_name, client_id):
    strategy = ai.get_ai(ai_name)

    request = bottle.request.json
    if not request:
        return "No request data sent"

    turn_num = request.get('turn_num')
    game_id = request.get('id')
    snakes = request.get('snakes')
    board = request.get('board')

    print "--- TICK", turn_num, '---', strategy.label
    print "Game ID:", game_id
    print "Turn Num:", turn_num
    print "Snakes:", len(snakes)
    print "----------------"

    # Find the last move we made
    my_snake = None
    for snake in request.get('snakes'):
        if snake['id'] == client_id:
            my_snake = snake
            continue
    if not my_snake:
        print 'ERROR: could not found our snake in request!'
        return 'No snake for client ID', client_id

    move = strategy.tick(game_id, client_id, turn_num, board, snakes, my_snake)

    print "Moving in direction:", move

    return _respond({
        'move': move,
        'message': 'Turn %d!' % turn_num
    })


@bottle.post('<ai_name>/end')
def end(ai_name):
    strategy = ai.get_ai(ai_name)

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- END ---", strategy.label
    print "Game ID:", request.get('game_id')
    print "-------------"

    return _respond({})


