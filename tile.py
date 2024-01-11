from enums_constants import TileStatus, board_size, padding, square_length

import arcade

class Tile:
    def __init__(self, row, col, win_width, win_height, handler, enemy=False):
        self.row = row
        self.col = col
        self.win_width = win_width
        self.win_height = win_height
        self.handler = handler
        self.enemy = enemy
        self.status = TileStatus.EMPTY
        if self.enemy:
            self.square = Square(col * square_length - padding + (win_width - square_length * board_size), self.win_height - ((row + 1) * square_length) - padding, arcade.color.RED, self.handler, True)
        else:
            self.square = Square(col * square_length + padding, self.win_height - ((row + 1) * square_length) - padding, arcade.color.BLACK, self.handler)
    
    def hitted(self):
        if self.status == TileStatus.BOAT:
                self.status = TileStatus.HIT
                self.square.texture = self.handler.fire
                if not self.enemy:
                    self.handler.fire_coords.append((self.square.x, self.square.y))
                    self.handler.hitpoints -= 1
        if self.status == TileStatus.EMPTY:
            self.status = TileStatus.MISS
            if self.enemy:
                self.square.alpha = 0
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
    def __init__(self, x, y, color, handler, enemy=False):
        self.x = x
        self.y = y
        self.color = color
        self.handler = handler
        self.enemy = enemy
        self.texture = self.handler.cloud
        self.alpha = 255
        self.transparent_color = (0, 0, 0, 0)
    
    def draw(self):
        if self.enemy:
            arcade.draw_lrwh_rectangle_textured(self.x, self.y, square_length, square_length, texture=self.texture, alpha=self.alpha)
        else:
            arcade.draw_rectangle_filled(self.x + square_length / 2, self.y + square_length / 2, square_length, square_length, self.transparent_color)
            arcade.draw_xywh_rectangle_outline(self.x, self.y, square_length, square_length, self.color, 2)