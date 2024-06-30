import pygame

class Track:
    def __init__(self):
        self.tiles = [] 

    def add_tile(self, new_tile):
        self.tiles.append(new_tile)
        
    def get_tile(self, grid_position):
        for tile in self.tiles:
            if tile.grid_position == grid_position:
                return tile
        return None

    def render(self, screen, scale, offset):
        for tile in self.tiles:
            tile_surface = tile.render()
            tile_surface = pygame.transform.scale_by(tile_surface, (scale, scale))
            screen.blit(tile_surface, (tile.x * scale + offset[0], tile.y * scale + offset[1]))