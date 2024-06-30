import pygame

import track_generator.config as config
from track_generator.track.tile import Tile


class Track:
    def __init__(self):
        self.tiles = [] 

    def add_tile(self, grid_position, road_element=None):
        self.tiles.append(Tile(grid_position, road_element))

    def get_tile(self, grid_position):
        for tile in self.tiles:
            if tile.grid_position == grid_position:
                return tile
        return None

    def render(self, screen, scale, offset):
        for tile in self.tiles: 
            tile_surface = pygame.transform.scale_by(tile.render(), (scale, scale))
            tile_offset = (config.tile_size * tile.x * scale + offset[0], config.tile_size * tile.y * scale + offset[1])
            
            screen.blit(tile_surface, tile_offset)