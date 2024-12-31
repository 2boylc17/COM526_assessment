from abc import ABC, abstractmethod


class Agent(ABC):

    def __init__(self, position: tuple[int, int]):
        self.position = position
        self.direction_offsets = {
            "up": (0, -1),
            "right": (1, 0),
            "down": (0, 1),
            "left": (-1, 0)
        }

    def sense(self, environment, position):
        neighbours = []
        for direction in ["up", "right", "down", "left"]:
            row_offset, col_offset = self.direction_offsets[direction]
            neighbours.append((position[0] + row_offset, position[1] + col_offset))
        # print("Perceive", position)
        return environment.get_cells(neighbours)

    @abstractmethod
    def decide(self, percept: dict[tuple[int, int], ...]):
        pass

    @abstractmethod
    def act(self, environment):
        pass
