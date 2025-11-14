from ortools.sat.python import cp_model
from classes import Point, Cluster
from matplotlib import pyplot as plt
from build_config import Config, Orientation
import os

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

        block_choices = [value for key,value in block_bools.items() if key.block_name == block_name]
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

            point = Point((sq_x,sq_y))

            pointing_at_square = list()

            for block_name, clusters in config.block_clusters.items():
                for cluster_id, cluster in enumerate(clusters):
                    for x in range(config.grid_x):
                        for y in range(config.grid_y):
                            for p in cluster.points:
                                
                                fx = x + p.x
                                fy = y + p.y

                                if (fx==sq_x) & (fy==sq_y):
                                    
                                    orientation = Orientation(block_name,cluster_id,x,y)
                                    pointing_at_square.append(block_bools[orientation])

            model.add(square_ints[point] == sum(pointing_at_square))

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

    for p in config.block_clusters[orientation.block_name][orientation.cluster_id].points:

        new_x = orientation.x_pos + p.x
        new_y = orientation.y_pos + p.y
        points.append(Point((new_x, new_y)))

    cluster = Cluster(points)
    return cluster

def convert_all_to_cluster(orientations: list[Orientation], 
                           config:Config
                           ) -> dict[str,Cluster]:

    all_clusters = {o.block_name: convert_to_cluster(o,config) for o in orientations}

    return all_clusters

def solve(model: cp_model.CpModel, config: Config) -> list[dict[str,Cluster]]:

    block_bools = create_block_bools(model, config)
    square_ints = create_square_ints(model, config)
    model = model_setup(model,config,block_bools,square_ints)

    solver = cp_model.CpSolver()
    collector = AllSolutionsCollector(block_bools, limit=None)
    solver.SearchForAllSolutions(model, collector)

    solutions = [convert_all_to_cluster(sol, config) for sol in collector.solutions]

    return solutions

cmap = {
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

def plot_solution(solution: dict[str,Cluster], config:Config, cmap: dict[str,str], file_name):

    fig, ax = plt.subplots()
    fig.set_size_inches(8,8)
    ax.set_xlim(0, config.grid_x)
    ax.set_ylim(0, config.grid_y)

    for block_name,cluster in solution.items():

        for point in cluster.points:

            ax.fill_between([point.x, point.x+1], [point.y, point.y], [point.y+1, point.y+1], color=cmap[block_name])

    plt.savefig(file_name)
    plt.close()

def plot_all(list_of_solutions, config, cmap, folder):

    os.mkdir(folder)

    for i,solution in enumerate(list_of_solutions):
        print(f'Plotting solution {i}')
        plot_solution(solution, config, cmap, f'{folder}/solution_{i}.png')

model = cp_model.CpModel()
config = Config('grid.json','blocks.json')
solutions = solve(model,config)
plot_all(solutions, config, cmap, 'first_test')

import os
import imageio
images = []
for filename in os.listdir('first_test'):
    images.append(imageio.imread(f'first_test/{filename}'))
imageio.mimsave('movie.gif', images)
