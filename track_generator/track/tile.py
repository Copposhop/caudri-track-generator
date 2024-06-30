import pygame
import track_generator.config as config


class Tile:

    def __init__(self, grid_position, road_element=None):
        self.set_grip_position(grid_position)
        self.road_element = road_element
        
        self.tile_surface = pygame.Surface((config.tile_size, config.tile_size))
                
    def __repr__(self):
        return f"Tile at {self.grid_position} with road element {self.road_element}"
    
    @property
    def x(self):
        return self.grid_position[0]
    
    @property
    def y(self):
        return self.grid_position[1]
    
    def set_grip_position(self, grid_position):
        if not isinstance(grid_position, tuple) or len(grid_position) != 2:
            raise ValueError("Grid position must be an integer tuple")
        if grid_position[0] < 0 or grid_position[1] < 0:
            raise ValueError("Grid position must be positive")
        self.grid_position = grid_position
        
    def render(self) -> pygame.Surface:
        self.tile_surface.fill(config.color_road)
        if self.road_element:
            self.road_element.render(self.tile_surface)
        return self.tile_surface
        