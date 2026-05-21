import pygame
import data_class

def Debug_show(data : data_class.Data_class) -> None:
    """
    Debuging overlay.
    Show the sorted world and the sorted path.
    """
    # Show sorted_path
    for i in range(len(data.sorted_path)):
        percentage : float = i / max(1, len(data.sorted_path)-1)
        color : tuple[int, int, int] = (
            int(255 * percentage),
            int(255 * (1-percentage)),
            0
        )
        # Draw an alpha-tile
        tile_surface : pygame.Surface = pygame.Surface((data.tile_zoom*12, data.tile_zoom*12), pygame.SRCALPHA)
        tile_surface.fill((color[0], color[1], color[2], 100))
        data.screen.blit(tile_surface, data.Get_World_to_Screen(data.sorted_path[i]))
        

    # Show weight-value of tiles
    for x in range(len(data.world[0])):
        for y in range(len(data.world)):
            if data._weighted_world[y][x] != 9999:
                data.Draw_text(str(data._weighted_world[y][x]), data.Get_World_to_Screen((x, y)), 6*data.tile_zoom, (0, 0, 0))