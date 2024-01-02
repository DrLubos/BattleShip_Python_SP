from enums import Status
import arcade
class Policko:
    def __init__(self, row, col, size, win_width, win_height, nepriatel=False, rozmer=10):
        self.row = row
        self.col = col
        self.size = size
        self.win_width = win_width
        self.win_height = win_height
        self.nepriatel = nepriatel
        self.status = Status.PRAZDNE
        if nepriatel:
            self.stvorec = Stvorec(col * size - 20 + (win_width - size * rozmer), self.win_height - ((row + 1) * size) - 20, size, arcade.color.RED, True)
        else:
            self.stvorec = Stvorec(col * size + 20, self.win_height - ((row + 1) * size) - 20, size, arcade.color.BLACK)

    def get_row(self):
        return self.row
    def get_col(self):
        return self.col
    def get_status(self):
        return self.status
    
    def zasah(self):
        if self.nepriatel:
            self.status = Status.VYSTRELENE
            self.stvorec.color = (0, 0, 0, 0)
            if self.status == Status.LOD:
                self.status = Status.ZASIAHNUTE
                self.stvorec.color = arcade.color.SILVER    
            
    def zmen_farbu(self):
        if self.status == Status.PRAZDNE:
            if self.nepriatel:
                self.stvorec.color = arcade.color.GREEN
            else:    
                self.stvorec.priehladna = arcade.color.GOLD

    def reset_farbu(self):
        if self.status == Status.PRAZDNE:
            if self.nepriatel:
                self.stvorec.color = arcade.color.RED
            else:
                self.stvorec.priehladna = (0, 0, 0, 0)
                
class Stvorec:
    def __init__(self, x, y, size, color, nepriatel=False):
        self.x = x
        self.y = y
        self.size = size
        self.color = color
        self.nepriatel = nepriatel
        self.povodna_farba = color
        self.priehladna = (0, 0, 0, 0)
    
    def vykresli(self):
        if self.nepriatel:
            arcade.draw_xywh_rectangle_filled(self.x, self.y, self.size, self.size, self.color)
        else:
            arcade.draw_rectangle_filled(self.x + self.size / 2, self.y + self.size / 2, self.size, self.size, self.priehladna)
            arcade.draw_xywh_rectangle_outline(self.x, self.y, self.size, self.size, self.color, 2)