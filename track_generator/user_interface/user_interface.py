import pygame
import os

import track_generator.config as config

# fonts folder in file directory
font_file_path = os.path.join(os.path.dirname(__file__), "fonts", "Rajdhani-SemiBold.ttf")

class UserInterface:

    def __init__(self, track):
        self.screen = pygame.display.get_surface()
        
        self.track = track
        
        self.top_bar_height = config.ui_top_bar_height
        self.track_position = [10, 10]
        self.track_scale = config.track_default_scale
        
        self._update_layout()
        
        self.selected_tile = None
        self.selected_point = None
        self.point_is_dragging = False
        
    def render(self) -> None:
        self.screen.fill(config.color_background)
        self._render_track()
        self._render_top_bar()
        
        pygame.display.flip()
        
    def handle_user_inputs(self, event) -> None:
        if event.type == pygame.KEYDOWN:
            self._handle_keydown(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_press(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_release(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEWHEEL:
            self._handle_mouse_wheel(event)
        elif event.type == pygame.VIDEORESIZE:
            self._update_layout()
            
    def _update_layout(self):
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()
        
        track_screen_width = self.screen_width - 2 * config.ui_track_padding
        track_screen_height = self.screen_height - self.top_bar_height - 2 * config.ui_track_padding
        self.track_rect = pygame.Rect(config.ui_track_padding, self.top_bar_height + config.ui_track_padding, track_screen_width, track_screen_height)
        self.track_screen = pygame.Surface((track_screen_width, track_screen_height))
    
    def _render_track(self) -> None:
        self.track_screen.fill(config.color_track_background)
        self.track.render(self.track_screen, self.track_scale, self.track_position)   
        self.screen.blit(self.track_screen, (config.ui_track_padding, self.top_bar_height + config.ui_track_padding))
        
    def _render_top_bar(self) -> None:
        padding = config.ui_track_padding
        top_bar_surface = pygame.Surface((self.screen_width - 2 * padding, config.ui_top_bar_height))
        text = f"CAuDri-Challenge Track Generator"
        font = pygame.font.Font(font_file_path, config.ui_top_bar_height // 2)
        text_surface = font.render(text, True, (10,10,10))
        text_rect = text_surface.get_rect(center=(top_bar_surface.get_width() // 2, top_bar_surface.get_height() // 2))
        top_bar_surface.fill(config.color_background)
        top_bar_surface.blit(text_surface, text_rect)
        self.screen.blit(top_bar_surface, (padding, 0))
        
        
    def _move_track(self, dx, dy):
        new_pos_x = self.track_position[0] + dx
        new_pos_y = self.track_position[1] + dy
        self.track_position = [new_pos_x, new_pos_y]

    def _handle_keydown(self, event) -> None:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
        if event.key == pygame.K_UP:
            self._move_track(0, config.pan_speed)
        elif event.key == pygame.K_DOWN:
            self._move_track(0, -config.pan_speed)
        elif event.key == pygame.K_LEFT:
            self._move_track(config.pan_speed, 0)
        elif event.key == pygame.K_RIGHT:
            self._move_track(-config.pan_speed, 0)
            
    def _handle_mouse_press(self, event) -> None:
        pass
    
    def _handle_mouse_release(self, event) -> None:
        if event.button == 1:
            self.point_is_dragging = False
    
    def _handle_mouse_motion(self, event) -> None:
        # If the middle mouse button is pressed, move the track
        if event.buttons[1]:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            dx, dy = event.rel
            self._move_track(dx, dy)
    
    def _handle_mouse_wheel(self, event) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.track_rect.collidepoint(mouse_pos):
            self.track_scale = self.track_scale * (1 + event.y * 0.1)
            self.track_scale = max(config.track_min_scale, self.track_scale)
            self.track_scale = min(config.track_max_scale, self.track_scale)