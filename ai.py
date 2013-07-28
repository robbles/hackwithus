import random

DEFAULT_STRATEGY = 'avoidance'

NORTH = 'n'
SOUTH = 's'
EAST = 'e'
WEST = 'w'

Wall = object()

ai_strategies = {}

def register_ai(name):
    def _register(cls):
        ai_strategies[name] = cls()
        return cls

    return _register

def get_ai(name):
    return ai_strategies.get(name, ai_strategies['random'])


class Strategy(object):

    def get_square(self, board, x, y):
        """ Get the contents of a square given its cartesian coordinates """
        return board[y][x]
    
    def get_surroundings(self, board, x, y):
        """ Get the contents of a square's neighbors given its cartesian coordinates """
        north = self.get_square(board, x, y-1) if y > 0 else Wall
        south = self.get_square(board, x, y+1) if y < len(board) - 1 else Wall
        west = self.get_square(board, x-1, y) if x > 0 else Wall
        east = self.get_square(board, x+1, y) if x < len(board[0]) - 1 else Wall

        return {
            NORTH: north,
            SOUTH: south,
            WEST: west,
            EAST: east
        }


@register_ai('north')
class Simple(Strategy):
    label = 'Default Strategy'

    def tick(self, game_id, client_id, turn_num, board, snakes, our_snake):
        return NORTH


@register_ai('random')
class Random(Strategy):
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


@register_ai('avoidance')
class Avoidance(Strategy):
    label = 'Avoidance Strategy'

    def safe_move(self, square):
        if square is Wall:
            return False

        if len(square) == 0:
            return True
        
        if square[0]['type'] == 'food':
            return True

        return False

    def tick(self, game_id, client_id, turn_num, board, snakes, my_snake):
        last_move = my_snake['last_move']
        if not last_move:
            last_move = NORTH

        posx, posy = my_snake['queue'][-1]

        surroundings = self.get_surroundings(board, posx, posy)

        # Go in same direction if nothing blocking
        if self.safe_move(surroundings[last_move]):
            return last_move

        # Can't go in same direction or in reverse, pick one of other two
        directions = {
            NORTH: [EAST, WEST],
            SOUTH: [EAST, WEST],
            WEST: [NORTH, SOUTH],
            EAST: [NORTH, SOUTH],
        }

        available = [direction for direction in directions[last_move] if self.safe_move(surroundings[direction])]
        print 'Available directions:'
        print available
        
        if not available:
            # We're screwed, just go north
            return NORTH

        return random.choice(available)



ai_strategies['default'] = ai_strategies[DEFAULT_STRATEGY]
