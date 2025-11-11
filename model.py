from ortools.sat.python import cp_model
from classes import Point, Block
from transformations import unique_block_transformations
from matplotlib import pyplot as plt
from build_inputs import Input

inputs = Input('grid.json','blocks.json')

model = cp_model.CpModel()

all_blocks = {}

def initialise_block_bools(blocks, grid_x, grid_y) -> dict:

    block_bools = dict()

    for block_name, clusters in blocks.items():
        for cluster_id,_ in enumerate(clusters):
            for x_pos in range(grid_x):
                for y_pos in range(grid_y):
                    all_blocks[(block_name,cluster_id,x_pos,y_pos)] = (
                        model.new_bool_var(f'{block_name}_{cluster_id}_{x_pos}_{y_pos}')
                    )

    return block_bools

# all_squares is an int showing the number of blocks that are on that square
all_squares = {}
for x in range(grid_x):
    for y in range(grid_y):
        all_squares[(x,y)] = model.new_int_var(0, len(transformations), f'{x}_{y}')
        if (x,y) in avoid_squares:
            model.add(all_squares[(x,y)] == 0)
        else:
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

colors = {
    'n':'green',
    'b':'black',
    'small_l':'yellow',
    'medium_l':'orange',
    'big_l':'red',
    'short_z':'cornflowerblue',
    'wide_z':'blue',
    'tall_z':'darkblue',
    't':'purple',
    'line':'hotpink',
}
fig, ax = plt.subplots()
fig.set_size_inches(8,8)
ax.set_xlim(0, grid_x)
ax.set_ylim(0, grid_y)

for block_name,block in output.items():

    for point in block.points:

        ax.fill_between([point.x, point.x+1], [point.y, point.y], [point.y+1, point.y+1], color=colors[block_name])

plt.savefig('foo.png')