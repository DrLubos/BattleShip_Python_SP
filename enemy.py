from enums_constants import TileStatus, board_size
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
        self.setup_boats()
        
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
                
class NormalEnemy(Enemy):
    def __init__(self, boats, handler):
        super().__init__(boats, handler)
        rand.shuffle(self.coords)
        self.up, self.down, self.left, self.right = True, True, True, True
        self.reset_location = None
        
    def shoot(self):
        location = self.coords.pop(0)
        if self.handler.player_tiles[location[0]][location[1]].status == TileStatus.BOAT and not self.reset_location:
            row_first = rand.choice([True, False])
            if row_first:
                index_iterator = self.shoot_rows(location)
                index_iterator = self.shoot_cols(location, index_iterator)
            else:
                index_iterator = self.shoot_cols(location)
                index_iterator = self.shoot_rows(location, index_iterator)
            self.reset_location = self.coords[index_iterator - 1]
        self.handler.player_tiles[location[0]][location[1]].hitted()
        if location == self.reset_location:
            self.up, self.down, self.left, self.right = True, True, True, True
            self.reset_location = None
            
    def shoot_rows(self, location, index_iterator = 0):
        row = location[0]
        iterator = 1
        while (row - iterator, location[1]) in self.coords and self.up:
            index = self.coords.index((row - iterator, location[1]))
            self.coords.insert(0 + index_iterator, self.coords.pop(index))
            if iterator > 1:
                self.left = False
                self.right = False
            if self.handler.player_tiles[row - iterator][location[1]].status != TileStatus.BOAT:
                self.up = False
                index_iterator += 1
                break
            iterator += 1
            index_iterator += 1
        row = location[0]
        iterator = 1
        while (row + iterator, location[1]) in self.coords and self.down:
            index = self.coords.index((row + iterator, location[1]))
            self.coords.insert(0 + index_iterator, self.coords.pop(index))
            if iterator > 1:
                self.left = False
                self.right = False
            if self.handler.player_tiles[row + iterator][location[1]].status != TileStatus.BOAT:
                self.down = False
                index_iterator += 1
                break
            iterator += 1
            index_iterator += 1
        return index_iterator
    
    def shoot_cols(self, location, index_iterator = 0):
        col = location[1]
        iterator = 1
        while (location[0], col - iterator) in self.coords and self.left:
            index = self.coords.index((location[0], col - iterator))
            self.coords.insert(0 + index_iterator, self.coords.pop(index))
            if iterator > 1:
                self.up = False
                self.down = False
            if self.handler.player_tiles[location[0]][col - iterator].status != TileStatus.BOAT:
                self.left = False
                index_iterator += 1
                break
            iterator += 1
            index_iterator += 1
        col = location[1]
        iterator = 1
        while (location[0], col + iterator) in self.coords and self.right:
            index = self.coords.index((location[0], col + iterator))
            self.coords.insert(0 + index_iterator, self.coords.pop(index))
            if iterator > 1:
                self.up = False
                self.down = False
            if self.handler.player_tiles[location[0]][col + iterator].status != TileStatus.BOAT:
                self.right = False
                index_iterator += 1
                break
            iterator += 1
            index_iterator += 1
        return index_iterator

class HardEnemy(NormalEnemy):
    def __init__(self, boats, handler):
        super().__init__(boats, handler)
        
    def shoot(self):
        location = self.coords.pop(0)
        if location == self.reset_location:
            self.up, self.down, self.left, self.right = True, True, True, True
            self.reset_location = None
        if self.handler.player_tiles[location[0]][location[1]].status == TileStatus.EMPTY:
            if rand.random() < 0.7:
                self.coords.append(location)
                self.shoot()
                return
        if self.handler.player_tiles[location[0]][location[1]].status == TileStatus.BOAT and not self.reset_location:
            row_first = rand.choice([True, False])
            if row_first:
                index_iterator = super().shoot_rows(location)
                index_iterator = super().shoot_cols(location, index_iterator)
            else:
                index_iterator = super().shoot_cols(location)
                index_iterator = super().shoot_rows(location, index_iterator)
            self.reset_location = self.coords[index_iterator - 1]
        self.handler.player_tiles[location[0]][location[1]].hitted()