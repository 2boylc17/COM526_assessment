import random


class EmptySpot:

    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.dirty = random.randint(1, 100)

    def __str__(self):
        return ' '
