import pygame
import track_generator.config as config

class Tile:
    def __init__(self, x, y, road_element):
        self.x = x
        self.y = y
        self.road_element = road_element

    def __repr__(self):
        return f"Tile at ({self.x}, {self.y}) with road element {self.road_element}"

    def render(self, screen, scale, offset):
        tile_surface = pygame.Surface((config.tile_size, config.tile_size))
        tile_surface.fill(config.color_road)
        self.road_element.render(tile_surface)

        tile_size_scaled = int(config.tile_size * scale)
        scaled_tile_surface = pygame.transform.scale(tile_surface, (tile_size_scaled, tile_size_scaled))

        scaled_x = self.x * tile_size_scaled + offset[0]
        scaled_y = self.y * tile_size_scaled + offset[1]
        screen.blit(scaled_tile_surface, (scaled_x, scaled_y))