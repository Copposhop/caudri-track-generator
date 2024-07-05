import pygame
import os

import track_generator.config as config
from track_generator.user_interface.track_overlay import TrackOverlay
from track_generator.exceptions import InvalidTrackError

# fonts folder in file directory
font_file_path = os.path.join(os.path.dirname(__file__), "fonts", "Rajdhani-SemiBold.ttf")


class UserInterface:

    def __init__(self, track):
        self.track = track
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
                
        self.track_screen =  None
        self.track_overlay = TrackOverlay(self, self.track_screen, track)
        self.track_scale = config.track_default_scale
        self.track_offset = config.track_default_offset
        
        self._fps_counter = 0
        self._fps_sum = 0
        self._fps = 0
        
        self._update_layout()


    def render(self) -> None:
        self.clock.tick()
        self.screen.fill(config.color_background)
        self._render_top_bar()
        self._render_track_screen()
        
        pygame.display.flip()
        
    def handle_user_inputs(self, event) -> None:
        try:
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
        except InvalidTrackError as e:
            self._handle_track_error(e)
            
    def _handle_track_error(self, error: Exception) -> None:            
        print(f"Invalid track, {error}")
            
    def _update_layout(self):
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()
        
        self.top_bar_height = config.ui_top_bar_height
        
        # Surface to render the track on
        track_screen_width = self.screen_width - 2 * config.ui_track_padding
        track_screen_height = self.screen_height - self.top_bar_height - 2 * config.ui_track_padding
        self.track_screen_rect = pygame.Rect(config.ui_track_padding,
                                      self.top_bar_height + config.ui_track_padding,
                                      track_screen_width,
                                      track_screen_height)
        self.track_screen = pygame.Surface((track_screen_width, track_screen_height))
        self.track_overlay.set_screen(self.track_screen)
        
    
    def _render_track_screen(self) -> None:
        # Fill the track screen with the background color
        self.track_screen.fill(config.color_track_background)
        # Render the track
        self.track.render(self.track_screen, self.track_scale, self.track_offset) 
        # Render the track overlay
        self.track_overlay.render()
        # Blit the track screen to the main screen  
        self.screen.blit(self.track_screen, (config.ui_track_padding, self.top_bar_height + config.ui_track_padding))            
        
    def _render_top_bar(self) -> None:
        padding = config.ui_track_padding
        top_bar_surface = pygame.Surface((self.screen_width - 2 * padding, config.ui_top_bar_height))
        text = f"CAuDri-Challenge Track Generator"
        font = pygame.font.Font(font_file_path, config.ui_top_bar_height // 2)
        text_surface = font.render(text, True, (10, 10, 10))
        text_rect = text_surface.get_rect(center=(top_bar_surface.get_width() // 2, top_bar_surface.get_height() // 2))
        top_bar_surface.fill(config.color_background)
        top_bar_surface.blit(text_surface, text_rect)
        top_bar_surface.blit(self._render_fps(), (self.screen_width - padding - 100, 0))
        self.screen.blit(top_bar_surface, (padding, 0))
        
    def _render_fps(self) -> pygame.Surface:
        # Average FPS over the last 50 frames
        self._fps_counter += 1
        self._fps_sum += self.clock.get_fps()
        if self._fps_counter == 50:
            self._fps_counter = 0
            self._fps = self._fps_sum / 50
            self._fps_sum = 0

        font = pygame.font.Font(font_file_path, config.ui_top_bar_height // 5)
        text_surface = font.render(f"FPS: {self._fps:.0f}", True, (200, 200, 200))
        return text_surface
        
    def _screen_to_track_position(self, screen_position) -> tuple:
        return (
            (screen_position[0] - self.track_screen_rect.left),
            (screen_position[1] - self.track_screen_rect.top)
        )
    
    def _move_track(self, dx, dy):
        new_pos_x = self.track_offset[0] + dx
        new_pos_y = self.track_offset[1] + dy
        self.track_offset = [new_pos_x, new_pos_y]

    def _handle_keydown(self, event: pygame.event.Event) -> None:
        if event.key == pygame.K_ESCAPE:
            pygame.quit()
            
    def _handle_mouse_press(self, event) -> None:
        if self.track_screen_rect.collidepoint(event.pos):
            self.track_overlay.handle_mouse_press(event, self._screen_to_track_position(event.pos))
    
    def _handle_mouse_release(self, event: pygame.event.Event) -> None:
        self.track_overlay.handle_mouse_release(event, self._screen_to_track_position(event.pos))
    
    def _handle_mouse_motion(self, event: pygame.event.Event) -> None:
        # Move the track if the middle mouse button is pressed
        if self.track_screen_rect.collidepoint(event.pos):
            if event.buttons[1]:
                dx, dy = event.rel
                self._move_track(dx, dy)
        self.track_overlay.handle_mouse_motion(self._screen_to_track_position(event.pos))

    def _handle_mouse_wheel(self, event: pygame.event.Event) -> None:
        mouse_pos = pygame.mouse.get_pos()
        if self.track_screen_rect.collidepoint(mouse_pos):
            self.track_overlay.handle_mouse_wheel(event)
