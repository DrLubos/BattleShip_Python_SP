# main.py
import arcade
from game_handler import Window

def main():
    game = Window(1200, 800, "BattleShip Game")
    arcade.run()

if __name__ == "__main__":
    main()