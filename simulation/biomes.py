
from collections import deque
from enum import Enum, auto
from simulation.hexgrid import HexGrid, HexTile

class Biome(Enum):
    OCEAN = auto()
    DESERT = auto()
    STEPPE = auto()
    PLAIN = auto()
    RAINFOREST = auto()
    SWAMP = auto()
    ALPINEDESERT = auto()
    ALPINESHRUBLAND = auto()
    TUNDRA = auto()
    TAIGA = auto()
    
BIOME_COLORS = {
    Biome.OCEAN: "#1f78b4",           # Deep Blue
    Biome.DESERT: "#edc9af",          # Sandy
    Biome.STEPPE: "#c2b280",          # Dry grass
    Biome.PLAIN: "#88cc44",           # Light green
    Biome.RAINFOREST: "#228b22",      # Forest green
    Biome.SWAMP: "#556b2f",           # Dark olive
    Biome.ALPINEDESERT: "#808080",    # Grey (rocky)
    Biome.ALPINESHRUBLAND: "#a9a9a9", # Light grey
    Biome.TUNDRA: "#ffffff",          # White (snow/ice)
    Biome.TAIGA: "#2e8b57"            # Sea green (cold forest)
}

def compute_moisture(grid: HexGrid, decay: float = 0.15) -> None:
    frontier = deque()
    visited = set()

    for tile in grid.all_tiles():
        if tile.elevation < 0:
            tile.moisture = 1.0
            frontier.append(tile)

    while frontier:
        current = frontier.popleft()
        for neighbor in grid.get_neighbors(current):
            
            elevation_factor = max(0.0, min(1,1.0 - 2*(current.elevation - neighbor.elevation)))
            propagated = min(1,current.moisture * (1.0 - decay) * elevation_factor)

            if propagated > neighbor.moisture:
                neighbor.moisture = propagated
                frontier.append(neighbor)

def assign_biomes(grid: HexGrid) -> None:
    for tile in grid.all_tiles():
        if tile.elevation < 0:
            tile.biome = Biome.OCEAN
        elif tile.elevation < 5:
            if tile.moisture == 0:
                tile.biome = Biome.DESERT
            elif tile.moisture < 0.3:
                tile.biome = Biome.STEPPE
            elif tile.moisture < 0.5:
                tile.biome = Biome.PLAIN
            elif tile.moisture < 0.9:
                tile.biome = Biome.RAINFOREST
            else:
                tile.biome = Biome.SWAMP
        elif tile.elevation < 7:
            if tile.moisture == 0:
                tile.biome = Biome.ALPINEDESERT
            elif tile.moisture < 0.3:
                tile.biome = Biome.ALPINESHRUBLAND
            elif tile.moisture < 0.5:
                tile.biome = Biome.TUNDRA
            else:
                tile.biome = Biome.TAIGA
        else:
            if tile.moisture < 0.5:
                tile.biome = Biome.ALPINEDESERT
            else:
                tile.biome = Biome.TUNDRA

