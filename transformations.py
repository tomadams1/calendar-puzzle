from ortools.sat.python import cp_model
import numpy as np

from classes import Point, Block

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

def transform_block(block: Block, 
                  rotation: int, 
                  flipped=False) -> Block:
    """Takes a block, and rotates it 'rotation' quarters anti-clockwise around the origin.
    Also flips the block across x=0 if flipped is True.
    """

    new_points = Block([transform_point(point, rotation, flipped) for point in block.points])
    return new_points

def unique_blocks(list_of_blocks: list[Block]) -> list[Block]:

    unique_blocks = {frozenset([(p.x,p.y) for p in block.points]) for block in list_of_blocks}
    # for u in unique_points:
    #     print(u)
    unique_blocks = [Block([Point((q[0], q[1])) for q in p]) for p in unique_blocks]
    return unique_blocks

def unique_block_transformations(block: Block) -> list[Block]:

    all_transformations = list()

    for flipped in [True,False]:
        for rotation in range(4):
            new_block = transform_block(block, rotation, flipped)
            all_transformations.append(new_block)

    unique_transformations = unique_blocks(all_transformations)

    return unique_transformations

co_ords = [(0,0),(1,0),(0,1)]
block = Block([Point(p) for p in co_ords])
all_blocks = unique_block_transformations(block)

for a in all_blocks:
    print(a)
