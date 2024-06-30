import pygame
import math

import track_generator.config as config

from track_generator.points import ConnectionPoint
from track_generator.points import GuidePoint


class UserInterface:

    def __init__(self, track):
        self.track = track
        
        self.selected_tile = None
        self.selected_point = None
        self.is_dragging = False
        
    def render(self, screen, scale, offset):
        self.screen = screen
        self.scale = scale
        self.offset = offset
        self._render_tile_overlays(screen, scale, offset)
        
    def handle_user_inputs(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self._handle_mouse_press(event.pos)
                
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self._handle_mouse_release()
       
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event.pos)
            
    def _tile_position_to_screen_position(self, tile_position, tile):
        return (
            self.scale * (tile.grid_position[0] * config.tile_size + tile_position[0]) + self.offset[0],
            self.scale * (tile.grid_position[1] * config.tile_size + tile_position[1]) + self.offset[1]            
        )
    
    def _screen_position_to_tile_position(self, screen_position, tile):
        return (
            (screen_position[0] - self.offset[0]) / self.scale - tile.grid_position[0] * config.tile_size,
            (screen_position[1] - self.offset[1]) / self.scale - tile.grid_position[1] * config.tile_size
        )
        
    def _render_tile_overlays(self, screen, scale, offset):
        if self.selected_tile:
            # Draw border around tile to indicate selection
            scaled_width = max(int(config.tile_selection_border_width * scale), 1)
            tile_position = self._tile_position_to_screen_position((0, 0), self.selected_tile)
            rect = (
                tile_position[0],
                tile_position[1],
                config.tile_size * scale,
                config.tile_size * scale
            )
            pygame.draw.rect(screen, config.color_tile_selection, rect, scaled_width)
            
            scaled_point_radius = int(config.point_selection_radius * scale)
            
            # Highlight connection points
            for index, cp in enumerate(self.selected_tile.road_element.connection_points):
                point_position = self._tile_position_to_screen_position(cp.position, self.selected_tile)
                pygame.draw.circle(screen, config.color_connection_point, point_position, scaled_point_radius)

                direction_indicator = (
                    point_position[0] + 2 * scaled_point_radius * cp.direction[0],
                    point_position[1] + 2 * scaled_point_radius * cp.direction[1]
                )
                pygame.draw.line(screen, config.color_connection_point, point_position, direction_indicator, scaled_point_radius // 2)
                
            # Highlight guide points
            for gp in self.selected_tile.road_element.guide_points:
                point_position = self._tile_position_to_screen_position(gp.position, self.selected_tile)
                pygame.draw.circle(screen, config.color_guide_point, point_position, scaled_point_radius)
                
                direction_indicator = (
                    point_position[0] + 2 * scaled_point_radius * gp.direction[0],
                    point_position[1] + 2 * scaled_point_radius * gp.direction[1]
                )
                pygame.draw.line(screen, config.color_guide_point, point_position, direction_indicator, scaled_point_radius // 2)
                                
            # Highlight selected point
            if self.selected_point:
                point_position = self.selected_point.position
                point_position = (tile_position[0] + point_position[0] * scale, tile_position[1] + point_position[1] * scale)
                pygame.draw.circle(screen, config.color_selected_point, point_position, 1.2 * scaled_point_radius)
                
    def _handle_mouse_press(self, position):
        mouse_x, mouse_y = position
        if self.selected_tile:
            # Check if a connection point on the currently selected tile was clicked
            for cp_index, cp in enumerate(self.selected_tile.road_element.connection_points):
                cp_position = self._tile_position_to_screen_position(cp.position, self.selected_tile)
                cp_radius = 2 * config.point_selection_radius * self.scale
                if math.hypot(cp_position[0] - mouse_x, cp_position[1] - mouse_y) < cp_radius:
                    self.selected_point = cp
                    self.selected_point_index = cp_index
                    self.is_dragging = True
                    break
            # Check if a guide point on the currently selected tile was clicked
            for gp_index, gp in enumerate(self.selected_tile.road_element.guide_points):
                gp_position = self._tile_position_to_screen_position(gp.position, self.selected_tile)
                gp_radius = 2 * config.point_selection_radius * self.scale
                if math.hypot(gp_position[0] - mouse_x, gp_position[1] - mouse_y) < gp_radius:
                    self.selected_point = gp
                    self.selected_point_index = gp_index
                    self.is_dragging = True
                    break
                
        # Check if a tile was clicked and toggle selection
        if not self.is_dragging:
            for tile in self.track.tiles:
                tile_size_scaled = config.tile_size * self.scale
                tile_grid_position = tile.grid_position
                tile_rect = pygame.Rect(
                    tile_grid_position[0] * tile_size_scaled + self.offset[0],
                    tile_grid_position[1] * tile_size_scaled + self.offset[1],
                    tile_size_scaled,
                    tile_size_scaled
                )
                if tile_rect.collidepoint(mouse_x, mouse_y):
                    print(f"Clicked tile at {tile.grid_position}")
                    self._click_tile(tile)
    
    def _handle_mouse_release(self):
        # Reset dragging state
        self.is_dragging = False
        self.selected_point = None
    
    def _handle_mouse_motion(self, position):
        # Update position of selected point if dragging
        if self.is_dragging:
            mouse_x, mouse_y = position
            if isinstance(self.selected_point, ConnectionPoint):
                position_on_tile = self._screen_position_to_tile_position((mouse_x, mouse_y), self.selected_tile)
                self.selected_tile.road_element.update_connection_point(self.selected_point_index, position_on_tile)
            elif isinstance(self.selected_point, GuidePoint):
                position_on_tile = self._screen_position_to_tile_position((mouse_x, mouse_y), self.selected_tile)
                self.selected_tile.road_element.update_guide_point(self.selected_point_index, position_on_tile)
    
    def _click_tile(self, tile):
        # Toggle selection of tile
        if tile == self.selected_tile:
            self.selected_tile = None
        else: 
            self.selected_tile = tile
