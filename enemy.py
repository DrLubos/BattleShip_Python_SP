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

                
                

    
class HardEnemy(Enemy):
    def __init__(self, boats, handler):
        super().__init__(boats, handler)
        self.last_hit = None
        self.direction = None

    def shoot(self):
        if self.last_hit is None:
            location = self.coords.pop(rand.randint(0, len(self.coords) - 1))
        else:
            location = self.get_next_location()

        self.last_hit = location
        self.handler.player_tiles[location[0]][location[1]].hitted()

    def get_next_location(self):
        row, col = self.last_hit

        if self.direction is None:
            self.direction = rand.choice(['up', 'down', 'left', 'right'])

        if self.direction == 'up':
            row -= 1
        elif self.direction == 'down':
            row += 1
        elif self.direction == 'left':
            col -= 1
        elif self.direction == 'right':
            col += 1

        if row < 0 or row >= board_size or col < 0 or col >= board_size or (row, col) not in self.coords:
            self.direction = None
            return self.get_next_location()

        self.coords.remove((row, col))
        return (row, col)


class HardEnemy(Enemy):
    def __init__(self, boats, handler):
        super().__init__(boats, handler)
        self.next_locations = []
        
    def calculate_shot(self):
        if len(self.next_locations) == 0:
            self.random_shot()
        else:
            self.neighbor_shot()
        
    def random_shot(self):
        location = self.coords.pop(rand.randint(0, len(self.coords) - 1))
        self.shoot(location[0], location[1])
        if self.handler.player_tiles[location[0]][location[1]].status == TileStatus.BOAT:
            self.next_locations.append((location[0], location[1] + 1))
            self.next_locations.append((location[0], location[1] - 1))
            self.next_locations.append((location[0] + 1, location[1]))
            self.next_locations.append((location[0] - 1, location[1]))
    
    def neighbor_shot(self):
        location = self.next_locations.pop(0)
        self.shoot(location[0], location[1])
        if self.handler.player_tiles[location[0]][location[1]].status == TileStatus.BOAT:
            if location[0] == self.next_locations[0][0]:
                self.next_locations.append((location[0], location[1] + 1))
                self.next_locations.append((location[0], location[1] - 1))
            else:
                self.next_locations.append((location[0] + 1, location[1]))
                self.next_locations.append((location[0] - 1, location[1]))
    
    def setup_shot(self):
        if len(self.next_locations) == 0:
            self.random_shot()
        else:
            self.neighbor_shot()
  
class NormalEnemy1(Enemy):
    def __init__(self, boats, handler):
        super().__init__(boats, handler)
        super().fill_coords()
        self.next_locations = []
        
    def calculate_shot(self):
        first_location = self.coords.pop(rand.randint(0, len(self.coords) - 1))
        self.shoot(first_location[0], first_location[1])
        # Ak trafil lod, pridaj susedne policka
        if self.handler.player_tiles[first_location[0]][first_location[1]].status == TileStatus.BOAT:
            # Vacsie indexy
            if first_location[0] < board_size - 1 and first_location[1] < board_size - 1:
                row_first = True if rand.randint(0, 1) == 0 else False
                next_location = (first_location[0] + 1, first_location[1]) if row_first else (first_location[0], first_location[1] + 1)
                self.coords.remove(next_location)
                self.next_locations.append(next_location)
            elif first_location[0] < board_size - 1:
                self.next_locations.append((first_location[0] + 1, first_location[1]))
            elif first_location[1] < board_size - 1:
                self.next_locations.append((first_location[0], first_location[1] + 1))
            # Mensie indexy
            if first_location[0] > 0 and first_location[1] > 0:
                row_first = True if rand.randint(0, 1) == 0 else False
                self.next_locations.append((first_location[0] - 1, first_location[1]) if row_first else (first_location[0], first_location[1] - 1))
            elif first_location[0] > 0:
                self.next_locations.append((first_location[0] - 1, first_location[1]))
            elif first_location[1] > 0:
                self.next_locations.append((first_location[0], first_location[1] - 1))
        
        # Inak geenruj nahodne policko
        else:
            next_location = self.coords[rand.randint(0, len(self.coords) - 1)]
            if next_location[0] == first_location[0] and not (next_location[1] == first_location[1] + 1 and next_location[1] == first_location[1] -1):
                self.next_locations.append(self.coords.pop(self.coords.index((next_location[0], next_location[1]))))
            elif next_location[1] == first_location[1] and not (next_location[0] == first_location[0] + 1 and next_location[0] == first_location[0] -1):
                self.next_locations.append(self.coords.pop(self.coords.index((next_location[0], next_location[1]))))
        # Vyberaj prve policko z listu
        first_list = self.next_locations.pop(0)
        # Ak to je lod, tak pridaj bud susedne riadky alebo stlpce
        if self.handler.player_tiles[first_list[0]][first_list[1]].status == TileStatus.BOAT:
            if first_location[0] == first_list[0]:
                if first_list[0] > 0:
                    self.next_locations.insert(0, (first_list[0] - 1, first_list[1]))
                if first_list[0] < board_size - 1:
                    self.next_locations.insert(0, (first_list[0] + 1, first_list[1]))
            else:
                if first_list[1] > 0:
                    self.next_locations.insert(0, (first_list[0], first_list[1] - 1))
                if first_list[1] < board_size - 1:
                    self.next_locations.insert(0, (first_list[0], first_list[1] + 1))
        self.shoot(first_list[0], first_list[1])
    
    def setup_shot(self):
        if len(self.next_locations) == 0:
            self.first_shot()
        else:
            self.calculate_shot()
        
    def first_shot(self):
        first_location = self.coords.pop(rand.randint(0, len(self.coords) - 1))
        self.shoot(first_location[0], first_location[1])
        # Ak trafil lod, pridaj susedne policka
        if self.handler.player_tiles[first_location[0]][first_location[1]].status == TileStatus.BOAT:
            # Vacsie indexy
            if first_location[0] < board_size - 1 and first_location[1] < board_size - 1:
                row_first = True if rand.randint(0, 1) == 0 else False
                next_location = (first_location[0] + 1, first_location[1]) if row_first else (first_location[0], first_location[1] + 1)
                self.coords.remove(next_location)
                self.next_locations.append(next_location)
            elif first_location[0] < board_size - 1:
                self.next_locations.append((first_location[0] + 1, first_location[1]))
            elif first_location[1] < board_size - 1:
                self.next_locations.append((first_location[0], first_location[1] + 1))
            # Mensie indexy
            if first_location[0] > 0 and first_location[1] > 0:
                row_first = True if rand.randint(0, 1) == 0 else False
                self.next_locations.append((first_location[0] - 1, first_location[1]) if row_first else (first_location[0], first_location[1] - 1))
            elif first_location[0] > 0:
                self.next_locations.append((first_location[0] - 1, first_location[1]))
            elif first_location[1] > 0:
                self.next_locations.append((first_location[0], first_location[1] - 1))
        
    def shoot(self, row, col):
        self.handler.player_tiles[row][col].hitted()