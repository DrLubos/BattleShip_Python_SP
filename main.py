# main.py
import arcade
from game_handler import Handler

def main():
    game = Handler(1200, 800, "BattleShip Game")
    arcade.run()

if __name__ == "__main__":
    main()