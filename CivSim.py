#import sys
import matplotlib.pyplot as plt
from simulation.hexgrid import HexGrid
from simulation.tectonics import assign_plates, find_plate_boundaries, classify_boundaries, debug_print_plates, debug_print_elevations
from simulation.biomes import compute_moisture, assign_biomes
from visualization.render import render_grid, render_elevation

def main():
    #print(sys.executable)
    #print(sys.path)
    grid = HexGrid(radius=15)
    plates = assign_plates(grid, num_plates=9, num_oceans=3)
    boundary_tiles = find_plate_boundaries(grid)
    classify_boundaries(grid,plates,boundary_tiles)
    compute_moisture(grid)
    assign_biomes(grid)
    print(f"Total tiles: {len(grid.all_tiles())}")

    fig, axes = plt.subplots(2,2,figsize=(10,10))
    render_grid(grid,color_by="plate", plates = plates, ax=axes[0][0])
    render_grid(grid,color_by="elevation", ax=axes[1][0])
    render_grid(grid,color_by="moisture", ax=axes[0][1])
    render_grid(grid,color_by="biome", ax=axes[1][1])
    plt.show()

if __name__ == "__main__":
    main()
