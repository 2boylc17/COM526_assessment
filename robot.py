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
        self.move_choice(percept)

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
            self.turn_right(environment)
        elif choice == "left":
            self.turn_left(environment)
        else:
            print("active error")

    def move_choice(self, environment):
        base_distance = self.calc_path(self.position, self.base_station_location, environment)
        print("bd", base_distance)
        if len(base_distance) >= self.battery_level and self.position != self.base_station_location:
            if base_distance[1] == "right":
                self.turn_right(environment)
            elif base_distance[1] == "left":
                self.turn_left(environment)
            else:
                self.move(environment, base_distance[1])
        elif self.position == self.base_station_location and self.battery_level < 100:
            print("staying to charge")
        else:
            self.random(environment)

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
        if environment.move_to(self.position, to) and self.viable_move(to[0], to[1], self.sense(environment)):
            print("moving", self.position, to)
            old = self.position
            self.position = (to[0], to[1])
            # print(self.position)
            environment.world[old[1]][old[0]] = ' '
            environment.world[self.position[1]][self.position[0]] = self
            self.map.world[old[1]][old[0]] = ' '
            self.map.world[self.position[1]][self.position[0]] = self.dire
            self.front_change()
        elif self.viable_move(to[0], to[1], self.sense(environment)) is not True:
            print("blocked")

    def __str__(self):
        return self.dire

    def calc_path(self, start, goal, environment):
        p_queue = []
        heapq.heappush(p_queue, (0, start))
        face = ""
        face_num = 0
        directions = {
            "right": (0, 1),
            "left": (0, -1),
            "up": (-1, 0),
            "down": (1, 0)
        }
        if self.dire == ">":
            face = "right"
        elif self.dire == "<":
            face = "left"
        elif self.dire == "^":
            face = "up"
        elif self.dire == "v":
            face = "down"
        predecessors = {start: None}
        g_values = {start: 0}
        while len(p_queue) != 0:
            current_cell = heapq.heappop(p_queue)[1]
            if current_cell == goal:
                return self.get_path(predecessors, start, goal)
            for direction in ["up", "right", "down", "left"]:
                row_offset, col_offset = directions[direction]
                neighbour = (current_cell[0] + row_offset, current_cell[1] + col_offset)
                # print("neighbour", neighbour)
                if neighbour not in g_values:
                    cost = g_values[current_cell] + 1
                    g_values[neighbour] = cost
                    f_value = cost + self.calc_distance(goal, neighbour)
                    # print("direction", direction)
                    # print("before", predecessors)
                    # print("pqueue before", p_queue)
                    if direction == face:
                        heapq.heappush(p_queue, (f_value, neighbour))
                        predecessors[neighbour] = current_cell
                    else:
                        heapq.heappush(p_queue, (f_value, neighbour))
                        point = direction
                        if (direction == "up" and face == "left" or direction == "right" and face == "up" or
                                direction == "down" and face == "right" or direction == "left" and face == "down"):
                            point = ("right", face_num)
                            predecessors[neighbour] = current_cell
                            predecessors[predecessors[neighbour]] = point
                            face_num += 1
                        elif (direction == "up" and face == "right" or direction == "right" and face == "down" or
                                direction == "down" and face == "left" or direction == "left" and face == "up"):
                            point = ("left", face_num)
                            predecessors[neighbour] = current_cell
                            predecessors[predecessors[neighbour]] = point
                            face_num += 1
                        elif (direction == "up" and face == "right" or direction == "right" and face == "down" or
                                direction == "down" and face == "left" or direction == "left" and face == "up"):
                            predecessors[neighbour] = current_cell
                            face_num += 1
                            point = ("right", face_num)
                            predecessors[predecessors[neighbour]] = point
                            predecessors[predecessors[predecessors[neighbour]]] = point
                            face_num += 1
                    print("after", predecessors)

    def get_path(self, predecessors, start, goal):
        current = goal
        path = []
        while current != start:
            print("path start", path)
            print("prob", current, start, predecessors)
            path.append(current)
            current = predecessors[current]
            print("po", path, current)
        path.append(start)
        path.reverse()
        print("path", path)
        return path

    def viable_move(self, x, y, adjacent):
        # print("via", x, y, adjacent)
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

    def recharge(self):
        self.battery_level = self.battery_level + 5
        if self.battery_level > 100:
            self.battery_level = 100
        self.base_station_location = self.position
        print("recharged")
