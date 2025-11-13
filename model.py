from ortools.sat.python import cp_model
from classes import Point, Cluster
from matplotlib import pyplot as plt
from build_config import Config, Orientation

def create_block_bools(model: cp_model.CpModel, 
                       config: Config
                       ) -> dict[Orientation,cp_model.IntVar]:

    block_bools = dict()

    for block_name, clusters in config.block_clusters.items():
        for cluster_id,_ in enumerate(clusters):
            for x_pos in range(config.grid_x):
                for y_pos in range(config.grid_y):
                    orientation = Orientation(block_name, cluster_id, x_pos, y_pos)
                    block_bools[orientation] = (
                        model.new_bool_var(f'{orientation}')
                    )

    return block_bools

def set_block_conditions(model: cp_model.CpModel, 
                         config: Config, 
                         block_bools: dict[Orientation,cp_model.IntVar]
                         ) -> cp_model.CpModel:

    for block_name in config.block_clusters:

        block_choices = [value for key,value in block_bools.items() if key[0] == block_name]
        model.add_exactly_one(block_choices)

    return model

def create_square_ints(model: cp_model.CpModel, 
                       config: Config
                       ) -> dict[Point,cp_model.IntVar]:

    square_ints = dict()

    for x in range(config.grid_x):
        for y in range(config.grid_y):
            square_point = Point((x,y))
            square_ints[square_point] = model.new_int_var(0, len(config.block_clusters), f'{square_point}')

    return square_ints

def set_square_conditions(model: cp_model.CpModel, 
                          config: Config, 
                          square_ints: dict[Point,cp_model.IntVar]
                          ) -> cp_model.CpModel:       
    
    for x in range(config.grid_x):
        for y in range(config.grid_y):
            
            point = Point((x,y))
            if point in config.grid_exclusions:
                model.add(square_ints[point] == 0)
            else:
                model.add(square_ints[point] == 1)

    return model

def set_touching_conditions(model: cp_model.CpModel, 
                            config: Config, 
                            block_bools: dict[Orientation,cp_model.IntVar], 
                            square_ints: dict[Point,cp_model.IntVar]
                            ):

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

def model_setup(model: cp_model.CpModel, 
                config: Config, 
                block_bools: dict[Orientation,cp_model.IntVar], 
                square_ints: dict[Point,cp_model.IntVar]
                ):

    model = set_block_conditions(model, config, block_bools)
    model = set_square_conditions(model, config, square_ints)
    model = set_touching_conditions(model, config, block_bools, square_ints)

    return model

class AllSolutionsCollector(cp_model.CpSolverSolutionCallback):
    
    def __init__(self, 
                 block_bools: dict[Orientation,cp_model.IntVar], 
                 limit: int = None):

        cp_model.CpSolverSolutionCallback.__init__(self)
        self.block_bools = block_bools
        self.limit = limit  # optional max number of solutions to collect
        self.solutions = []  # list of dicts
        self._count = 0

    def OnSolutionCallback(self):
        self._count += 1
        sol = {var_name: self.Value(var_value) for var_name, var_value in self.block_bools.items()}
        sol = [var_name for var_name,var_value in sol.items() if var_value == 1]
        self.solutions.append(sol)

        # optional: stop if we reached a user limit
        if self.limit is not None and self._count >= self.limit:
            self.StopSearch()

    def solution_count(self):
        return self._count
    
def convert_to_cluster(orientation: Orientation, config: Config) -> Cluster:

    points = list()

    for p in config.block_clusters[orientation.cluster_id].points:

        new_x = orientation + p.x
        new_y = orientation + p.y
        points.append(Point((new_x, new_y)))

    cluster = Cluster(points)
    return cluster

def convert_all_to_cluster(orientations: 
                                list[Orientation], 
                                config:Config
                                ) -> dict[str,Cluster]:

    all_clusters = {o.block_name: convert_to_cluster(o) for o in orientations}

def solve(model: cp_model.CpModel, config: Config) -> list[list[tuple]]:

    block_bools = create_block_bools(model, config)
    square_ints = create_square_ints(model, config)
    model = model_setup(model,config,block_bools,square_ints)

    solver = cp_model.CpSolver()
    collector = AllSolutionsCollector(block_bools, limit=5)
    solver.SearchForAllSolutions(model, collector)



    solutions = collector.solutions

    return solutions

def convert_to_cluster(solution: list[tuple], config: Config) -> dict[str,Cluster]

    final_points = {}
        
        for p in config.block_clusters[solution[1]].points:

                new_x = key[2] + p.x
                new_y = key[3] + p.y

                final_points.append(Point((new_x, new_y)))

def print_solution(solution: list[tuple], config: Config):





model = cp_model.CpModel()
config = Config('grid.json','blocks.json')
bb = solve(model,config)
print(bb)

    





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