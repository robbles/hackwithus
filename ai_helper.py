from random import choice

class SnakeAIs:
    def __init__(self, board, snakes):
        self.board = board
        self.snakes = snakes
        self.nrows = 0
        self.ncols = 0
        self.getBoardDimensions()
        self.DEBUG = True

    #get the size of board
    def getBoardDimensions(self):
        self.nrows = len(self.board)
        self.ncols = len(self.board[0])
        
    #check if we can move from current pos=[x, y] in direction
    #west:w, east:e, nort:n, south:s
    def checkSquare(self, pos, direction):
        x = pos[0]
        y = pos[1]
        if self.DEBUG:
            print "current loc = (x=%d, y=%d)" % (x, y)
        if direction == "n":
            y -= 1
        elif direction == "s":
            y += 1
        elif direction == "e":
            x += 1
        else:
            x -= 1
        if self.DEBUG:
            print "dir: %s" % direction
            print "move to x=%d, y=%d" % (x, y)
        valid = True
        #check the boundaries
        if (x >= self.ncols or x < 0) or (y >= self.nrows or
                                                     y < 0):
            valid = False
            if self.DEBUG:
                print "out of boundaries!!"
        #check if there is snake on that cell
        cell = self.board[y][x]
        if valid and cell:
            if cell[0]["type"] == "snake":
                valid = False
            if self.DEBUG:
                print "occupied cell"

        return valid
    
    #random AI - takes the current position and tries to move in a random
    #direction by just avoiding forbidden squares
    #pos = [x, y] current head location
    def randomAI(self, pos):
        possible_directions = []
        if self.checkSquare(pos, "n"):
            possible_directions.append("n")
        if self.checkSquare(pos, "s"):
            possible_directions.append("s")
        if self.checkSquare(pos, "e"):
            possible_directions.append("e")
        if self.checkSquare(pos, "w"):
            possible_directions.append("w")
        
        if self.DEBUG:
            print "possible directions"
            print possible_directions
        
        direction = choice(possible_directions)
        if self.DEBUG:
            print "random: go to %s" % direction
        return direction

    #given two positions in the format of lists [x, y]
    #returns Manhatan distance
    def getManDist(self, pos1, pos2):
        return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))
    #a method which just fins the closest food
    #given board and head location in pos = [x, y]
    def getClosestFood(self, pos):
        #iterate the board and find all foods locations
        food_locs = []
        for row in range(0, self.nrows):
            for col in range(0, self.ncols):
                square = self.board[row][col]
                if square:
                    #print square
                    if square[0]["type"] == "food":
                        fpos = [col, row]
                        food_locs.append(fpos)
        if self.DEBUG:
            print "food locs:"
            print food_locs
        #let's find the closest food based on manhatan dist
        min_dist = 100000000
        closest_food = []
        for fpos in food_locs:
            dist = self.getManDist(pos, fpos)
            if dist < min_dist:
                min_dist = dist
                closest_food = fpos
        if self.DEBUG:
            print "closest food:"
            print closest_food
        possible_directions = []
        #compare x's
        if closest_food[0] > pos[0]:
            possible_directions.append("e")
        elif closest_food[0] < pos[0]:
            possible_directions.append("w")
        #compare y's
        if closest_food[1] > pos[1]:
            possible_directions.append("n")
        elif closest_food[1] < pos[1]:
            possible_directions.append("s")
        print possible_directions
        direction = choice(possible_directions)
        print direction

def main():
    #board setting
    board = [ [
                  [{
                     "type": "snake_head",
                      "id": "e287ad13-b8e2-4b4e-bc1f-57ce613da2ee"
                   }
                  ],
                  [{
                   "type" : "food",
                   "id": "66b2fe91-6595-483a-a953-b2c7f83ee1da"
                  }
                  ],
                  [], 
                  []
               ],     
               [
                  [],
                  [{
                  "type": "snake",
                  "id": "e287ad13-b8e2-4b4e-bc1f-57ce613da2ee"
                  }
                  ],
                  [],
                  []
                ],
                [
                  [
                  {
                  "type": "food",
                  "id": "66b2fe91-6595-483a-a953-b2c7f83ee1df"
                  }
                  ],
                  [],
                  [],
                  []
                 ]
            ]
    #snakes descriptions
    snakes = [{
                "status": "alive",
                "stats": {
                            "food": 1,
                            "life": 0,
                            "kills": 0
                          },
                "name": "Local Snake",
                "last_move": "w",
                "queue": [
                            [
                              0,
                              1
                            ],
                            [
                              0,
                              0
                            ]
                          ],
                  "message": "",
                  "id": "e287ad13-b8e2-4b4e-bc1f-57ce613da2ee",
                  "ate_last_turn": False
                }]

    #create the AI object
    ai = SnakeAIs(board, snakes)
    #get dimensions of the board
    ai.getBoardDimensions()
    print "(rows=%d, cols=%d)" % (ai.nrows, ai.ncols)
    #pos = [0, 0]
    #direction = "w"
    #if ai.checkSquare(pos, direction):
    #    print "valid move!"
    #else:
    #    print "not valid move!!!"
    #play random moves
    pos = [0, 0]    #head position
    ai.randomAI(pos)
    ai.getClosestFood(pos)

if __name__ == '__main__':
        main()
