from enums_constants import board_size, TileStatus
from boat import Boat
import random as rand

class Enemy:
    def __init__(self, boats, handler):
        self.boats = []
        self.handler = handler
        for boat in boats:
            self.boats.append(Boat(boat.length, None))
        
    def setup_boats(self):
        for boat in self.boats:
            location = self.generate_location()
            self.handler.active_boat = boat
            if location[2] == 1:
                self.handler.active_boat.rotate()
            while not self.handler.check_boat_placement(location[0], location[1], False, True):
                location = self.generate_location()
            self.handler.active_boat = None
            
    def generate_location(self):
        rotation = rand.randint(0, 1)
        row = rand.randint(0, board_size - 1)
        col = rand.randint(0, board_size - 1)
        return (row, col, rotation)
    
    def shoot(self):
        location = self.generate_location()
        while self.handler.player_tiles[location[0]][location[1]].status == TileStatus.HIT or self.handler.player_tiles[location[0]][location[1]].status == TileStatus.MISS:
            location = self.generate_location()
        self.handler.player_tiles[location[0]][location[1]].hitted()