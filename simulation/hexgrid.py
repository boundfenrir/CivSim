# /simulation/hexgrid.py

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

@dataclass
class HexTile:
    q: int
    r: int
    elevation: float = 0.0
    biome: str = "unknown"
    plate_id: Optional[int] = None
    culture_id: Optional[int] = None

    @property
    def s(self) -> int:
        return -self.q - self.r

    def coords(self) -> Tuple[int, int, int]:
        return (self.q, self.r, self.s)


class HexGrid:
    # Axial directions for neighbor lookup
    DIRECTIONS = [
        (+1, 0), (0, +1), (-1, +1),
        (-1, 0), (0, -1), (+1, -1)
    ]

    def __init__(self, radius: int):
        self.radius = radius
        self.tiles: Dict[Tuple[int, int], HexTile] = {}
        self._generate_grid()

    def _generate_grid(self) -> None:
        for q in range(-self.radius, self.radius + 1):
            r1 = max(-self.radius, -q - self.radius)
            r2 = min(self.radius, -q + self.radius)
            for r in range(r1, r2 + 1):
                self.tiles[(q, r)] = HexTile(q, r)

    def get_tile(self, q: int, r: int) -> Optional[HexTile]:
        return self.tiles.get((q, r))

    def get_neighbors(self, tile: HexTile) -> List[HexTile]:
        neighbors = []
        for dq, dr in self.DIRECTIONS:
            neighbor = self.get_tile(tile.q + dq, tile.r + dr)
            if neighbor:
                neighbors.append(neighbor)
        return neighbors

    def all_tiles(self) -> List[HexTile]:
        return list(self.tiles.values())