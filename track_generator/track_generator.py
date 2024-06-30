import pygame

import track_generator.config as config
from track_generator.track.track import Track
from track_generator.user_interface.user_interface import UserInterface
from track_generator.track.tile import Tile

class TrackGenerator:
    def __init__(self, track: Track = None) -> None:
        self._init_pygame()
        
        self.running = True
        
        if track:
            self.load_track(track)
        else:
            self.create_new_track()
            
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
        
    def load_track(self, track) -> None:
        if not isinstance(track, Track):
            raise ValueError("track must be an instance of Track")
        self.track = track
        
    def add_tile(self, grid_position, road_element=None) -> None:
        self.track.add_tile(grid_position, road_element)
                    
    def _update(self) -> None:
        self._handle_events()
        self.user_interface.render()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            self.user_interface.handle_user_inputs(event)
            if event.type == pygame.QUIT:
                self.running = False

    