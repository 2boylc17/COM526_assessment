import random


class EmptySpot:

    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.dirty = random.randint(1, 100)

    def clean(self):
        self.dirty -= 10
        if self.dirty <= 0:
            self.dirty = 0

    def __str__(self):
        return ' '
