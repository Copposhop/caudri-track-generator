import pygame
import pygame.gfxdraw  
import math

import track_generator.config as config

from track_generator.track.road_element import RoadElement
from track_generator.track.points import TrackPoint, GuidePoint, ConnectionPoint
from track_generator.exceptions import InvalidPositionError, InvalidTrackError


class StraightRoad(RoadElement):
    
    def __init__(self, guide_point=None, connection_points=[]):
        super().__init__()
        
        if guide_point:
            self.update_guide_point(guide_point.position, guide_point.direction)
        elif len(connection_points) == 2:
            self.connection_points = connection_points
        else:
            self.update_guide_point((config.tile_size / 2, config.tile_size / 2), (1, 0))
        
    def __repr__(self) -> str:
        return f"Straight Road with guide points {self.guide_points} and connection points {self.connection_points}"
    
    def render(self, surface):
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, 40)

    def update_guide_point(self, position, direction, index=0):
        # Straight road only has one guide point
        if index != 0:
            return

        new_connection_points = self._border_intersection_from_point(GuidePoint(self, position, direction))
        
        if len(self.guide_points) == 0:
            self.guide_points.append(GuidePoint(self, position, direction))
            self.connection_points = new_connection_points
        else:
            self.guide_points[0].update(position, direction)
            self.connection_points[0].update(new_connection_points[0].position, new_connection_points[0].direction)
            self.connection_points[1].update(new_connection_points[1].position, new_connection_points[1].direction) 
        self.road_direction = direction
            
    def update_connection_point(self, position, direction, index):
        self.connection_points[index].update(position, direction)
        
    def _distance_from_point_to_borders(self, point: TrackPoint, border_rect: pygame.Rect):
        distance_right = (border_rect.right - point.position.x) / point.direction.x if point.direction.x != 0 else math.inf
        distance_top = (border_rect.top - point.position.y) / point.direction.y if point.direction.y != 0 else math.inf
        distance_left = (border_rect.left - point.position.x) / point.direction.x if point.direction.x != 0 else math.inf
        distance_bottom = (border_rect.bottom - point.position.y) / point.direction.y if point.direction.y != 0 else math.inf
        return distance_right, distance_top, distance_left, distance_bottom
        
    def _border_intersection_from_point(self, point: TrackPoint):
        position = point.position
        direction = point.direction
        distances = self._distance_from_point_to_borders(point, pygame.Rect(0, 0, config.tile_size, config.tile_size))
        
        # If the point lies within the tile, the first intersection has the smallest positive distance
        if pygame.Rect(0, 0, config.tile_size, config.tile_size).collidepoint(position):
            distance_front = min(d for d in distances if d > 0)
            distance_back = -min(-d for d in distances if d <= 0)
        else:
            distance_back = min(d for d in distances if d > 0)
            distance_front = min(d for d in distances if d >= 0 and d != distance_back)

        try: 
            point_front = ConnectionPoint(None, (position.x + distance_front * direction.x, position.y + distance_front * direction.y), direction)
            point_back = ConnectionPoint(None, (position.x + distance_back * direction.x, position.y + distance_back * direction.y), (-direction.x, -direction.y))
        except InvalidPositionError:
            raise InvalidTrackError("Could not find an intersection with any of the tile borders", point)
        
        return point_front, point_back
    
