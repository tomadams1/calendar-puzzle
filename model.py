from ortools.sat.python.cp_model import CpModel
from classes import Point, Cluster
from matplotlib import pyplot as plt
from build_config import Config

def create_block_bools(model: CpModel, config: Config) -> dict:

    block_bools = dict()

    for block_name, clusters in config.block_clusters.items():
        for cluster_id,_ in enumerate(clusters):
            for x_pos in range(config.grid_x):
                for y_pos in range(config.grid_y):
                    block_bools[(block_name,cluster_id,x_pos,y_pos)] = (
                        model.new_bool_var(f'{block_name}_{cluster_id}_{x_pos}_{y_pos}')
                    )

    return block_bools

def set_block_conditions(model: CpModel, config: Config, block_bools: dict):

    for block_name in config.block_clusters:

        block_choices = [value for key,value in block_bools.items() if key[0] == block_name]
        print(block_choices)
        model.add_exactly_one(block_choices)

    return model

def create_square_ints(model, config: Config) -> dict:

    square_ints = dict()

    for x in range(config.grid_x):
        for y in range(config.grid_y):
            square_ints[(x,y)] = model.new_int_var(0, len(config.block_clusters), f'{x}_{y}')

    return square_ints

def set_square_conditions(model: CpModel, config: Config, square_ints: dict) -> CpModel:       
    
    for x in range(config.grid_x):
        for y in range(config.grid_y):

            if Point((x,y)) in config.grid_exclusions:
                model.add(square_ints[(x,y)] == 0)
            else:
                model.add(square_ints[(x,y)] == 1)

    return model

def set_touching_conditions(model: CpModel, config: Config, block_bools, square_ints):

    # Each square has the value of the number of blocks that are lying on it
    for sq_x in range(config.grid_x):
        for sq_y in range(config.grid_y):

            pointing_at_square = list()

            for block_name, clusters in config.block_clusters.items():
                for cluster_id, cluster in enumerate(clusters):
                    for x in range(config.grid_x):
                        for y in range(config.grid_y):
                            for p in cluster.points:

                                fx = x + p.x
                                fy = y + p.y

                                if (fx==sq_x) & (fy==sq_y):

                                    pointing_at_square.append(block_bools[(block_name,cluster_id,x,y)])

            model.add(square_ints[sq_x,sq_y] == sum(pointing_at_square))

    return model

def model_setup(model: CpModel, config: Config):

    block_bools = create_block_bools(model, config)
    print(block_bools)
    square_ints = create_square_ints(model, config)

    model = set_block_conditions(model, config, block_bools)
    model = set_square_conditions(model, config, square_ints)
    model = set_touching_conditions(model, config, block_bools, square_ints)

    return model

config = Config('grid.json','blocks.json')
model = CpModel()
model = model_setup(model, config)

solver = model.CpSolver()
solution_printer = model.ObjectiveSolutionPrinter()
status = solver.solve(model, solution_printer)

output = dict()

# for block in blocks:

#     all_matches = {key:value for key,value in all_blocks.items() if (key[0] == block)}

#     for key,value in all_matches.items():

#         if solver.boolean_value(value):

#             # print(f'Place {block} at position ({key[2]},{key[3]})')
#             # print(transformations[block][key[1]])
            
#             final_points = []
#             for p in transformations[block][key[1]].points:

#                 new_x = key[2] + p.x
#                 new_y = key[3] + p.y

#                 final_points.append(Point((new_x, new_y)))

#             output[block] = Block(final_points)

# print(output)

# colors = {
#     'n':'green',
#     'b':'black',
#     'small_l':'yellow',
#     'medium_l':'orange',
#     'big_l':'red',
#     'short_z':'cornflowerblue',
#     'wide_z':'blue',
#     'tall_z':'darkblue',
#     't':'purple',
#     'line':'hotpink',
# }
# fig, ax = plt.subplots()
# fig.set_size_inches(8,8)
# ax.set_xlim(0, grid_x)
# ax.set_ylim(0, grid_y)

# for block_name,block in output.items():

#     for point in block.points:

#         ax.fill_between([point.x, point.x+1], [point.y, point.y], [point.y+1, point.y+1], color=colors[block_name])

# plt.savefig('foo.png')