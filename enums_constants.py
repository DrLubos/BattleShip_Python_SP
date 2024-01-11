from enum import Enum

square_length = 50
board_size = 10
padding = 20
win_width = 1200
win_height = 800

class TileStatus(Enum):
    EMPTY = 0
    BOAT = 1
    HIT = 2
    MISS = 3