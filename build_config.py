from classes import Point, Cluster
from transformations import unique_cluster_orientations
import json
from ortools.sat.python.cp_model import CpModel

def load_grid_json(grid_file: str):

    with open(grid_file) as file:
        grid_json = json.load(file)

    return grid_json

def get_grid_exclusions(grid_json) -> list[Point]:

    excluded_co_ords = [Point(p) for p in grid_json['excluded_squares']]

    return excluded_co_ords

def load_block_json(block_file: str):

    with open(block_file) as file:
        block_json = json.load(file)

    return block_json

def get_block_clusters(block_json) -> dict[str,list[Cluster]]:

    initial_clusters = {
        block_name: Cluster([Point(p) for p in points]) for block_name,points in block_json.items()
        }
    
    block_clusters = {
        block_name:unique_cluster_orientations(cluster) for block_name,cluster in initial_clusters.items()
        }

    return block_clusters

class Config:

    def __init__(self, grid_file, block_file):
        
        grid_json = load_grid_json(grid_file)
        self.grid_exclusions = get_grid_exclusions(grid_json)
        self.grid_x = grid_json['grid_x']
        self.grid_y = grid_json['grid_y']

        block_json = load_block_json(block_file)
        self.block_clusters = get_block_clusters(block_json)

class Orientation:

    def __init__(self, block_name, cluster_id, x_pos, y_pos):

        self.block_name = block_name
        self.cluster_id = cluster_id
        self.x_pos = x_pos
        self.y_pos = y_pos

    def __repr__(self):

        return f"{self.block_name}_{self.cluster_id}_{self.x}_({self.y})"

class Beans:

    def __init__(self, model, block_bools):

        self.model = model
        self.block_bools = block_bools

    