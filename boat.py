from enums_constants import square_length

import arcade

class Boat:
    def __init__(self, length, image_path):
        self.length = length
        self.image_path = image_path
        self.image = arcade.load_texture(image_path) if image_path else None
        self.x = 20 + square_length
        self.y = self.length * square_length / 2 + 20
        self.angle = 0
        self.left_up_x = 0
        self.left_up_y = 0
        self.alpha = 255

    def draw(self, x, y):
        if x or x == 0 : self.x = x
        if y or y == 0 : self.y = y
        if self.left_up_x == 0: self.left_up_x = self.x - (square_length / 2)
        if self.left_up_y == 0: self.left_up_y = self.y + (self.length * square_length / 2)
        if self.image:
            arcade.draw_texture_rectangle(self.x, self.y, square_length, square_length * self.length, self.image, angle=self.angle, alpha=self.alpha)
        else:
            print("Nepodarilo sa nacitat obrazok lode")

    def rotate(self):
        self.angle = 270 if self.angle == 0 else 0