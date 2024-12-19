from agent import Agent
from environment import Environment
import utils
import random
import heapq


class Robot(Agent):

    def __init__(self, position: tuple[int, int], dire):
        super().__init__(position)
        self.dire = dire
        self.front = []
        self.battery_level = 100
        self.base_station_location = None
        self.map = Environment("robotmap.txt")
        self.map.world[self.position[1]][self.position[0]] = self.dire
        self.front_change()
        print("starting position", self.position, self.front)

    def decide(self, percept: dict[tuple[int, int], ...]):
        cell = self.sense(percept)
        # print("cell", cell)
        for k, v in cell:
            self.map.world[v][k] = cell.get((k, v))
            if utils.is_base_station(cell.get((k, v))):
                self.base_station_location = (k, v)
        # self.calc_path(self.position, self.base_station_location, self.map)
        print("dis", self.calc_distance(self.position, self.base_station_location))
        self.random(percept)

    def act(self, environment):
        self.decide(environment)
        self.battery_level = self.battery_level - 1
        print("battery", self.battery_level)

    def front_change(self):
        if self.dire == '^':
            self.front = [self.position[0] - 1, self.position[1]]
        elif self.dire == 'v':
            self.front = [self.position[0] + 1, self.position[1]]
        elif self.dire == '<':
            self.front = [self.position[0], self.position[1] - 1]
        elif self.dire == '>':
            self.front = [self.position[0], self.position[1] + 1]

    def random(self, environment):
        directions = {
            "down": (0, 1),
            "up": (0, -1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        way = ""
        if self.dire == '^':
            way = "up"
        elif self.dire == 'v':
            way = "down"
        elif self.dire == '<':
            way = "left"
        elif self.dire == '>':
            way = "right"
        options = ["move", "left", "right"]
        num1 = random.randint(1, 3)
        choice = options[num1 - 1]
        print("choice", choice)
        if choice == "move":
            # print("move active")
            to = (self.position[0] + directions[way][0], self.position[1] + directions[way][1])
            self.move(environment, to)
        elif choice == "right":
            # print("right active", self.dire)
            if self.dire == '^':
                self.dire = '>'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
            elif self.dire == 'v':
                self.dire = '<'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
            elif self.dire == '<':
                self.dire = '^'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
            elif self.dire == '>':
                # print("before", self.dire)
                self.dire = 'v'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
                # print("after", self.dire)
            self.map.world[self.position[1]][self.position[0]] = self.dire
        elif choice == "left":
            # print("left active", self.dire)
            if self.dire == '^':
                self.dire = '<'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
            elif self.dire == 'v':
                self.dire = '>'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
            elif self.dire == '<':
                self.dire = 'v'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
            elif self.dire == '>':
                self.dire = '^'
                self.front_change()
                environment.world[self.position[1]][self.position[0]] = self.__str__()
            self.map.world[self.position[1]][self.position[0]] = self.dire
        else:
            print("active error")

    def move(self, environment, to):
        if environment.move_to(self.position, to) and self.viable_move(to[0], to[1], self.sense(environment)):
            print("moving", self.position, to)
            old = self.position
            self.position = (to[0], to[1])
            # print(self.position)
            environment.world[old[1]][old[0]] = ' '
            environment.world[self.position[1]][self.position[0]] = self.__str__()
            self.map.world[old[1]][old[0]] = ' '
            self.map.world[self.position[1]][self.position[0]] = self.dire
            self.front_change()
        elif self.viable_move(to[0], to[1], self.sense(environment)) is not True:
            print("blocked")

    def __str__(self):
        return self.dire

    # MANHATTAN DISTANCE FUNCTIONS
    def calc_path(self, start, goal, environment):
        p_queue = []
        heapq.heappush(p_queue, (0, start))

        directions = {
            "right": (0, 1),
            "left": (0, -1),
            "up": (-1, 0),
            "down": (1, 0)
        }
        predecessors = {start: None}
        g_values = {start: 0}

        while len(p_queue) != 0:
            # print("p queue print", p_queue)
            # print("g value print", g_values)
            current_cell = heapq.heappop(p_queue)[1]
            if current_cell == goal:
                return self.get_path(predecessors, start, goal)
            for direction in ["up", "right", "down", "left"]:
                row_offset, col_offset = directions[direction]
                # print("row_offset, col_offset", row_offset, col_offset)
                # print("Current cells", current_cell[0], current_cell[1])
                neighbour = (current_cell[0] + row_offset, current_cell[1] + col_offset)
                # print("neighbour print", neighbour)

                print("prob", neighbour[0], neighbour[1], self.sense(environment))
                if self.viable_move(neighbour[0], neighbour[1], self.sense(environment)) and neighbour not in g_values:
                    cost = g_values[current_cell] + 1
                    g_values[neighbour] = cost
                    f_value = cost + self.calc_distance(goal, neighbour)
                    heapq.heappush(p_queue, (f_value, neighbour))
                    predecessors[neighbour] = current_cell

    def get_path(self, predecessors, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = predecessors[current]
        path.append(start)
        path.reverse()
        return path

    def viable_move(self, x, y, adjacent):
        print("via", x, y, adjacent)
        cell = adjacent[(x, y)]
        if cell == 'x':
            return False
        elif utils.is_base_station(cell):
            return False
        elif utils.is_robot(cell):
            return False
        else:
            return True

    def calc_distance(self, point1: tuple[int, int], point2: tuple[int, int]):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    # END OF MANHATTAN DISTANCE FUNCTIONS

    def recharge(self):
        self.battery_level = self.battery_level + 5
        if self.battery_level > 100:
            self.battery_level = 100
        self.base_station_location = self.position
        print("recharged")
