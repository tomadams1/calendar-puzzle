from classes import Point, Cluster
from transformations import unique_cluster_orientations
import json

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

class Input:

    def __init__(self, grid_file, block_file):
        
        grid_json = load_grid_json(grid_file)
        self.grid_exclusions = get_grid_exclusions(grid_json)
        self.grid_x = grid_json['grid_x']
        self.grid_y = grid_json['grid_y']

        block_json = load_block_json(block_file)
        self.block_clusters = get_block_clusters(block_json)