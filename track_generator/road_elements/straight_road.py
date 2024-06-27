import math
import pygame

import track_generator.config as config
from track_generator.config import tile_size
from .road_element import RoadElement
from track_generator.connection_point import ConnectionPoint


class StraightRoad(RoadElement):
    def __init__(self, midpoint=(tile_size / 2, tile_size / 2), direction=(1, 0)):
        super().__init__()
        self.midpoint = midpoint
        self.direction = direction
        self._calc_connection_points_from_midpoint(midpoint, direction)

    def _calc_connection_points_from_midpoint(self, midpoint, direction):
        distance_right = (tile_size - midpoint[0]) / direction[0] if direction[0] != 0 else math.inf
        distance_top = (tile_size - midpoint[1]) / direction[1] if direction[1] != 0 else math.inf
        distance_left = midpoint[0] / -direction[0] if direction[0] != 0 else math.inf
        distance_bottom = midpoint[1] / -direction[1] if direction[1] != 0 else math.inf

        min_distance = min(d for d in (distance_right, distance_top, distance_left, distance_bottom) if d > 0)

        if min_distance == distance_right:
            connection_point_a = ConnectionPoint((tile_size, midpoint[1] + min_distance * direction[1]), direction)
        elif min_distance == distance_top:
            connection_point_a = ConnectionPoint((midpoint[0] + min_distance * direction[0], tile_size), direction)
        elif min_distance == distance_left:
            connection_point_a = ConnectionPoint((0, midpoint[1] - min_distance * direction[1]), direction)
        elif min_distance == distance_bottom:
            connection_point_a = ConnectionPoint((midpoint[0] - min_distance * direction[0], 0), direction)
        else:
            raise ValueError("No valid connection point found")

        if len(self.connection_points) == 0:
            self.connection_points.append(connection_point_a)
        else:
            self.connection_points[0] = connection_point_a

        # Calculate second connection point
        min_distance_opposite = min(d for d in (distance_right, distance_top, distance_left, distance_bottom) if d > 0)

        if min_distance_opposite == distance_right:
            connection_point_b = ConnectionPoint((0, midpoint[1] - min_distance_opposite * direction[1]), (-direction[0], -direction[1]))
        elif min_distance_opposite == distance_top:
            connection_point_b = ConnectionPoint((midpoint[0] - min_distance_opposite * direction[0], 0), (-direction[0], -direction[1]))
        elif min_distance_opposite == distance_left:
            connection_point_b = ConnectionPoint((tile_size, midpoint[1] + min_distance_opposite * direction[1]), (-direction[0], -direction[1]))    
        elif min_distance_opposite == distance_bottom:
            connection_point_b = ConnectionPoint((midpoint[0] + min_distance_opposite * direction[0], tile_size), (-direction[0], -direction[1]))
        else:
            raise ValueError("No valid connection point found")

        if len(self.connection_points) == 1:
            self.connection_points.append(connection_point_b)
        else:
            self.connection_points[1] = connection_point_b

    def render(self, surface):
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, 2 * (config.lane_width + config.line_width))
        pygame.draw.line(surface, config.color_road, self.connection_points[0].position, self.connection_points[1].position, 2 * config.lane_width)
        # Dotted center line
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, config.line_width)
        for cp in self.connection_points:
            pygame.draw.circle(surface, (0,255,0), cp.position, 50, 50)