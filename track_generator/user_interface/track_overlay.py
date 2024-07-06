import pygame
import pygame.gfxdraw

import track_generator.config as config

from track_generator.track.track import Track
from track_generator.track.points import ConnectionPoint, GuidePoint
from pip._vendor.pygments.lexer import include


class TrackOverlay:

    def __init__(self, ui, screen: pygame.Surface, track: Track):
        self.ui = ui
        self.screen = screen
        self.track = track

        self.higlighted_tile = None
        self.selected_tile = None
        self.selected_point = None
        self.selected_point_index = None
        self.point_is_dragging = False
        
    def render(self):
        # Highlight the tile the mouse is hovering over
        if self.higlighted_tile:
            tile_rect = self._get_tile_rect_on_screen(self.higlighted_tile)
            pygame.draw.rect(self.screen, config.color_tile_highlight, tile_rect, config.tile_highlight_border_width)
        if self.selected_tile:
            tile_rect = self._get_tile_rect_on_screen(self.selected_tile)
            pygame.draw.rect(self.screen, config.color_tile_selection, tile_rect, config.tile_selection_border_width)
            self._render_tile_overlay(self.selected_tile)
            
    def set_screen(self, screen):
        self.screen = screen        

    def handle_mouse_press(self, event, position):
        if event.button == pygame.BUTTON_LEFT:
            # Check if a point was clicked and select it
            if self.selected_tile and self.selected_tile.road_element:
                cp = enumerate(self.selected_tile.road_element.connection_points)
                gp = enumerate(self.selected_tile.road_element.guide_points)
                for points in [cp, gp]:
                    for index, point in points:
                        screen_position = self._tile_position_to_screen_position(point.position, self.selected_tile)
                        scaled_radius = config.point_selection_radius * self.ui.track_scale
                        if pygame.Vector2(screen_position).distance_to(position) < scaled_radius:
                            self.selected_point = point
                            self.selected_point_index = index
                            self.point_is_dragging = True
                            return
            
            # Click on a tile to select/deselect it
            for tile in self.track.tiles:
                if self._get_tile_rect_on_screen(tile).collidepoint(position):
                    # Toggle tile selection
                    self.selected_tile = tile if self.selected_tile != tile else None
                    break
            else:
                self.selected_tile = None
        
    def handle_mouse_release(self, event, position):
        if event.button == pygame.BUTTON_LEFT:
            self.point_is_dragging = False
            self.selected_point = None
        
    def handle_mouse_motion(self, position):
        # Update the position of the selected point if it is being dragged
        if self.point_is_dragging:
            tile_position = self._screen_position_to_tile_position(position, self.selected_tile)
            if isinstance(self.selected_point, GuidePoint):
                self.selected_tile.road_element.update_guide_point(self.selected_point_index, tile_position)
            elif isinstance(self.selected_point, ConnectionPoint):
                self.selected_tile.road_element.update_connection_point(self.selected_point_index, tile_position)
        else:
            # Update the tile the mouse is hovering over
            self.higlighted_tile = None
            for tile in self.track.tiles:
                if self._get_tile_rect_on_screen(tile).collidepoint(position):
                    self.higlighted_tile = tile
                    break
        
    def handle_mouse_wheel(self, event):
        self.ui.track_scale = self.ui.track_scale * (1 + event.y * 0.1)
        self.ui.track_scale = max(config.track_min_scale, self.ui.track_scale)
        self.ui.track_scale = min(config.track_max_scale, self.ui.track_scale)
        
    def _render_tile_overlay(self, tile):
        if tile.road_element:
            for cp in tile.road_element.connection_points:
                if cp.twin:
                    color = config.color_connection_point_twin
                else:
                    color = config.color_connection_point
                self._render_point(cp, tile, color)
                self._render_direction_indicator(cp, tile, color)
            for gp in tile.road_element.guide_points:
                self._render_point(gp, tile, config.color_guide_point)
                self._render_direction_indicator(gp, tile, config.color_guide_point)
            if self.selected_point:
                self._render_point(self.selected_point, tile, config.color_selected_point)
                self._render_direction_indicator(self.selected_point, tile, config.color_selected_point)
            
    def _render_point(self, point, tile, color):
        screen_position = self._tile_position_to_screen_position(point.position, tile)
        scaled_radius = config.point_visual_radius * self.ui.track_scale
        pygame.gfxdraw.filled_circle(self.screen, int(screen_position[0]), int(screen_position[1]), int(scaled_radius), color)
        
    def _render_direction_indicator(self, point, tile, color):
        # Draw an arrow indicating the direction of the track point
        if point.direction:
            screen_position = self._tile_position_to_screen_position(point.position, tile)
            scaled_length = config.direction_indicator_length * self.ui.track_scale
            scaled_width = int(config.direction_indicator_width * self.ui.track_scale)
            scaled_arrowhead_length = config.direction_indicator_arrow_length * self.ui.track_scale
            
            direction = pygame.Vector2(point.direction)
            arrowhead_direction = pygame.Vector2(direction).rotate(config.direction_indicator_arrow_angle / 2)

            direction.scale_to_length(scaled_length)
            arrowhead_direction.scale_to_length(scaled_arrowhead_length)
            arrowhead_direction_mirrored = pygame.Vector2(arrowhead_direction).reflect(direction)
            
            pygame.draw.line(self.screen, color, screen_position, screen_position + direction, scaled_width)
            pygame.draw.line(self.screen, color, screen_position + direction, screen_position + direction - arrowhead_direction, scaled_width)
            pygame.draw.line(self.screen, color, screen_position + direction, screen_position + direction + arrowhead_direction_mirrored, scaled_width)
            
    def _tile_position_to_screen_position(self, tile_position, tile):
        screen_x = self.ui.track_offset[0] + self.ui.track_scale * (tile.grid_position[0] * config.tile_size + tile_position[0])
        screen_y = self.ui.track_offset[1] + self.ui.track_scale * (tile.grid_position[1] * config.tile_size + tile_position[1])
        return pygame.Vector2(screen_x, screen_y)
    
    def _screen_position_to_tile_position(self, screen_position, tile):
        tile_x = (screen_position[0] - self.ui.track_offset[0]) / self.ui.track_scale - tile.grid_position[0] * config.tile_size
        tile_y = (screen_position[1] - self.ui.track_offset[1]) / self.ui.track_scale - tile.grid_position[1] * config.tile_size
        return pygame.Vector2(tile_x, tile_y)
    
    def _get_tile_rect_on_screen(self, tile):
        x, y = self._tile_position_to_screen_position((0, 0), tile)
        width = config.tile_size * self.ui.track_scale
        height = config.tile_size * self.ui.track_scale
        return pygame.Rect(x, y, width, height)
        
