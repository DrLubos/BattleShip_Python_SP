from enums_constants import board_size
from boat import Boat
import random as rand

class Enemy:
    def __init__(self, boats, handler):
        self.boats = []
        self.handler = handler
        for boat in boats:
            self.boats.append(Boat(boat.length, None))
        self.coords = []
        self.fill_coords()
        
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
        location = self.coords.pop(rand.randint(0, len(self.coords) - 1))
        self.handler.player_tiles[location[0]][location[1]].hitted()
    
    def fill_coords(self):
        for row in range(board_size):
            for col in range(board_size):
                self.coords.append((row, col))