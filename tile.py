from enums_constants import TileStatus

import arcade

class Tile:
    def __init__(self, row, col, side_length, win_width, win_height, enemy=False, board_size=10):
        self.row = row
        self.col = col
        self.side_length = side_length
        self.win_width = win_width
        self.win_height = win_height
        self.enemy = enemy
        self.status = TileStatus.EMPTY
        if self.enemy:
            self.square = Square(col * self.side_length - 20 + (win_width - self.side_length * board_size), self.win_height - ((row + 1) * self.side_length) - 20, self.side_length, arcade.color.RED, True)
        else:
            self.square = Square(col * self.side_length + 20, self.win_height - ((row + 1) * self.side_length) - 20, self.side_length, arcade.color.BLACK)
    
    def hitted(self):
        if self.status == TileStatus.BOAT:
                self.status = TileStatus.HIT
                self.square.color = arcade.color.SILVER    
        if self.status == TileStatus.EMPTY:
            self.status = TileStatus.MISS
            if self.enemy:
                self.square.color = (0, 0, 0, 0)
            
    def change_color(self):
        if self.status == TileStatus.EMPTY:
            if self.enemy:
                self.square.color = arcade.color.GREEN
            else:    
                self.square.transparent_color = arcade.color.GOLD

    def reset_color(self):
        if self.status == TileStatus.EMPTY:
            if self.enemy:
                self.square.color = arcade.color.RED
            else:
                self.square.transparent_color = (0, 0, 0, 0)
                
class Square:
    def __init__(self, x, y, side_length, color, enemy=False):
        self.x = x
        self.y = y
        self.side_length = side_length
        self.color = color
        self.enemy = enemy
        self.transparent_color = (0, 0, 0, 0)
    
    def draw(self):
        if self.enemy:
            arcade.draw_xywh_rectangle_filled(self.x, self.y, self.side_length, self.side_length, self.color)
        else:
            arcade.draw_rectangle_filled(self.x + self.side_length / 2, self.y + self.side_length / 2, self.side_length, self.side_length, self.transparent_color)
            arcade.draw_xywh_rectangle_outline(self.x, self.y, self.side_length, self.side_length, self.color, 2)