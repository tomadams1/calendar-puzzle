from ortools.sat.python import cp_model
import numpy as np

grid_size = 3

blocks = {
    'square':{(0,0),(0,1),(1,0),(1,1)},
    'line':{(0,0),(0,1),(0,2)}
}

def transform(point: tuple[int,int], 
              rotation: int, 
              flipped: bool) -> tuple[int,int]:

    x,y = point[0],point[1]
    theta = rotation * np.pi / 2
    flip = -1 if flipped else 1

    new_x = np.rint(flip * (x * np.cos(theta) - y * np.sin(theta)))
    new_y = np.rint(x * np.sin(theta) + y * np.cos(theta))

    new_point = (new_x, new_y)
    return new_point

def transform_block(points: list[tuple[int,int]], 
                  rotation: int, 
                  flipped=False) -> list[tuple[int,int]]:

    new_points = [transform(p, rotation, flipped) for p in points]
    return new_points

def centre_block(points: list[tuple[int,int]]) -> list[tuple[int,int]]:

    min_x = min([p[0] for p in points])
    min_y = min([p[1] for p in points])

    new_points = [(p[0]-min_x, p[1]-min_y) for p in points]
    return new_points

def get_all(points: list[tuple[int,int]]) -> list[list[tuple[int,int]]]:

    all_transformations = set()

    for flipped in [True,False]:
        for rotation in range(4):
            new_points = transform_block(points, rotation, flipped)
            new_points = centre_block(new_points)
            all_transformations.add(frozenset(new_points))

    return all_transformations

all = (get_all(
    ((0,0),(0,1),(0,2))
    ))

for a in all:
    print(a)