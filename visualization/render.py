# /visualization/render.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D
from simulation.hexgrid import HexGrid, HexTile
from simulation.biomes import Biome, BIOME_COLORS
from simulation.utils import hex_to_pixel

import math

def draw_hex(ax,x,y,size,color):
    angles = [math.radians(60*i) for i in range(6)]
    points = [
        (x + size * math.cos(a), y + size * math.sin(a))
        for a in angles
    ]
    hex_patch = patches.Polygon(points,closed = True, edgecolor='k', facecolor=color,linewidth=0.5)
    ax.add_patch(hex_patch)

def render_grid(grid: HexGrid, color_by="plate", plates: dict = None, ax=None):
    if ax is None:
        fig, ax = plt.subplits(figsize=(10,10))

    ax.set_aspect('equal')

    match color_by:
        case "plate":
            render_plate_map(grid,ax)
            if plates is not None:
                render_plate_arrows(grid,plates,ax)
            ax.set_title("Tectonic Plates")
        case "elevation":
            render_elevation(grid,ax)
            ax.set_title("Elevation Map")
        case "biome":
            render_biome_map(grid,ax)
            ax.set_title("Biomes")
        case "moisture":
            render_moisture_map(grid,ax)
            ax.set_title("Moisture")
        case _:
            print(f"Unknown color mode: {color_by}")

    ax.autoscale()
    ax.axis('off')

def render_plate_arrows(grid:HexGrid, plates: dict, ax):
    for plate in plates.values():
        if not plate.tiles:
            continue
        seed_tile = plate.tiles[0]
        x, y = hex_to_pixel(seed_tile.q, seed_tile.r)
        dx, dy = plate.motion_vector()
        ax.arrow(x,y,dx,dy,head_width=0.3,head_length=0.3,fc='black', ec='black')


def render_plate_map(grid:HexGrid, ax):
    # Generate a color map
    color_map = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())

    for tile in grid.all_tiles():
        x,y = hex_to_pixel(tile.q, tile.r)

        if tile.plate_id is not None:
            color = color_map[tile.plate_id % len(color_map)]
        else:
            color = 'lightgray'

        draw_hex(ax, x, y, size=1.0, color=color)
        

def render_elevation(grid: HexGrid, ax):
    # Compute min/max for normalization
    elevations = [tile.elevation for tile in grid.all_tiles()]
    min_el = min(elevations)
    max_el = max(elevations)
    #max_abs = max(abs(min_el),abs(max_el))
    span = max_el - min_el

    cmap = plt.cm.terrain
    norm = plt.Normalize(vmin=min_el,vmax=max_el)

    for tile in grid.all_tiles():
        x, y = hex_to_pixel(tile.q, tile.r)
        norm_el = (tile.elevation - min_el) / span
        color = plt.cm.terrain(norm_el)
        draw_hex(ax,x,y,size=1.0,color=color)

    sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
    sm.set_array([])
    plt.colorbar(sm,ax=ax,orientation='vertical', fraction=0.046, pad=0.04,label="Elevasion")

def render_biome_map(grid: HexGrid, ax):
    for tile in grid.all_tiles():
        x, y = hex_to_pixel(tile.q, tile.r)
        color = BIOME_COLORS.get(tile.biome,"#000000")
        draw_hex(ax, x, y, size=1.0, color=color)

    legend_elements = [
     Line2D([0],[0],marker='s',color='w', 
            label=biome.name,
            markerfacecolor=color, markersize=10)
     for biome, color in BIOME_COLORS.items()
    ]
    ax.legend(handles=legend_elements, loc='lower left', bbox_to_anchor=(1.01,0), borderaxespad=0.)

def render_moisture_map(grid: HexGrid, ax):
    moistures = [tile.moisture for tile in grid.all_tiles()]
    cmap = plt.cm.Blues
    norm = plt.Normalize(vmin=0.0, vmax=1.0)

    for tile in grid.all_tiles():
        x, y = hex_to_pixel(tile.q, tile.r)
        color = cmap(norm(tile.moisture))
        draw_hex(ax, x, y, size=1.0, color=color)

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, orientation='vertical', fraction=0.046, pad=0.04, label='Moisture')