from ortools.sat.python import cp_model
import numpy as np

from classes import Point

grid_size = 3

blocks = {
    'square':{(0,0),(0,1),(1,0),(1,1)},
    'line':{(0,0),(0,1),(0,2)}
}

def transform(point: Point, 
              rotation: int, 
              flipped: bool) -> Point:

    theta = rotation * np.pi / 2
    flip = -1 if flipped else 1

    new_x = np.rint(flip * (point.x * np.cos(theta) - point.y * np.sin(theta)))
    new_y = np.rint(point.x * np.sin(theta) + point.y * np.cos(theta))

    new_point = Point((new_x, new_y))
    return new_point

def transform_block(points: list[Point], 
                  rotation: int, 
                  flipped=False) -> list[Point]:

    new_points = [transform(p, rotation, flipped) for p in points]
    return new_points

def centre_block(points: list[Point]) -> list[Point]:

    min_x = min([p.x for p in points])
    min_y = min([p.y for p in points])

    new_points = [(p.x-min_x, p.y-min_y) for p in points]
    return new_points

def get_all(points: list[Point]) -> list[list[Point]]:

    all_transformations = set()

    for flipped in [True,False]:
        for rotation in range(4):
            new_points = transform_block(points, rotation, flipped)
            new_points = centre_block(new_points)
            all_transformations.add(frozenset(new_points))

    all_transformations = [list(t) for t in all_transformations]

    return all_transformations

points = [(0,0),(1,0),(0,1)]
points = [Point(p) for p in points]
for x in get_all(points):
    print(x)