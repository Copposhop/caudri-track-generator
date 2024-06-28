## Render overlays for the racing track and individual tiles when the user interacts with the track

import pygame

import track_generator.config as config

class UserInterface:
    def __init__(self, track):
        self.track = track
        
        self.selected_tile = None
        self.selected_connection_point = None