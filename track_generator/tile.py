import pygame
import track_generator.config as config

class Tile:
    def __init__(self, x, y, road_element):
        self.x = x
        self.y = y
        self.road_element = road_element
        
        self.is_selected = False

    def __repr__(self):
        return f"Tile at ({self.x}, {self.y}) with road element {self.road_element}"

    def render(self, screen, scale, offset):
        tile_surface = pygame.Surface((config.tile_size, config.tile_size))
        tile_surface.fill(config.color_road)
        self.road_element.render(tile_surface)
        
        if self.is_selected:
            # Draw border around tile to indicate selection
            width = config.tile_selection_border_width
            pygame.draw.rect(tile_surface, config.color_tile_selection, (0, 0, config.tile_size - width, config.tile_size - width), width)
            
            # Highlight connection points
            for cp in self.road_element.connection_points:
                point_radius = config.point_selection_radius
                point_offset = config.point_selection_offset
                point_position = cp.position[0] - point_offset * cp.direction[0], cp.position[1] - point_offset * cp.direction[1]
                pygame.draw.circle(tile_surface, config.color_connection_point, point_position, point_radius)
                
                direction_indicator = point_position[0] + 2 * point_radius * cp.direction[0], point_position[1] + 2*  point_radius * cp.direction[1]
                pygame.draw.line(tile_surface, config.color_connection_point, point_position, direction_indicator, point_radius // 2)
                
            for gp in self.road_element.guide_points:
                point_radius = config.point_selection_radius
                point_position = gp[0], gp[1]
                pygame.draw.circle(tile_surface, config.color_guide_point, point_position, point_radius)

        tile_size_scaled = int(config.tile_size * scale)
        scaled_tile_surface = pygame.transform.scale(tile_surface, (tile_size_scaled, tile_size_scaled))

        scaled_x = self.x * tile_size_scaled + offset[0]
        scaled_y = self.y * tile_size_scaled + offset[1]
        screen.blit(scaled_tile_surface, (scaled_x, scaled_y))
        
    def clicked(self, x, y):
        self.is_selected = not self.is_selected
        
    def select(self):
        self.is_highlighted = True
        for cp in self.road_element.connection_points:
            cp.is_highlighted = True
            
    def deselect(self):
        self.is_highlighted = False
        for cp in self.road_element.connection_points:
            cp.is_highlighted = False