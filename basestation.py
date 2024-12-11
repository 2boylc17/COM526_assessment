from agent import Agent
import utils


class BaseStation(Agent):

    def __init__(self, position: tuple[int, int], dire):
        super().__init__(position)
        self.dire = dire
        self.front = []
        if self.dire == 'u':
            self.front = [self.position[0], self.position[1] - 1]
        elif self.dire == 'd':
            self.front = [self.position[0], self.position[1] + 1]
        elif self.dire == 'l':
            self.front = [self.position[0] - 1, self.position[1]]
        elif self.dire == 'd':
            self.front = [self.position[0] + 1, self.position[1]]
        #print(self.front, "front")

    def decide(self, percept):
        for k, v in percept.items():
            #print([k[0], k[1]], self.front, v, "test")
            if utils.is_robot(v) and [k[0], k[1]] == self.front:
                v.refill()
        return

    def act(self, environment):
        cell = self.sense(environment)
        decision = self.decide(cell)
        print(decision)

    def __str__(self):
        return self.dire

    def sense(self, environment):
        neighbours = []
        for direction in ["up", "right", "down", "left"]:
            if (direction == "up" and self.dire == "u") or (direction == "down" and self.dire == "d") or (direction == "left" and self.dire == "l") or (direction == "right" and self.dire == "d"):
                row_offset, col_offset = self.direction_offsets[direction]
                neighbours.append((self.position[0] + row_offset, self.position[1] + col_offset))

        return environment.get_cells(neighbours)
