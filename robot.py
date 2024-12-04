from agent import Agent
import utils
import random
import heapq


class Robot(Agent):

    def __init__(self, position: tuple[int, int], dire):
        super().__init__(position)
        self.dire = dire
        self.front = []
        if self.dire == '^':
            self.front = [self.position[0] - 1, self.position[1]]
        elif self.dire == 'v':
            self.front = [self.position[0] + 1, self.position[1]]
        elif self.dire == '<':
            self.front = [self.position[0], self.position[1] - 1]
        elif self.dire == '>':
            self.front = [self.position[0], self.position[1] + 1]
        self.battery_level = 20
        self.base_station_location = None

    def decide(self, percept: dict[tuple[int, int], ...]):
        adjacent = self.sense(percept)
        print("d", adjacent)
        for cell in adjacent:
            print("cell value decide", cell, adjacent[cell], utils.is_flame(adjacent[cell]))
            if utils.is_flame(adjacent[cell]):
                print("checking", percept[cell])

    def act(self, environment):
        self.random(environment)
        pass

    def flame(self, environment):
        adjacent = self.sense(environment)
        for cell in adjacent:
            print("cell value", cell, environment.world[cell[1]][cell[0]])
            if environment.world[cell[1]][cell[0]] == '🔥':
                print("Flame sensed")
                environment.world[cell[1]][cell[0]] = ''

    def random(self, environment):
        directions = {
            "right": (0, 1),
            "left": (0, -1),
            "up": (-1, 0),
            "down": (1, 0)
        }
        names = ["up", "right", "down", "left"]
        num = random.randint(1, 4)
        way = names[num - 1]
        for direction in names:
            #print("check", directions[way], directions[direction])
            if directions[way] == directions[direction]:
                #print("happening", self.position, directions[way])
                to = (self.position[0] + directions[way][0], self.position[1] + directions[way][1])
                #print("happen", to)
                self.move(environment, to)
                break

    def move(self, environment, to):
        if environment.move_to(self.position, to) and self.viable_move(to[0], to[1], self.sense(environment)):
            print(self.position, to)
            old = self.position
            self.position = (to[0], to[1])
            print(self.position)
            environment.world[old[1]][old[0]] = ''
            environment.world[self.position[1]][self.position[0]] = self.__str__()
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
            print("p queue print", p_queue)
            print("g value print", g_values)
            current_cell = heapq.heappop(p_queue)[1]
            if current_cell == goal:
                return self.get_path(predecessors, start, goal)
            for direction in ["up", "right", "down", "left"]:
                row_offset, col_offset = directions[direction]
                print("row_offset, col_offset", row_offset, col_offset)
                print("Current cells", current_cell[0], current_cell[1])
                neighbour = (current_cell[0] + row_offset, current_cell[1] + col_offset)
                print("neighbour print", neighbour)

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
        cell = adjacent[x, y]
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

    def refill(self):
        self.battery_level = self.battery_level + 1
