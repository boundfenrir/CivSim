# /simulation/tectonics.py

import random
import math
from typing import Dict, List, Tuple
from collections import deque
from simulation.hexgrid import HexGrid, HexTile
from simulation.utils import polar_to_cartesian

class TectonicPlate:
    def __init__(self, plate_id: int):
        self.plate_id = plate_id
        self.tiles: List[HexTile] = []
        self.motion_angle: float = random.uniform(0,2*math.pi) # Radians
        self.motion_speed: float = random.uniform(0.1,1.0) # Arbitrary speed units

    def add_tile(self, tile: HexTile):
        tile.plate_id = self.plate_id
        self.tiles.append(tile)

    def motion_vector(self) -> Tuple[float,float]:
        dx = math.cos(self.motion_angle) * self.motion_speed
        dy = math.sin(self.motion_angle) * self.motion_speed
        return dx,dy

def assign_plates(grid: HexGrid, num_plates: int, seed: int = 42) -> Dict[int, TectonicPlate]:
    random.seed(seed)
    plates: Dict[int, TectonicPlate] = {}

    all_tiles = grid.all_tiles()
    seed_tiles = random.sample(all_tiles, num_plates)

    # Initialize plates with seed tiles
    for plate_id, tile in enumerate(seed_tiles):
        plates[plate_id] = TectonicPlate(plate_id)
        plates[plate_id].add_tile(tile)
        
    ocean_plate_ids = set(random.sample(range(num_plates),2))

    frontier = deque(seed_tiles)

    while frontier:
        current_tile = frontier.popleft()
        current_plate_id = current_tile.plate_id
        if current_plate_id in ocean_plate_ids:
            current_tile.elevation -= 3

        for neighbor in grid.get_neighbors(current_tile):
            if neighbor.plate_id is None:
                plates[current_plate_id].add_tile(neighbor)
                frontier.append(neighbor)

    return plates


def find_plate_boundaries(grid:HexGrid) -> List[HexTile]:
    boundary_tiles: List[HexTile] = []
    for tile in grid.all_tiles():
        for neighbor in grid.get_neighbors(tile):
            if neighbor.plate_id != tile.plate_id:
                boundary_tiles.append(tile)
                break
    return boundary_tiles


def classify_boundaries(grid: HexGrid, plates: Dict[int, TectonicPlate], boundary_tiles: List[HexTile]) -> None:
    for tile in boundary_tiles:
        for neighbor in grid.get_neighbors(tile):
            if neighbor.plate_id is None or neighbor.plate_id == tile.plate_id:
                continue
            
            # Get plate vectors
            plate_a = plates[tile.plate_id]
            plate_b = plates[neighbor.plate_id]

            va = plate_a.motion_vector()
            vb = plate_b.motion_vector()

            ax, ay = polar_to_cartesian(tile.q, tile.r)
            bx, by = polar_to_cartesian(neighbor.q, neighbor.r)

            # Direction vector from A to B
            dx = bx - ax
            dy = by - ay
            mag = math.sqrt(dx**2 + dy**2)
            if mag == 0:
                continue
            nx, ny = dx / mag, dy / mag

            # Dot products
            dot_a = va[0] * nx + va[1] * ny
            dot_b = vb[0] * -nx + vb[1] * -ny

            if dot_a > 0 and dot_b > 0:
                tile.elevation += mag # Convergent
            elif dot_a < 0 and dot_b < 0:
                tile.elevation -= mag # Divergent
            # else neutral/transform

            

def debug_print_plates(grid: HexGrid):
    for tile in grid.all_tiles():
        print(f"Tile {tile.coords()} -> Plate {tile.plate_id}")

def debug_print_elevations(grid: HexGrid):
    for tile in grid.all_tiles():
        print(f"Tile {tile.coords()} -> Elevasion {tile.elevation}")