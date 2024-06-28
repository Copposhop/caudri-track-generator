import math
import pygame

import track_generator.config as config
from track_generator.config import tile_size
from .road_element import RoadElement
from track_generator.points import ConnectionPoint
from track_generator.points import GuidePoint

class StraightRoad(RoadElement):

    def __init__(self, guide_position=(tile_size / 2, tile_size / 2), guide_direction=(1, 0)):
        super().__init__()

        self.guide_points.append(GuidePoint(guide_position, guide_direction))
        self.road_direction = guide_direction
        
        self.connection_points = []
        point_a, point_b = self._border_intersection_from_point(guide_position, guide_direction)
        self.connection_points.append(point_a)
        self.connection_points.append(point_b)

    def update_connection_point(self, index, position, direction):
        assert index in (0, 1), "Index must be 0 or 1"
        
        # Find the new connection point on the border of the tile
        unchanged_point = self.connection_points[1 - index]
        direction = self._norm_direction_from_points(unchanged_point.position, position)
        new_point = self._border_intersection_from_point(unchanged_point.position, direction)[0]
        
        # Update new connection point and directions
        direction = self._norm_direction_from_points(unchanged_point.position, new_point.position)
        self.direction = direction

        self.connection_points[index].position = new_point.position
        self.connection_points[index].direction = direction
        self.connection_points[1 - index].direction = (-direction[0], -direction[1])

        # Update midpoint based on new direction
        self.guide_points[0].position = ((self.connection_points[0].position[0] + self.connection_points[1].position[0]) / 2, (self.connection_points[0].position[1] + self.connection_points[1].position[1]) / 2)
        self.guide_points[0].direction = direction
        
    def render(self, surface):
        # Road fully white
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, 2 * (config.lane_width + config.line_width))
        # Repaint innner part with road color
        pygame.draw.line(surface, config.color_road, self.connection_points[0].position, self.connection_points[1].position, 2 * config.lane_width)
        # Draw inner lane
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, config.line_width)

    def _border_intersection_from_point(self, position, direction):
        point_is_within_tile = 0 <= position[0] <= tile_size and 0 <= position[1] <= tile_size
        
        # Distances from point to borders in the direction of the direction vector
        # Borders are ordered right, top, left, bottom
        def _distance_from_point_to_borders(pos, dir):      
            distance_right = (tile_size - pos[0]) / dir[0] if dir[0] != 0 else math.inf
            distance_top = -pos[1] / dir[1] if dir[1] != 0 else math.inf
            distance_left = -pos[0] / dir[0] if dir[0] != 0 else math.inf
            distance_bottom = (tile_size - pos[1]) / dir[1] if dir[1] != 0 else math.inf
            return distance_right, distance_top, distance_left, distance_bottom
            
        distances = _distance_from_point_to_borders(position, direction) 
        
        # Point a is the first intersection point on any of the borders
        distance_a = min(d for d in distances if d > 0)
        if point_is_within_tile:            
            distance_b = min(-d for d in distances if d <= 0)
            index_b = distances.index(-distance_b)
            
            point_a = ConnectionPoint((position[0] + distance_a * direction[0], position[1] + distance_a * direction[1]), direction)
            point_b = ConnectionPoint((position[0] - distance_b * direction[0], position[1] - distance_b * direction[1]), (-direction[0], -direction[1]))
        
        return point_a, point_b 
      
    def _norm_direction_from_points(self, position_a, position_b):
        distance = math.hypot(position_b[0] - position_a[0], position_b[1] - position_a[1])
        direction = ((position_b[0] - position_a[0]) / distance, (position_b[1] - position_a[1]) / distance)
        return direction
            

