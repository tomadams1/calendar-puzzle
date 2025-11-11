from ortools.sat.python import cp_model
import numpy as np

from classes import Point, Cluster

grid_size = 3

blocks = {
    'square':{(0,0),(0,1),(1,0),(1,1)},
    'line':{(0,0),(0,1),(0,2)}
}

def transform_point(point: Point, 
              rotation: int, 
              flipped: bool) -> Point:
    """Takes a point, and rotates it 'rotation' quarters anti-clockwise around the origin.
    Also negates the x co-ordinate of the point if flipped is True.
    """

    theta = rotation * np.pi / 2
    flip = -1 if flipped else 1

    new_x = int(np.rint(flip * (point.x * np.cos(theta) - point.y * np.sin(theta))))
    new_y = int(np.rint(point.x * np.sin(theta) + point.y * np.cos(theta)))
    new_point = Point((new_x, new_y))

    return new_point

def transform_cluster(cluster: Cluster, 
                  rotation: int, 
                  flipped=False) -> Cluster:
    """Takes a block, and rotates it 'rotation' quarters anti-clockwise around the origin.
    Also flips the block horizontally if flipped is True.
    """

    new_cluster = Cluster({transform_point(point, rotation, flipped) for point in cluster.points})
    return new_cluster

def centre_cluster(cluster: Cluster) -> Cluster:

    min_x = min([point.x for point in cluster.points])
    min_y = min([point.y for point in cluster.points])

    new_cluster = Cluster([Point((point.x-min_x, point.y-min_y)) for point in cluster.points])
    return new_cluster

def unique_cluster_orientations(cluster: Cluster) -> list[Cluster]:

    unique_orientations = set()

    for flipped in [True,False]:
        for rotation in range(4):
            new_cluster = transform_cluster(cluster, rotation, flipped)
            new_cluster = centre_cluster(new_cluster)
            unique_orientations.add(new_cluster)

    unique_orientations = list(unique_orientations)

    return unique_orientations