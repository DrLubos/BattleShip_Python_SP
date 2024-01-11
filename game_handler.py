from boat import Boat
from enums_constants import *
from tile import Tile
from enemy import Enemy

import arcade

class Handler(arcade.Window):
    def __init__(self, title):
        super().__init__(win_width, win_height, title)
        self.background = arcade.load_texture("./assets/bg.jpg")
        self.cloud = arcade.load_texture("./assets/cloud.png")
        self.fire = arcade.load_texture("./assets/fire.png")
        self.missed = arcade.load_texture("./assets/missed.png")
        self.player_tiles = [[Tile(row, col, win_width, win_height, self, enemy=False) for col in range(board_size)] for row in range(board_size)]
        self.enemy_tiles = [[Tile(row, col, win_width, win_height, self, enemy=True) for col in range(board_size)] for row in range(board_size)]
        self.fire_coords = []
        self.miss_coords = []
        self.boats = []
        self.hitpoints = 0
        self.enemy_hitpoints = 0
        self.active_tile = None
        self.active_boat = None
        self.game_status = False
        self.placed_boats = 0
        self.player_move = True
        self.set_up_boats()
        self.enemy = Enemy(self.boats, self)
        self.enemy.setup_boats()
        self.frame = 0

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, win_width, win_width, self.background)
        self.draw_tiles(self.player_tiles)
        self.draw_tiles(self.enemy_tiles)
        self.load_boats()
        self.display_enemy_hits()
        self.frame += 1
        if self.frame % 3 == 0:
            if self.game_status and not self.player_move:
                self.enemy.shoot()
                self.player_move = True
                
    def on_mouse_press(self, x, y, button, modifiers):
        if self.game_status and self.player_move and self.active_tile:
            if self.active_tile.enemy and (self.active_tile.status == TileStatus.EMPTY or self.active_tile.status == TileStatus.BOAT):
                if self.active_tile.status == TileStatus.BOAT:
                    self.enemy_hitpoints -= 1
                self.active_tile.hitted()
                self.active_tile = None
                self.player_move = False
            #arcade.cleanup_texture_cache()
        if not self.game_status and not self.active_boat:
            for boat in self.boats:
                if (
                    x >= boat.left_up_x
                    and x <= boat.left_up_x + square_length
                    and y <= boat.left_up_y
                    and y >= boat.left_up_y - square_length * boat.length
                ):
                    self.active_boat = boat
                    self.active_boat.alpha = 170
        if not self.game_status and self.active_boat and x < win_width / 2:
            boat_placement_tile = self.get_mouse_tile(x, y, self.player_tiles)
            if isinstance(boat_placement_tile, Tile): 
                lower_index = False
                if ((self.active_boat.angle == 0 and boat_placement_tile.square.y + square_length / 2 < y) 
                    or (self.active_boat.angle != 0 and boat_placement_tile.square.x + square_length / 2 > x)):
                    lower_index = True
                if self.check_boat_placement(boat_placement_tile.row, boat_placement_tile.col, lower_index):
                    self.place_boat(boat_placement_tile, lower_index)
                    self.placed_boats += 1
                    if self.placed_boats == len(self.boats):
                        self.game_status = True
        
    def on_mouse_motion(self, x, y, dx, dy):
        if self.active_boat:
            self.active_boat.draw(x,y)
        new_tile = None
        if x < win_width / 2:
            new_tile = self.get_mouse_tile(x, y, self.player_tiles)
        elif x > win_width / 2 and not self.active_boat:
            new_tile = self.get_mouse_tile(x, y, self.enemy_tiles)
        if new_tile:
            if self.active_tile and self.active_tile != new_tile:
                self.active_tile.reset_color()
            new_tile.change_color()
            self.active_tile = new_tile
        else:
            if self.active_tile:
                self.active_tile.reset_color()
            self.active_tile = None
    
    def on_close(self):
        self.active_tile = None
        arcade.cleanup_texture_cache()
        super().on_close()
        
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R and self.active_boat:
            self.active_boat.rotate()
            
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT and self.active_boat:
            self.active_boat.rotate()
        
    def set_up_boats(self):
        self.boats = [
                Boat(5, "./assets/ship1.png"),
                #Boat(4, "./assets/ship3.png"),
                #Boat(4, "./assets/ship2.png"),
                #Boat(3, "./assets/ship4.png"),
                #Boat(3, "./assets/ship5.png"),
                #Boat(2, "./assets/ship6.png"),
                #Boat(2, "./assets/ship7.png"),
            ]
        index = 1
        for lod in self.boats:
            lod.draw(index * (square_length * 1 + 20), None)
            self.hitpoints += lod.length
            index += 1
        self.enemy_hitpoints = self.hitpoints

    def load_boats(self):
        for boat in self.boats:
            boat.draw(None, None)
    
    def get_mouse_tile(self, x, y, tile_list):
        for row in tile_list:
            for tile in row:
                if isinstance(tile, Tile):
                    if (
                        x >= tile.square.x
                        and x < tile.square.x + square_length
                        and y >= tile.square.y
                        and y < tile.square.y + square_length
                    ):
                        return tile
        return None        
    
    def draw_tiles(self, tile_list):
        for row in tile_list:
            for tile in row:
                if isinstance(tile, Tile):
                    tile.square.draw()
                    
    def check_boat_placement(self, row, col, lower_index=False, enemy_check=False):
        if self.active_boat.length % 2 == 0:
            if self.active_boat.angle == 270:
                if lower_index:
                    polovica = self.active_boat.length // 2
                    col -= polovica
                    if col < 0 or col + self.active_boat.length > board_size:
                        return False
                    for i in range(col, col + self.active_boat.length):
                        if not enemy_check:
                            if self.player_tiles[row][i].status != TileStatus.EMPTY:
                                return False
                        else:
                            if self.enemy_tiles[row][i].status != TileStatus.EMPTY:
                                return False
                    for i in range(col, col + self.active_boat.length):
                        if not enemy_check:
                            self.player_tiles[row][i].status = TileStatus.BOAT
                        else:
                            self.enemy_tiles[row][i].status = TileStatus.BOAT
                            self.enemy_tiles[row][i].square.color = arcade.color.PURPLE
                    return True
                else:
                    polovica = self.active_boat.length // 2
                    col = col - polovica + 1
                    if col < 0 or col + self.active_boat.length > board_size:
                        return False
                    for i in range(col, col + self.active_boat.length):
                        if not enemy_check:
                            if self.player_tiles[row][i].status != TileStatus.EMPTY:
                                return False
                        else:
                            if self.enemy_tiles[row][i].status != TileStatus.EMPTY:
                                return False
                    for i in range(col, col + self.active_boat.length):
                        if not enemy_check:
                            self.player_tiles[row][i].status = TileStatus.BOAT
                        else:
                            self.enemy_tiles[row][i].status = TileStatus.BOAT
                            self.enemy_tiles[row][i].square.color = arcade.color.PURPLE
                    return True
            else:
                if lower_index:
                    polovica = self.active_boat.length // 2
                    row -= polovica
                    if row < 0 or row + self.active_boat.length > board_size:
                        return False
                    for i in range(row, row + self.active_boat.length):
                        if not enemy_check:
                            if self.player_tiles[i][col].status != TileStatus.EMPTY:
                                return False
                        else:
                            if self.enemy_tiles[i][col].status != TileStatus.EMPTY:
                                return False
                    for i in range(row, row + self.active_boat.length):
                        if not enemy_check:
                            self.player_tiles[i][col].status = TileStatus.BOAT
                        else:
                            self.enemy_tiles[i][col].status = TileStatus.BOAT
                            self.enemy_tiles[i][col].square.color = arcade.color.PURPLE
                    return True
                else:
                    polovica = self.active_boat.length // 2
                    row = row - polovica + 1
                    if row < 0 or row + self.active_boat.length > board_size:
                        return False
                    for i in range(row, row + self.active_boat.length):
                        if not enemy_check:
                            if self.player_tiles[i][col].status != TileStatus.EMPTY:
                                return False
                        else:
                            if self.enemy_tiles[i][col].status != TileStatus.EMPTY:
                                return False
                    for i in range(row, row + self.active_boat.length):
                        if not enemy_check:
                            self.player_tiles[i][col].status = TileStatus.BOAT
                        else:
                            self.enemy_tiles[i][col].status = TileStatus.BOAT
                            self.enemy_tiles[i][col].square.color = arcade.color.PURPLE
                    return True
        else:
            polovica = self.active_boat.length // 2
            if self.active_boat.angle == 270:
                if col < polovica or col > board_size - (polovica + 1):
                    return False
                for i in range(polovica + 1):
                    if not enemy_check:
                        if self.player_tiles[row][col - i].status != TileStatus.EMPTY:
                            return False
                    else:
                        if self.enemy_tiles[row][col - i].status != TileStatus.EMPTY:
                            return False
                for i in range(polovica + 1):
                    if not enemy_check:
                        if self.player_tiles[row][col + i].status != TileStatus.EMPTY:
                            return False
                    else:
                        if self.enemy_tiles[row][col + i].status != TileStatus.EMPTY:
                            return False
                for i in range(self.active_boat.length):
                    if not enemy_check:
                        self.player_tiles[row][col - polovica + i].status = TileStatus.BOAT
                    else:
                        self.enemy_tiles[row][col - polovica + i].status = TileStatus.BOAT
                        self.enemy_tiles[row][col - polovica + i].square.color = arcade.color.PURPLE
                return True
            else:
                if row < polovica or row > board_size - (polovica + 1):
                    return False
                for i in range(polovica + 1):
                    if not enemy_check:
                        if self.player_tiles[row - i][col].status != TileStatus.EMPTY:
                            return False
                    else:
                        if self.enemy_tiles[row - i][col].status != TileStatus.EMPTY:
                            return False
                for i in range(polovica + 1):
                    if not enemy_check:
                        if self.player_tiles[row + i][col].status != TileStatus.EMPTY:
                            return False
                    else:
                        if self.enemy_tiles[row + i][col].status != TileStatus.EMPTY:
                            return False
                for i in range(self.active_boat.length):
                    if not enemy_check:
                        self.player_tiles[row - polovica + i][col].status = TileStatus.BOAT
                    else:
                        self.enemy_tiles[row - polovica + i][col].status = TileStatus.BOAT
                        self.enemy_tiles[row - polovica + i][col].square.color = arcade.color.PURPLE
                return True
    
    def place_boat(self, boat_placement_tile, lower_index):
        self.active_boat.alpha = 255
        if isinstance(boat_placement_tile, Tile):
            if self.active_boat.angle == 270 or self.active_boat.angle == 90: 
                self.active_boat.y = boat_placement_tile.square.y + square_length / 2
                if self.active_boat.length % 2 == 0:
                    if not lower_index:
                        self.active_boat.x = boat_placement_tile.square.x + square_length
                    else:
                        self.active_boat.x = boat_placement_tile.square.x
                else:
                    self.active_boat.x = boat_placement_tile.square.x + square_length / 2
            else: 
                self.active_boat.x = boat_placement_tile.square.x + square_length / 2
                if self.active_boat.length % 2 == 0:
                    if not lower_index:
                        self.active_boat.y = boat_placement_tile.square.y
                    else:
                        self.active_boat.y = boat_placement_tile.square.y + square_length
                else:
                    self.active_boat.y = boat_placement_tile.square.y + square_length / 2
            self.active_boat = None
        
    def display_enemy_hits(self):
        for coord in self.fire_coords:
            arcade.draw_lrwh_rectangle_textured(coord[0], coord[1], square_length, square_length, texture=self.fire)
        for coord in self.miss_coords:
            arcade.draw_lrwh_rectangle_textured(coord[0], coord[1], square_length, square_length, texture=self.missed, angle=90)
            
    def main_menu(self, win=False):
        pass