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

    def update_connection_point(self, index, position, direction=None):
        assert index in (0, 1), "Index must be 0 or 1"
        
        # Fix the opposite connection point if no direction is provided
        if direction is None:        
            # Find the new connection point on the border of the tile
            unchanged_point = self.connection_points[1 - index]
            direction = self._norm_direction_from_points(unchanged_point.position, position)
            new_point = self._border_intersection_from_point(unchanged_point.position, direction)[0]
        
            # Update new connection point and directions
            direction = self._norm_direction_from_points(unchanged_point.position, new_point.position)
            self.road_direction = direction

            self.connection_points[index].position = new_point.position
            self.connection_points[index].direction = direction
            self.connection_points[1 - index].direction = (-direction[0], -direction[1])
        
        # Calculate the updated and opposite connection point based on the new direction
        else:
            print("\n", position, direction)
            opposite_point, new_point = self._border_intersection_from_point(position, (-direction[0], -direction[1]))
            
            self.connection_points[index].position = new_point.position
            self.connection_points[index].direction = direction
            self.connection_points[1 - index].position = opposite_point.position
            self.connection_points[1 - index].direction = (-direction[0], -direction[1])
            
            
            # self.connection_points[index].position = position
            # self.connection_points[index].direction = direction
            
            # self.road_direction = direction
            
            # opposite_point = self._border_intersection_from_point(position, direction)[0]
            # self.connection_points[1 - index].position = opposite_point.position
            # self.connection_points[1 - index].direction = (-direction[0], -direction[1])
            

        # Update guide point based on new direction
        guide_x = (self.connection_points[0].position[0] + self.connection_points[1].position[0]) / 2
        guide_y = (self.connection_points[0].position[1] + self.connection_points[1].position[1]) / 2
        self.guide_points[0].position = (guide_x, guide_y)
        self.guide_points[0].direction = direction
        
    def update_guide_point(self, index, position, direction=None):
        assert index == 0, "Index must be 0, there is only one guide point in a straight road."
        
        # Keep the current direction if none is provided
        if direction is None:
            direction = self.guide_points[0].direction
        
        # Guide point distance from border must be < lane_width + line_width
        min_distance = config.lane_width + config.line_width
        
        # If the guide point lies within tile_size - min_distance, update the guide point and connection points
        if min_distance < position[0] < tile_size - min_distance and min_distance < position[1] < tile_size - min_distance: 
            self.guide_points[0].position = position
            self.guide_points[0].direction = direction
            self.road_direction = direction
        
        # If the guide point lies outside of the tile, find a point on the minimum distance border
        else:
            tile_center = (tile_size / 2, tile_size / 2)
            direction_from_center = self._norm_direction_from_points(tile_center, position)
            distances = self._distance_from_point_to_borders(tile_center, direction_from_center, min_distance, tile_size - min_distance)
            distance_to_closest_point = min(d for d in distances if d > 0)
            
            guide_point_x = tile_center[0] + distance_to_closest_point * direction_from_center[0]
            guide_point_y = tile_center[1] + distance_to_closest_point * direction_from_center[1]
            self.guide_points[0].position = (guide_point_x, guide_point_y)
            self.guide_points[0].direction = direction
            self.road_direction = direction
            
        # Update connection points based on new guide point
        point_a, point_b = self._border_intersection_from_point(self.guide_points[0].position, self.guide_points[0].direction)
        self.connection_points[0] = point_a
        self.connection_points[1] = point_b
        
    def render(self, surface):
        # Road fully white
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, 2 * (config.lane_width + config.line_width))
        # Repaint innner part with road color
        pygame.draw.line(surface, config.color_road, self.connection_points[0].position, self.connection_points[1].position, 2 * config.lane_width)
        # Draw inner lane
        pygame.draw.line(surface, config.color_lane_marking, self.connection_points[0].position, self.connection_points[1].position, config.line_width)
        
    def __repr__(self):
        return f"Straight road with guide point at {self.guide_points[0].position} and direction {self.guide_points[0].direction}"
    
    # Distances from point to borders in the direction of the direction vector
    # Borders are ordered right, top, left, bottom
    # Positions of the border corners can be set 
    def _distance_from_point_to_borders(self, position, direction, border_pos_a=0, border_pos_b=tile_size):
        distance_right = (border_pos_b - position[0]) / direction[0] if direction[0] != 0 else math.inf
        distance_top = (border_pos_a - position[1]) / direction[1] if direction[1] != 0 else math.inf
        distance_left = (border_pos_a - position[0]) / direction[0] if direction[0] != 0 else math.inf
        distance_bottom = (border_pos_b - position[1]) / direction[1] if direction[1] != 0 else math.inf
        print(distance_right, distance_top, distance_left, distance_bottom)
        return distance_right, distance_top, distance_left, distance_bottom


    def _border_intersection_from_point(self, position, direction):
        point_is_within_tile = 0 <= position[0] <= tile_size and 0 <= position[1] <= tile_size
            
        distances = self._distance_from_point_to_borders(position, direction) 
        
        # Point A is the first intersection of any of the borders if the point lies within the tile
        # Point B lies on the intersection in the opposite direction
        if point_is_within_tile:         
            distance_a = min(d for d in distances if d > 0)   
            distance_b = -min(-d for d in distances if d <= 0)      

        # Point A is the second intersection of any of the borders if the point lies outside the tile
        # Point B is the first intersection 
        else:
            # direction = (-direction[0], -direction[1])
            def intersects_tile_border(distance):
                pos_x = position[0] + distance * direction[0]
                pos_y = position[1] + distance * direction[1]
                x_is_on_border = math.isclose(pos_x, 0, rel_tol=1e-6) or math.isclose(pos_x, tile_size, rel_tol=1e-6)
                y_is_on_border = math.isclose(pos_y, 0, rel_tol=1e-6) or math.isclose(pos_y, tile_size, rel_tol=1e-6)
                return x_is_on_border and y_is_on_border
            try:
                distance_b = min(d for d in distances if d > 0 and intersects_tile_border(d))
                distance_a = min(d for d in distances if d > 0 and d != distance_b and intersects_tile_border(d))
            except ValueError:
                distance_a = math.inf
                distance_b = math.inf
        
        if distance_a == math.inf or distance_b == math.inf:
            raise ValueError("No intersection with any of the tile borders", position, direction, distance_a, distance_b, distances)
        
        print(position, direction, distance_a, distance_b)
        point_a = ConnectionPoint((position[0] + distance_a * direction[0], position[1] + distance_a * direction[1]), direction)
        point_b = ConnectionPoint((position[0] + distance_b * direction[0], position[1] + distance_b * direction[1]), (-direction[0], -direction[1]))
            
        return point_a, point_b 
      
    def _norm_direction_from_points(self, position_a, position_b):
        distance = math.hypot(position_b[0] - position_a[0], position_b[1] - position_a[1])
        direction = ((position_b[0] - position_a[0]) / distance, (position_b[1] - position_a[1]) / distance)
        return direction
            

