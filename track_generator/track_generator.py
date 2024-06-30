import pygame

import track_generator.config as config
from track_generator.track.track import Track
from track_generator.user_interface.user_interface import UserInterface
from track_generator.track.tile import Tile

class TrackGenerator:
    def __init__(self) -> None:
        self._init_pygame()
        
        self.running = True
        
        self.track = None
        self.user_interface = UserInterface(self.track)
             
    def _init_pygame(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.RESIZABLE)
        pygame.display.set_caption('CAuDri-Challenge Track Generator')
        
    def start(self) -> None:
        if not self.track:
            self.create_new_track()
        while self.running:
            self._update()
        pygame.quit()
        
    def create_new_track(self) -> None:
        self.track = Track()
        self.user_interface = UserInterface(self.track)
        
    def add_road_element(self, road_element, grid_position) -> None:
        tile = Tile(grid_position, road_element)
        self.track.add_tile(tile)
                    
    def _update(self) -> None:
        self._handle_events()
        self.user_interface.render()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self.user_interface.handle_user_inputs(event)
            if event.type == pygame.QUIT:
                self.running = False

    