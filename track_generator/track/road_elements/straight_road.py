import pygame
import pygame.gfxdraw  

import track_generator.config as config

from track_generator.track.road_element import RoadElement
from track_generator.track.points import GuidePoint, ConnectionPoint

class StraightRoad(RoadElement):
    
    def __init__(self, guide_point = None, connection_points = []):
        super().__init__()
        
        if guide_point:
            self.update_guide_point
        elif len(connection_points) == 2:
            self.connection_points = connection_points
        else:
            self.update_guide_point((config.tile_size / 2, config.tile_size / 2), (1, 0))
        
        
    def __repr__(self)->str:
        return f"Straight Road with guide points {self.guide_points} and connection points {self.connection_points}"
    
    def render(self, surface):
        pygame.draw.circle(surface, config.color_guide_point, (int(self.guide_points[0].position[0]), int(self.guide_points[0].position[1])), 200, 0)
        pygame.gfxdraw.aacircle(surface, int(self.guide_points[0].position[0]), int(self.guide_points[0].position[1]), 200, config.color_guide_point)


    def update_guide_point(self, position, direction, index=0):
        if index == 0:
            if len(self.guide_points) == 0:
                self.guide_points.append(GuidePoint(self, position, direction))
            self.guide_points[0].position = position
            self.guide_points[0].direction = direction
            
    def update_connection_point(self, position, direction, index):
        self.connection_points[index].position = position
        self.connection_points[index].direction = direction