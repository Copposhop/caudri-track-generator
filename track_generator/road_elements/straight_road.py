import math
import pygame

import track_generator.config as config
from track_generator.config import tile_size
from .road_element import RoadElement
from track_generator.connection_point import ConnectionPoint
from operator import pos


class StraightRoad(RoadElement):
    def __init__(self, midpoint=(tile_size / 2, tile_size / 2), direction=(1, 0)):
        super().__init__()

        self.guide_points = [midpoint]
        self.direction = direction
        
        self.connection_points = []
        point_a, point_b = self._border_intersection_from_point(midpoint, direction)
        self.connection_points.append(point_a)
        self.connection_points.append(point_b)

    def _border_intersection_from_point(self, position, direction):
        # Distance to the border of the tile from the midpoint in the direction of the road element
        distance_right = (tile_size - position[0]) / direction[0] if direction[0] != 0 else math.inf
        distance_top = (tile_size - position[1]) / direction[1] if direction[1] != 0 else math.inf
        distance_left = position[0] / -direction[0] if direction[0] != 0 else math.inf
        distance_bottom = position[1] / -direction[1] if direction[1] != 0 else math.inf

        # Point on the border of the tile where the road element connects
        min_distance = min(d for d in (distance_right, distance_top, distance_left, distance_bottom) if d > 0)

        if min_distance == distance_right:
            point_a = ConnectionPoint((tile_size, position[1] + min_distance * direction[1]), direction)
        elif min_distance == distance_top:
            point_a = ConnectionPoint((position[0] + min_distance * direction[0], tile_size), direction)
        elif min_distance == distance_left:
            point_a = ConnectionPoint((0, position[1] - min_distance * direction[1]), direction)
        elif min_distance == distance_bottom:
            point_a = ConnectionPoint((position[0] - min_distance * direction[0], 0), direction)
        else:
            raise ValueError("No valid connection point found")

        # Point on the border of the tile where the road element connects on the opposite side
        min_distance = min(d for d in (distance_right, distance_top, distance_left, distance_bottom) if d > 0)

        if min_distance == distance_right:
            point_b = ConnectionPoint((0, position[1] - min_distance * direction[1]), (-direction[0], -direction[1]))
        elif min_distance == distance_top:
            point_b = ConnectionPoint((position[0] - min_distance * direction[0], 0), (-direction[0], -direction[1]))
        elif min_distance == distance_left:
            point_b = ConnectionPoint((tile_size, position[1] + min_distance * direction[1]), (-direction[0], -direction[1]))    
        elif min_distance == distance_bottom:
            point_b = ConnectionPoint((position[0] + min_distance * direction[0], tile_size), (-direction[0], -direction[1]))
        else:
            raise ValueError("No valid connection point found")
        
        return point_a, point_b 
      
    def _norm_direction_from_points(self, position_a, position_b):
        distance = math.hypot(position_b[0] - position_a[0], position_b[1] - position_a[1])
        direction = ((position_b[0] - position_a[0]) / distance, (position_b[1] - position_a[1]) / distance)
        return direction
            
    def update_connection_points(self, index, position, direction):
        assert index in (0, 1), "Index must be 0 or 1"
        
        # Find the new connection point on the border of the tile
        unchanged_point = self.connection_points[1 - index]
        direction = self._norm_direction_from_points(unchanged_point.position, position)
        new_point = self._border_intersection_from_point(unchanged_point.position, direction)[0]
        
        # Update new connection point and directions
        direction = self._norm_direction_from_points(unchanged_point.position, new_point.position)
        self.direction = direction

        self.connection_points[index].set_position(new_point.position)
        self.connection_points[index].set_direction(direction)
        self.connection_points[1 - index].set_direction((-direction[0], -direction[1]))

        # Update midpoint based on new direction
        self.guide_points[0] = ((self.connection_points[0].position[0] + self.connection_points[1].position[0]) / 2,
                        (self.connection_points[0].position[1] + self.connection_points[1].position[1]) / 2)

        
    def render(self, surface):
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, 2 * (config.lane_width + config.line_width))
        pygame.draw.line(surface, config.color_road, self.connection_points[0].position, self.connection_points[1].position, 2 * config.lane_width)
        # Dotted center line
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, config.line_width)
