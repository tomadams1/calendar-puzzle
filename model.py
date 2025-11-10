from ortools.sat.python import cp_model
from classes import Point, Block
from transformations import unique_block_transformations
from matplotlib import pyplot as plt

# grid_x = 3
# grid_y = 2

# blocks = {
#     'corner':{(0,0),(0,1),(1,0)},
#     'line':{(0,0),(0,1)},
#     'dot':{(0,0)}
# }

grid_x = 5
grid_y = 5

blocks = {
    'tee':{(0,0),(0,-1),(0,-2),(-1,0),(1,0)},
    'chunk':{(0,0),(1,0),(2,0),(1,1),(2,1)},
    'line':{(0,0),(0,1),(0,2)},
    'corner':{(0,0),(1,0),(2,0),(3,0),(3,1),(3,2)},
    'curly':{(0,0),(0,1),(0,2),(1,0),(2,0),(2,1)}
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

output = dict()

for block in blocks:

    all_matches = {key:value for key,value in all_blocks.items() if (key[0] == block)}

    for key,value in all_matches.items():

        if solver.boolean_value(value):

            # print(f'Place {block} at position ({key[2]},{key[3]})')
            # print(transformations[block][key[1]])
            
            final_points = []
            for p in transformations[block][key[1]].points:

                new_x = key[2] + p.x
                new_y = key[3] + p.y

                final_points.append(Point((new_x, new_y)))

            output[block] = Block(final_points)

print(output)

colors = {'tee':'red','chunk':'green','line':'blue','corner':'purple','curly':'cornflowerblue'}

fig, ax = plt.subplots()
fig.set_size_inches(12,8)
ax.set_xlim(0, grid_x)
ax.set_ylim(0, grid_y)

for block_name,block in output.items():

    for point in block.points:

        ax.fill_between([point.x, point.x+1], [point.y, point.y], [point.y+1, point.y+1], color=colors[block_name])

plt.savefig('foo.png')