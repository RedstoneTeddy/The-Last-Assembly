import random

import data_class


def Create_floor_patches(data : data_class.Data_class) -> None:
    """
    For the whole map whose tiles start with "floor_" create noisy patches to make it look more natural.
    Therefore make the base map floor_1 and patches of floor_21
    """
    if not data.world:
        return

    seed_density : float = 0.3
    smooth_iterations : int = 2
    broken_chance : float = 0.2

    floor_mask : list[list[bool]] = []
    patch_mask : list[list[bool]] = []

    for row in data.world:
        floor_row : list[bool] = []
        patch_row : list[bool] = []
        for tile in row:
            is_floor = isinstance(tile, str) and tile.startswith("floor_")
            floor_row.append(is_floor)
            patch_row.append(is_floor and random.random() < seed_density)
        floor_mask.append(floor_row)
        patch_mask.append(patch_row)

    def Count_neighbors(y: int, x: int) -> int:
        count = 0
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                ny = y + dy
                nx = x + dx
                if 0 <= ny < len(patch_mask) and 0 <= nx < len(patch_mask[ny]):
                    if floor_mask[ny][nx] and patch_mask[ny][nx]:
                        count += 1
        return count

    for _ in range(smooth_iterations):
        new_mask : list[list[bool]] = []
        for y, row in enumerate(patch_mask):
            new_row : list[bool] = []
            for x, _ in enumerate(row):
                if not floor_mask[y][x]:
                    new_row.append(False)
                    continue
                neighbors = Count_neighbors(y, x)
                if neighbors >= 5:
                    new_row.append(True)
                elif neighbors <= 2:
                    new_row.append(False)
                else:
                    new_row.append(patch_mask[y][x])
            new_mask.append(new_row)
        patch_mask = new_mask

    for y, row in enumerate(data.world):
        for x, _ in enumerate(row):
            if floor_mask[y][x]:
                data.world[y][x] = "floor_21" if patch_mask[y][x] else "floor_1"

    # Randomize the chosen floor tiles a bit
    for y, row in enumerate(data.world):
        for x, tile in enumerate(row):
            if tile.startswith("floor_"):
                if random.random() < broken_chance:
                    current_floor_id : int = int(tile.split("_")[1])
                    new_floor_id : int = current_floor_id + random.randint(1, 19)
                    data.world[y][x] = f"floor_{new_floor_id}"

    # Randomize the chosen acid tiles a bit
    for y, row in enumerate(data.world):
        for x, tile in enumerate(row):
            if tile.startswith("acid_"):
                old_acid_id : int = int(tile.split("_")[1])
                if old_acid_id <= 10:
                    new_acid_id : int = random.randint(1, 10)
                    data.world[y][x] = f"acid_{new_acid_id}"
