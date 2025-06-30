# /visualization/render.py

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as mcolors
from simulation.hexgrid import HexGrid, HexTile
from simulation.utils import polar_to_cartesian

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
        case _:
            print(f"Unknown color mode: {color_by}")

    ax.autoscale()
    ax.axis('off')

def render_plate_arrows(grid:HexGrid, plates: dict, ax):
    for plate in plates.values():
        if not plate.tiles:
            continue
        seed_tile = plate.tiles[0]
        x, y = polar_to_cartesian(seed_tile.q, seed_tile.r)
        dx, dy = plate.motion_vector()
        ax.arrow(x,y,dx,dy,head_width=0.3,head_length=0.3,fc='black', ec='black')


def render_plate_map(grid:HexGrid, ax):
    # Generate a color map
    color_map = list(mcolors.TABLEAU_COLORS.values()) + list(mcolors.CSS4_COLORS.values())

    for tile in grid.all_tiles():
        x,y = polar_to_cartesian(tile.q, tile.r)

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
    max_abs = max(abs(min_el),abs(max_el))
    span = max_abs * 2.4

    cmap = plt.cm.terrain
    norm = plt.Normalize(vmin=-max_abs,vmax=max_abs*1.4)

    for tile in grid.all_tiles():
        x, y = polar_to_cartesian(tile.q, tile.r)
        norm_el = (tile.elevation - min_el) / span
        color = plt.cm.terrain(norm_el)
        draw_hex(ax,x,y,size=1.0,color=color)

    sm = plt.cm.ScalarMappable(cmap=cmap,norm=norm)
    sm.set_array([])
    plt.colorbar(sm,ax=ax,orientation='vertical', fraction=0.046, pad=0.04,label="Elevasion")