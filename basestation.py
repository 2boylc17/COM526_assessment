from agent import Agent
import utils


class BaseStation(Agent):

    def __init__(self, position: tuple[int, int], dire):
        super().__init__(position)
        self.dire = dire
        self.front = []
        if self.dire == 'u':
            self.front = [self.position[0] - 1, self.position[1]]
        elif self.dire == 'd':
            self.front = [self.position[0] + 1, self.position[1]]
        elif self.dire == 'l':
            self.front = [self.position[0], self.position[1] - 1]
        elif self.dire == 'd':
            self.front = [self.position[0], self.position[1] + 1]

    def decide(self, percept):
        for k, v in percept.items():
            if utils.is_robot(v):
                v.refill()
        return

    def act(self, environment):
        cell = self.sense(environment)
        decision = self.decide(cell)
        print(decision)

    def __str__(self):
        return self.dire
