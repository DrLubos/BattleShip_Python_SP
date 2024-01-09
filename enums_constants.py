from enum import Enum

square_length = 40
board_size = 10

class TileStatus(Enum):
    EMPTY = 0
    BOAT = 1
    HIT = 2
    MISS = 3