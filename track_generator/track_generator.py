import pygame
import math

import track_generator.config as config
from track_generator.track import Track
from track_generator.user_interface import UserInterface


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
        self.user_interface = UserInterface(self.track)

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption('CAuDri-Challenge Track Generator')
        
    def update(self):
        self._event_handler()
       
        self.screen.fill(config.color_background)
        self.track.render(self.screen, self.scale, self.offset)
        self.user_interface.render(self.screen, self.scale, self.offset)
        
        pygame.display.flip()
        
    def _event_handler(self):
        for event in pygame.event.get():
            self.user_interface.handle_user_inputs(event)
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
                self.scale = self.scale * (1 + event.y * 0.1)
                self.scale = max(config.min_scale_factor, self.scale)
                self.scale = min(config.max_scale_factor, self.scale)
                print(f"Scale: {self.scale}")
