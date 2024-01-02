from enums import Status
from policko import Policko
import arcade

rozmer = 10
stvorec_size = 40

class Window(arcade.Window):
    def __init__(self, width, height, title, stvorec_size):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLUE)
        self.width = width
        self.height = height
        stvorec_size = stvorec_size
        self.stvorec_size = stvorec_size
        self.hracie_pole = [[Policko(row, col, stvorec_size, self.width, self.height) for col in range(rozmer)] for row in range(rozmer)]
        self.nepriatelske_pole = [[Policko(row, col, stvorec_size, self.width, self.height, nepriatel=True) for col in range(rozmer)] for row in range(rozmer)]
        self.aktivne_policko = None
        self.hrac_lode = []
        self.hra_sa = False
        self.nacitane_lode = False
        self.aktivna_lod = None

    def on_draw(self):
        arcade.start_render()
        self.vykresli_pole(self.hracie_pole)
        self.vykresli_pole(self.nepriatelske_pole)
        self.nacitaj_lode()
                
    def on_mouse_press(self, x, y, button, modifiers):
        if not self.hra_sa and not self.nacitane_lode:
            for lod in self.hrac_lode:
                if (
                    x >= lod.LHX
                    and x <= lod.LHX + self.stvorec_size
                    and y <= lod.LHY
                    and y >= lod.LHY - self.stvorec_size * lod.size
                ) and not self.aktivna_lod:
                    self.aktivna_lod = lod
                    self.aktivna_lod.alpha = 170
                    print("asdas")
        if self.hra_sa and self.aktivne_policko:
            self.aktivne_policko.zasah()
            self.aktivne_policko = None
            arcade.cleanup_texture_cache()
        
    def on_mouse_motion(self, x, y, dx, dy):
        if self.aktivna_lod:
            self.aktivna_lod.vykresli(x,y)
        
        nove_pole = None
        if x < self.stvorec_size * (len(self.hracie_pole) + 1) + 100:
            nove_pole = self.zisti_policko_pod_mysou(x, y, self.hracie_pole)
        elif x > self.width - (self.stvorec_size * (len(self.nepriatelske_pole) + 1)) - 100 and not self.aktivna_lod:
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
    
    def on_close(self):
        self.aktivne_policko = None
        arcade.cleanup_texture_cache()
        super().on_close()
        
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.R and self.aktivna_lod:
            self.aktivna_lod.otoc()
            
    def on_mouse_release(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_RIGHT and self.aktivna_lod:
            self.aktivna_lod.otoc()
        
    def priprav_lode(self):
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
            lod.vykresli(index * (stvorec_size * 1 + 20), None)
            index += 1   

    def nacitaj_lode(self):
        if len(self.hrac_lode) < 1:
            self.priprav_lode()
        for lod in self.hrac_lode:
            lod.vykresli(None, None)
        
    
    def zisti_policko_pod_mysou(self, x, y, pole):
        for row in pole:
            for policko in row:
                stvorec = policko.stvorec
                if (
                    x >= stvorec.x
                    and x < stvorec.x + stvorec.size
                    and y >= stvorec.y
                    and y < stvorec.y + stvorec.size
                ):
                    return policko
        return None        
    
    def vykresli_pole(self, pole):
        for row in pole:
            for policko in row:
                policko.stvorec.vykresli()
            
class Lod:
    def __init__(self, size, image_path):
        self.size = size
        self.image_path = image_path
        self.image = arcade.load_texture(image_path) if image_path else None
        self.stav = Status.LOD
        self.x = 20 + stvorec_size
        self.y = self.size * stvorec_size / 2 + 20
        self.active = False
        self.angle = 0
        self.LHX = 0
        self.LHY = 0
        self.alpha = 255

    def vykresli(self, x, y):
        if x or x == 0 : self.x = x
        if y or y == 0 : self.y = y
        if self.LHX == 0: self.LHX = self.x - (stvorec_size / 2)
        if self.LHY == 0: self.LHY = self.y + (self.size * stvorec_size / 2)
        if self.image:
            arcade.draw_texture_rectangle(self.x, self.y, stvorec_size, stvorec_size * self.size, self.image, angle=self.angle, alpha=self.alpha)
        else:
            print("Nepodarilo sa nacitat obrazok lode")
            
    def otoc(self):
        self.angle = 90 if self.angle == 0 else 0
        print(self.angle)