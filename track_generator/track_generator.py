import pygame
import math

import track_generator.config as config
from track_generator.track import Track


class TrackGenerator:
    def __init__(self):
        self.init_pygame()
        
        self.running = True
        self.scale = 0.1
        self.offset = [10, 10]
        self.pan_speed = 20
        
        self.tile_selected = None
        self.dragging_point = None
        
        self.track = Track()

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption('CAuDri-Challenge Track Generator')
        
    def update(self):
        self._event_handler()
       
        self.screen.fill(config.color_background)
        self.track.render(self.screen, self.scale, self.offset)
        pygame.display.flip()
        
    def _event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.offset[1] += self.pan_speed
                elif event.key == pygame.K_DOWN:
                    self.offset[1] -= self.pan_speed
                elif event.key == pygame.K_LEFT:
                    self.offset[0] += self.pan_speed
                elif event.key == pygame.K_RIGHT:
                    self.offset[0] -= self.pan_speed
            elif event.type == pygame.MOUSEWHEEL:
                self.scale = max(self.scale * (1 + event.y * 0.1), 0.05)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_x, mouse_y = event.pos
                    # Check if a connection point was clicked and select it
                    if self.tile_selected:
                        for cp_index, cp in enumerate(self.tile_selected.road_element.connection_points):
                            cp_position = (cp.position[0] * self.scale + self.offset[0], cp.position[1] * self.scale + self.offset[1])
                            cp_radius = 1.5 * config.point_selection_radius
                            if math.hypot(cp_position[0] - mouse_x, cp_position[1] - mouse_y) < cp_radius:
                                print(f"Clicked on connection point {cp}")
                                cp.is_dragging = True
                                self.dragging_point = (self.tile_selected, cp_index)
                                break 

                    # Check if a tile was clicked and select it
                    if not self.dragging_point:
                        for tile in self.track.tiles:
                            tile_size_scaled = config.tile_size * self.scale
                            tile_rect = pygame.Rect(tile.x * tile_size_scaled + self.offset[0], tile.y * tile_size_scaled + self.offset[1], tile_size_scaled, tile_size_scaled)
                            if tile_rect.collidepoint(mouse_x, mouse_y):
                                print(f"Clicked on tile {tile}")
                                tile.clicked(mouse_x - tile.x * tile_size_scaled - self.offset[0], mouse_y - tile.y * tile_size_scaled - self.offset[1])
                                self.tile_selected = tile
                                break
                            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 and self.dragging_point:
                    tile, cp_index = self.dragging_point
                    tile.road_element.connection_points[cp_index].is_dragging = False
                    self.dragging_point = None
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging_point:
                    tile, cp_index = self.dragging_point
                    mouse_x, mouse_y = event.pos
                    new_position = ((mouse_x - self.offset[0]) / self.scale, (mouse_y - self.offset[1]) / self.scale)
                    tile.road_element.update_connection_points(cp_index, new_position, tile.road_element.direction)
        