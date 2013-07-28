import bottle
import json
import os
import random

def _respond(response_json):
    return json.dumps(response_json)


def map_ai(ai_mode):
    if ai_mode not in ['sq', 'n', 's', 'e', 'w']:
        return 'r'
    return ai_mode


@bottle.post('/<ai_mode>/register')
def register(ai_mode):
    ai_mode = map_ai(ai_mode)

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- REGISTER ---", str(ai_mode)
    print "Game ID:", request.get('game_id')
    print "Client ID:", request.get('client_id')
    print "Board:"
    print "  Width:", request.get('board').get('width')
    print "  Height:", request.get('board').get('height')
    print "----------------"

    ai_names = {
        'sq': 'Square Snake',
        'n': 'North Snake',
        's': 'South Snake',
        'e': 'East Snake',
        'w': 'West Snake',
        'r': 'RaNd0m Sn4K3'
    }

    return _respond({
        'name': ai_names[ai_mode],
        'img_url': "https://secure.gravatar.com/avatar/a4c3a996a2b224de62d5c2aae1f2760b?s=50"
    })


@bottle.post('/<ai_mode>/start')
def start(ai_mode):
    ai_mode = map_ai(ai_mode)

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- START ---", str(ai_mode)
    print "Game ID:", request.get('game_id')
    print "Num Players:", request.get('num_players')
    print "-------------"

    return _respond({})


@bottle.post('/<ai_mode>/tick/<client_id>')
def tick(ai_mode, client_id):
    ai_mode = map_ai(ai_mode)

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- TICK", request.get('turn_num'), '---', str(ai_mode)
    print "Game ID:", request.get('id')
    print "Turn Num:", request.get('turn_num')
    print "Snakes:", len(request.get('snakes'))
    # print request.get('board')
    print "----------------"
    print client_id
    print request.get('snakes')

    # Find the last move we made
    for snake in request.get('snakes'):
        if snake['id'] == client_id:
            my_snake = snake
            continue

    random_map = {
        'n': [random.choice(['n', 'e', 'w'])],
        's': [random.choice(['s', 'e', 'w'])],
        'w': [random.choice(['n', 's', 'w'])],
        'e': [random.choice(['n', 's', 'e'])],
        '': [random.choice(['n', 's', 'e', 'w'])]
    }
    r_choices = random_map[my_snake['last_move']]

    modes = {
        'sq': ['n', 'n', 'w', 'w', 's', 's', 'e', 'e'],
        'n': ['n'],
        's': ['n'],
        'e': ['e'],
        'w': ['w'],
        'r': r_choices
    }

    # Map
    moves = modes[ai_mode]
    my_move = moves[request.get('turn_num') % len(moves)]

    return _respond({
        'move': my_move,
        'message': 'Turn %d!' % (request.get('turn_num'))
    })


@bottle.post('<ai_mode>/end')
def end(ai_mode):
    ai_mode = map_ai(ai_mode)

    request = bottle.request.json
    if not request:
        return "No request data sent"

    print "--- END ---", str(ai_mode)
    print "Game ID:", request.get('game_id')
    print "-------------"

    return _respond({})


