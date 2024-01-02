from enums import Status
import arcade

rozmer = 10
stvorec_size = 40
hra_sa = False
nacitane_lode = False

class Window(arcade.Window):
    def __init__(self, width, height, title, stvorec_size):
        super().__init__(width, height, title)
        #arcade.set_background_color(arcade.color.BLUE)
        self.width = width
        self.height = height
        stvorec_size = stvorec_size
        self.stvorec_size = stvorec_size
        self.hracie_pole = [[Policko(row, col, stvorec_size, self.width, self.height) for col in range(rozmer)] for row in range(rozmer)]
        self.nepriatelske_pole = [[Policko(row, col, stvorec_size, self.width, self.height, nepriatel=True) for col in range(rozmer)] for row in range(rozmer)]
        self.sprite_list = arcade.SpriteList()
        self.aktivne_policko = None

    def on_draw(self):
        arcade.start_render()
        #self.vykresli_pole(self.hracie_pole)
        #self.vykresli_pole(self.nepriatelske_pole)
        if not nacitane_lode: self.nacitaj_lode()
        

    def vykresli_pole(self, pole):
        for row in pole:
            for policko in row:
                policko.stvorec.vykresli()
                
    def on_mouse_press(self, x, y, button, modifiers):
        if self.aktivne_policko:
            lod = self.aktivne_policko.lod
            if lod:
                if (
                    x > lod.x
                    and x < lod.x + lod.size
                    and y > lod.y
                    and y < lod.y + lod.size
                ):
                    lod.active = True  # Nastavíme loď ako aktívnu

        
    def on_mouse_motion(self, x, y, dx, dy):
        if not hra_sa:
            pass
        
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
            self.aktivne_policko = None
            arcade.cleanup_texture_cache()
    
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
        self.aktivne_policko = None
        arcade.cleanup_texture_cache()
        super().on_close()
        
    def nacitaj_lode(self):
        self.hrac_lode = [
            Lod(5, "./assets/ship1.png"),
            Lod(4, "./assets/ship2.png"),
            Lod(4, "./assets/ship3.png"),
            Lod(3, "./assets/ship4.png"),
            Lod(3, "./assets/ship5.png"),
            Lod(2, "./assets/ship6.png"),
            Lod(2, "./assets/ship7.png"),
        ]
        index = 1
        for lod in self.hrac_lode:
            lod.vykresli(index * (stvorec_size * 1 + 20), None, stvorec_size)
            index += 1
        nacitane_lode = True

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
            self.stvorec = Stvorec(col * size - 20 + (win_width - size * rozmer), self.win_height - ((row + 1) * size) - 20, size, arcade.color.RED, True)
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
            
class Lod:
    def __init__(self, size, image_path):
        self.size = size
        self.image_path = image_path
        self.image = arcade.load_texture(image_path) if image_path else None
        self.stav = Status.LOD
        self.x = 20 + stvorec_size # defaultne hodnoty
        self.y = self.size * stvorec_size / 2 + 20
        self.active = False
        self.angle = 0
        self.LHX = 0
        self.LHY = 0

    def vykresli(self, x, y, stvorec_size):
        if x or x == 0 : self.x = x
        if y or y == 0 : self.y = y
        self.LHX = self.x - (stvorec_size / 2)
        self.LHY = self.y + (self.size * stvorec_size / 2)
        if self.image:
            print(self.x, self.y)
            arcade.draw_texture_rectangle(self.x, self.y, stvorec_size, stvorec_size * self.size, self.image, self.angle)
        else:
            print("Nepodarilo sa nacitat obrazok lode")
            
    def otoc(self):
        self.rotation = 90 if self.rotation == 0 else 0