from agent import Agent
from environment import Environment
import utils
import random
import heapq
import fuzzy


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
        self.spot = utils.EmptySpot((self.position[0], self.position[1]))
        self.spot.dirty = 0
        self.mode = "Idle"
        self.fan_speed = fuzzy.calc_fan_speed(0, 0)
        print("starting position", self.position, self.front)

    def decide(self, percept: dict[tuple[int, int], ...]):
        cell = self.sense(percept, self.position)
        for k, v in cell:
            self.map.world[v][k] = cell.get((k, v))
        self.move_choice(percept)
        print("Decide")

    def act(self, environment):
        self.decide(environment)
        if self.mode == "Cleaning":
            self.fan_speed = fuzzy.calc_fan_speed(self.spot.dirty, self.battery_level)
            if self.fan_speed > 100:
                self.fan_speed = 100
            if self.fan_speed < 0:
                self.fan_speed = 0
            self.spot.clean(fuzzy.calc_cleaning(self.fan_speed))
            self.battery_level -= fuzzy.calc_battery(self.fan_speed)
        elif self.mode == "Moving":
            self.fan_speed = fuzzy.calc_fan_speed(0, 0)
            if self.fan_speed > 100:
                self.fan_speed = 100
            if self.fan_speed < 0:
                self.fan_speed = 0
            self.battery_level -= fuzzy.calc_battery(self.fan_speed)
        print("Spot Dirtiness:", self.spot.dirty, (self.position[1], self.position[0]))
        print("battery", self.battery_level)
        print("Act")

    def front_change(self):
        if self.dire == '^':
            self.front = [self.position[0], self.position[1] - 1]
        elif self.dire == 'v':
            self.front = [self.position[0], self.position[1] + 1]
        elif self.dire == '<':
            self.front = [self.position[0] - 1, self.position[1]]
        elif self.dire == '>':
            self.front = [self.position[0] + 1, self.position[1]]

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
            self.turn_right(environment)
        elif choice == "left":
            self.turn_left(environment)
        else:
            print("active error")

    def move_choice(self, environment):
        if self.base_station_location is None:
            base_distance = ["error"]
        else:
            base_distance = self.calc_path(self.position, self.base_station_location)
        # print("bd", base_distance)
        if ((len(base_distance) * 2) + 3 >= self.battery_level and self.position != self.base_station_location
                and base_distance[0] != "error"):
            # print("commence")
            self.mode = "Moving"
            self.move_attempt(environment, base_distance[1])
        elif self.position == self.base_station_location and self.battery_level < 95:
            self.mode = "Charging"
            print("staying to charge")
        elif self.dirt_check(environment):
            self.mode = "Cleaning"
            self.move_attempt(environment, self.dirt_rating(environment))
        else:
            self.mode = "Moving"
            self.random(environment)

    def dirt_check(self, environment):
        cell = self.sense(environment, self.position)
        for k, v in cell:
            if utils.is_empty_spot(cell.get((k, v))):
                if cell.get((k, v)).dirty != 0:
                    return True
        return False

    def dirt_rating(self, environment):
        cell = self.sense(environment, self.position)
        dirty_spot = ""
        for k, v in cell:
            if utils.is_empty_spot(cell.get((k, v))):
                new_spot = cell.get((k, v))
                if dirty_spot == "":
                    if new_spot.dirty != 0:
                        dirty_spot = new_spot.position
                elif new_spot.dirty > cell.get(dirty_spot).dirty:
                    dirty_spot = new_spot.position
        return dirty_spot

    def move_attempt(self, environment, coordinates):
        directions = {
            "right": (1, 0),
            "left": (-1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }
        move = (coordinates[0] - self.position[0], coordinates[1] - self.position[1])
        for direction in directions:
            if directions[direction] == move:
                way = ""
                if self.dire == '^':
                    way = "up"
                elif self.dire == 'v':
                    way = "down"
                elif self.dire == '<':
                    way = "left"
                elif self.dire == '>':
                    way = "right"
                # print("need", way, move)
                if directions[way] == move:
                    # print("correct way")
                    self.move(environment, coordinates)
                elif (way == "up" and move == (1, 0) or way == "right" and move == (0, 1)
                      or way == "down" and move == (-1, 0) or way == "left" and move == (0, -1)):
                    # print("right turn needed")
                    self.turn_right(environment)
                elif (way == "up" and move == (-1, 0) or way == "left" and move == (0, 1)
                      or way == "down" and move == (1, 0) or way == "right" and move == (0, -1)):
                    # print("left turn needed")
                    self.turn_left(environment)
                elif (way == "up" and move == (0, 1) or way == "right" and move == (-1, 0)
                      or way == "down" and move == (0, -1) or way == "left" and move == (1, 0)):
                    # print("spin needed")
                    self.turn_right(environment)

    def turn_right(self, environment):
        if self.dire == '^':
            self.dire = '>'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
        elif self.dire == 'v':
            self.dire = '<'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
        elif self.dire == '<':
            self.dire = '^'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
        elif self.dire == '>':
            # print("before", self.dire)
            self.dire = 'v'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
            # print("after", self.dire)
        self.map.world[self.position[1]][self.position[0]] = self.dire

    def turn_left(self, environment):
        if self.dire == '^':
            self.dire = '<'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
        elif self.dire == 'v':
            self.dire = '>'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
        elif self.dire == '<':
            self.dire = 'v'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
        elif self.dire == '>':
            self.dire = '^'
            self.front_change()
            environment.world[self.position[1]][self.position[0]] = self
        self.map.world[self.position[1]][self.position[0]] = self.dire

    def move(self, environment, to):
        if (environment.move_to(self.position, to) and
                self.viable_move(to[0], to[1], self.sense(environment, self.position))):
            print("moving", self.position, to)
            old = self.position
            self.position = (to[0], to[1])
            environment.world[old[1]][old[0]] = self.spot
            self.map.world[old[1]][old[0]] = self.spot
            self.spot = environment.world[self.position[1]][self.position[0]]
            environment.world[self.position[1]][self.position[0]] = self
            self.map.world[self.position[1]][self.position[0]] = self
            self.front_change()
        elif self.viable_move(to[0], to[1], self.sense(environment, self.position)) is not True:
            print("blocked")

    def __str__(self):
        return self.dire

    def calc_path(self, start, goal):
        p_queue = []
        heapq.heappush(p_queue, (0, start))
        directions = {
            "right": (1, 0),
            "left": (-1, 0),
            "up": (0, -1),
            "down": (0, 1)
        }
        predecessors = {start: None}
        g_values = {start: 0}
        while len(p_queue) != 0:
            current_cell = heapq.heappop(p_queue)[1]
            if current_cell == goal:
                return self.get_path(predecessors, start, goal)
            for direction in ["up", "right", "down", "left"]:
                row_offset, col_offset = directions[direction]
                neighbour = (current_cell[0] + row_offset, current_cell[1] + col_offset)
                if (self.viable_move(neighbour[0], neighbour[1], self.sense(self.map, current_cell))
                        and neighbour not in g_values):
                    cost = g_values[current_cell] + 1
                    g_values[neighbour] = cost
                    f_value = cost + self.calc_distance(goal, neighbour)
                    heapq.heappush(p_queue, (f_value, neighbour))
                    predecessors[neighbour] = current_cell

    @staticmethod
    def get_path(predecessors, start, goal):
        current = goal
        path = []
        while current != start:
            path.append(current)
            current = predecessors[current]
        path.append(start)
        path.reverse()
        return path

    @staticmethod
    def viable_move(x, y, adjacent):
        # print("via", x, y, adjacent)
        cell = adjacent[(x, y)]
        if cell == 'x' or cell == '?':
            return False
        elif utils.is_base_station(cell):
            return False
        elif utils.is_robot(cell):
            return False
        else:
            # print("viable move", cell)
            return True

    @staticmethod
    def calc_distance(point1: tuple[int, int], point2: tuple[int, int]):
        x1, y1 = point1
        x2, y2 = point2
        return abs(x1 - x2) + abs(y1 - y2)

    def recharge(self):
        self.battery_level = self.battery_level + 5
        if self.battery_level > 100:
            self.battery_level = 100
        self.base_station_location = self.position
        print("recharged")
