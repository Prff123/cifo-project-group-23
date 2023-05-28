import random


def create_map(nr_ghosts=20, nr_fruits=14, width=12, height=12):
    map = [["*" for i in range(width)] for i in range(height)]

    map[0][0] = "p"

    while nr_ghosts > 0:
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        if map[y][x] != "g" and (x != 0 or y != 0):
            # Check if any neighboring cells are g
            neighbors = [(x+i, y+j) for i in range(-1,2) for j in range(-1,2) if (i != 0 or j != 0) and x+i >= 0 and x+i < width and y+j >= 0 and y+j < height]
            if not any(map[j][i] == "g" for (i,j) in neighbors):
                map[y][x] = "g"
                nr_ghosts -= 1

    while nr_fruits > 0:
        x = random.randint(0, width-1)
        y = random.randint(0, height-1)
        if map[y][x] != "g" and (x != 0 or y != 0):
            map[y][x] = "f"
            nr_fruits -= 1

    return map
