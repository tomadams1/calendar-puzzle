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

all_blocks = {}

# all_blocks is a dictionary of whether we have a block in a certain position / transformation
for b, list_of_transforms in transformations.items():
    for t,_ in enumerate(list_of_transforms):
        for x in range(grid_x):
            for y in range(grid_y):

                all_blocks[(b,t,x,y)] = model.new_bool_var(f'{b}_{t}_{x}_{y}')

# all_squares is an int showing the number of blocks that are on that square
all_squares = {}
for x in range(grid_x):
    for y in range(grid_y):
        all_squares[(x,y)] = model.new_int_var(0, len(transformations), f'{x}_{y}')
        model.add(all_squares[(x,y)] == 1)

# Each block can only have one position and transformation
for block_name in transformations:

    block_choices = [value for key,value in all_blocks.items() if key[0] == block_name]
    print(block_choices)
    model.add_exactly_one(block_choices)

# Each square has the value of the number of blocks that are lying on it
for sq_x in range(grid_x):
    for sq_y in range(grid_y):

        pointing_at_square = list()

        for b, list_of_transforms in transformations.items():
            for t, block_trans in enumerate(list_of_transforms):
                for x in range(grid_x):
                    for y in range(grid_y):
                        for p in block_trans.points:

                            fx = x + p.x
                            fy = y + p.y

                            if (fx==sq_x) & (fy==sq_y):

                                pointing_at_square.append(all_blocks[(b,t,x,y)])

        model.add(all_squares[sq_x,sq_y] == sum(pointing_at_square))

solver = cp_model.CpSolver()
solution_printer = cp_model.ObjectiveSolutionPrinter()
status = solver.solve(model, solution_printer)

for block in blocks:

    all_matches = {key:value for key,value in all_blocks.items() if (key[0] == block)}

    for key,value in all_matches.items():

        if solver.boolean_value(value):

            print(f'Place {key[0]} at position ({key[2]},{key[3]})')
            print(transformations[block][key[1]])
