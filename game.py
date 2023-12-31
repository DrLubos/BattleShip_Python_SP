from enums import Status
import arcade

class Window(arcade.Window):
    def __init__(self, width, height, title, stvorec_size):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLUE)
        self.width = width
        self.height = height
        self.stvorec_size = stvorec_size
        self.hracie_pole = [[Policko(row, col, stvorec_size, self.width, self.height) for col in range(10)] for row in range(10)]
        self.nepriatelske_pole = [[Policko(row, col, stvorec_size, self.width, self.height, nepriatel=True) for col in range(10)] for row in range(10)]
        self.aktivne_policko = None

    def on_draw(self):
        arcade.start_render()
        self.vykresli_pole(self.hracie_pole)
        self.vykresli_pole(self.nepriatelske_pole)

    def vykresli_pole(self, pole):
        for row in pole:
            for policko in row:
                policko.stvorec.vykresli()
        
    def on_mouse_motion(self, x, y, dx, dy):
        nove_pole = None
        if x < self.stvorec_size * (len(self.hracie_pole) + 1) + 100:
            nove_pole = self.zisti_policko_pod_mysou(x, y, self.hracie_pole)
        elif x > self.width - (self.stvorec_size * (len(self.nepriatelske_pole) + 1)) - 100:
            nove_pole = self.zisti_policko_pod_mysou(x, y, self.nepriatelske_pole)
            
        if nove_pole:
            if self.aktivne_policko and self.aktivne_policko != nove_pole:
                self.aktivne_policko.reset_farbu()
            nove_pole.zmen_farbu()
            self.aktivne_policko = nove_pole
        else:
            if self.aktivne_policko:
                self.aktivne_policko.reset_farbu()
            self.aktivne_policko = None
            
    def on_mouse_press(self, x, y, button, modifiers):
        if self.aktivne_policko:
            self.aktivne_policko.zasah()
            arcade.cleanup_texture_cache()
            self.cleanup_sprites()
            self.aktivne_policko = None
    
    def zisti_policko_pod_mysou(self, x, y, pole):
        for row in pole:
            for policko in row:
                stvorec = policko.stvorec
                if (
                    x > stvorec.x
                    and x < stvorec.x + stvorec.size
                    and y > stvorec.y
                    and y < stvorec.y + stvorec.size
                ):
                    return policko
        return None
    
    def on_close(self):
        arcade.cleanup_texture_cache()
        self.aktivne_policko = None
        self.cleanup_sprites()
        super().on_close()
        
    def cleanup_sprites(self):
        # Prejdeme cez všetky sprajty v hracích poliach
        for row in self.hracie_pole:
            for policko in row:
                policko.stvorec.remove_from_sprite_lists()

        for row in self.nepriatelske_pole:
            for policko in row:
                policko.stvorec.remove_from_sprite_lists()

class Policko:
    def __init__(self, row, col, size, win_width, win_height, nepriatel=False, lod=False):
        self.row = row
        self.col = col
        self.size = size
        self.win_width = win_width
        self.win_height = win_height
        self.nepriatel = nepriatel
        self.lod = lod
        self.status = Status.PRAZDNE
        if nepriatel:
            self.stvorec = Stvorec(col * size - 20 + (win_width - size * 10), self.win_height - ((row + 1) * size) - 20, size, arcade.color.RED, True)
        else:
            self.stvorec = Stvorec(col * size + 20, self.win_height - ((row + 1) * size) - 20, size, arcade.color.BLACK)

    def zasah(self):
        if self.nepriatel:
            self.status = Status.VYSTRELENE
            self.stvorec.color = (0, 0, 0, 0)
            if self.lod:
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