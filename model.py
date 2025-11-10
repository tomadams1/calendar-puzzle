from ortools.sat.python import cp_model
from classes import Point, Block
from transformations import unique_block_transformations

grid_x = 3
grid_y = 2

blocks = {
    'corner':{(0,0),(0,1),(1,0)},
    'line':{(0,0),(0,1)},
    'dot':{(0,0)}
}

blocks = {name:Block(Point(p) for p in points) for name,points in blocks.items()}
transformations = {name:unique_block_transformations(block) for name,block in blocks.items()}

model = cp_model.CpModel()

choices = {}

# Position and rotation for each block
for block_name, list_of_transforms in transformations.items():

    for x in range(grid_x):
        for y in range(grid_y):

            for t,_ in enumerate(list_of_transforms):

                choices[(block_name,x,y,t)] = model.new_bool_var(f'{block_name}_{x}_{y}_{t}')
