import random

NORTH = 'n'
SOUTH = 's'
EAST = 'e'
WEST = 'w'

ai_strategies = {}

def register_ai(name):
    def _register(cls):
        ai_strategies[name] = cls()
        return cls

    return _register

def get_ai(name):
    return ai_strategies.get(name, ai_strategies['random'])


@register_ai('north')
class SimpleStrategy(object):
    label = 'Default Strategy'

    def tick(self, game_id, client_id, turn_num, board, snakes, our_snake):
        return NORTH


@register_ai('random')
class RandomStrategy(SimpleStrategy):
    label = 'Random Strategy'

    def tick(self, game_id, client_id, turn_num, board, snakes, my_snake):
        random_map = {
            NORTH: random.choice([NORTH, EAST, WEST]),
            SOUTH: random.choice([SOUTH, EAST, WEST]),
            WEST: random.choice([NORTH, SOUTH, WEST]),
            EAST: random.choice([NORTH, SOUTH, EAST]),
            '': random.choice([NORTH, SOUTH, EAST, WEST]),
        }
        return random_map[my_snake['last_move']]


register_ai('default')(RandomStrategy)
