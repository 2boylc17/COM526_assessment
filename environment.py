import utils


class Environment:

    def __init__(self, map_path):
        self.file_path = map_path
        self.world = self.load_assets(self.load_map())

    def load_map(self):
        try:
            with open(self.file_path) as f:
                world_map = row = [[col.lower() for col in line.strip()] for line in f]

                # quick error check
                first_row = len(world_map[0])
                for row in world_map:
                    if len(row) != first_row:
                        raise Exception("Map rows are not even")
                return world_map
        except FileNotFoundError:
            print(f"File not found")
        except PermissionError:
            print(f"File read permissions were denied")
        except IOError as e:
            print(f"IO error: {e}")

        return []

    def load_assets(self, world_map:list):
        for i in range(len(world_map)):
            for j in range(len(world_map[i])):
                if world_map[i][j] == '^' or world_map[i][j] == 'v' or world_map[i][j] == '<' or world_map[i][j] == '>':
                    world_map[i][j] = utils.Robot((j, i))
                elif world_map[i][j] == 'u' or world_map[i][j] == 'd' or world_map[i][j] == 'l' or world_map[i][j] == 'r':
                    world_map[i][j] = utils.BaseStation((j, i), world_map[i][j])
        return world_map

    def get_cells(self, positions:list) -> dict[tuple[int,int],...]:
        cells = {}
        for pos in positions:
            cells[pos] = self.world[pos[1]][pos[0]]
        return cells

    def __str__(self):
        out = ""
        for row in self.world:
            for col in row:
                out += f"{col}\t"
            out += "\n"
        return out

    def move_to(self, start, goal):
        valid = False
        if (goal[0], goal[1]) == (start[0] + 1, goal[1]):
            valid = True
        elif (goal[0], goal[1]) == (start[0] - 1, goal[1]):
            valid = True
        elif (goal[0], goal[1]) == (goal[0], start[1] + 1):
            valid = True
        elif (goal[0], goal[1]) == (goal[0], start[1] - 1):
            valid = True
        print("goal", goal[0], goal[1])
        # print("start", start[0], start[1])
        # print("1",(start[0] + 1, goal[1]))
        # print("2",(start[0] - 1, goal[1]))
        # print("3",(goal[0], goal[1] + 1))
        # print("4",(goal[0], goal[1] - 1))
        # print("Valid", valid)
        if valid is True:
            print("success")
            return True
        else:
            return False



if __name__ == "__main__":
    e = Environment("map.txt")

    water = e.world[1][5]
    robot1 = e.world[2][5]

    for i in range(50):  # Change 1 simulate more moves. I.e. 100 would simulate 100 moves
        # Call the act method for each agent operating in the environment
        water.act(e)
        print(e)
        robot1.decide(e)
        #robot1.flame(e)
        # print("before", robot1.position)
        robot1.random(e)
        # print("after", robot1.position)
