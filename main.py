# main.py
import arcade
from gui_main import Window

def main():
    game = Window(1200, 800, "Battleship Game", 40)
    arcade.run()

if __name__ == "__main__":
    main()