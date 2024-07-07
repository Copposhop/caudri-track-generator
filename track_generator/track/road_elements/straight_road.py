import pygame
import pygame.gfxdraw
import math
import numpy

import track_generator.config as config
import track_generator.regulations as regulations

from track_generator.track.road_element import RoadElement
from track_generator.track.points import TrackPoint, GuidePoint, ConnectionPoint
from track_generator.exceptions import InvalidPositionError, InvalidTrackError
from pip._vendor.rich import color


class StraightRoad(RoadElement):
    
    def __init__(self, guide_point=None, connection_points=[]):
        super().__init__()
        
        if guide_point:
            self.update_guide_point(0, guide_point.position, guide_point.direction)
        elif len(connection_points) == 2:
            self.connection_points = connection_points
        else:
            self.update_guide_point(0, (config.tile_size / 2, config.tile_size / 2), (1, 0))
        
    def __repr__(self) -> str:
        return f"Straight Road with guide points {self.guide_points} and connection points {self.connection_points}"
    
    def render(self, surface):
        pos_a = self.connection_points[0].position
        pos_b = self.connection_points[1].position
        color = config.color_lane_marking
        line_width = regulations.lane_marking_line_width
        lane_width = regulations.lane_width
        pygame.draw.line(surface, color, pos_a, pos_b, 2 * (lane_width + line_width))
        pygame.draw.line(surface, config.color_road, pos_a, pos_b, 2 * lane_width)
        # pygame.draw.line(surface, color, pos_a, pos_b, line_width)
        self._draw_line_dashed(surface, color, pos_a, pos_b, line_width, regulations.lane_marking_dash_length)

    def update_guide_point(self, index, position, direction=None):
        if index != 0:
            raise ValueError("Straight road only has one guide point")
        self._update_guide_point(position, direction)
        
    def update_connection_point(self, index, position, direction=None):
        self._update_connection_point(index, position, direction)
        
    def _update_guide_point(self, position, direction):
        if direction is None:
            direction = self.road_direction
        position = self._restrict_position_to_selected_tile(position)
        new_connection_points = self._border_intersection_from_point(GuidePoint(self, position, direction))
        
        if len(self.guide_points) == 0:
            self.guide_points.append(GuidePoint(self, position, direction))
            self.connection_points = new_connection_points
        else:
            self.connection_points[0].update(new_connection_points[0].position, new_connection_points[0].direction)
            self.connection_points[1].update(new_connection_points[1].position, new_connection_points[1].direction)
            self.guide_points[0].update(position, direction) 
        self.road_direction = direction

    def _update_connection_point(self, index, position, direction):
        position = pygame.Vector2(position)
        # Move the guidepoint to the new centerline while keeping the ratio between the connection points
        center_line_length = self.connection_points[0].position.distance_to(self.connection_points[1].position)
        distance_to_guide_point = self.connection_points[0].position.distance_to(self.guide_points[0].position)
        guide_point_ratio = distance_to_guide_point / center_line_length
        guide_point_ratio = max(0.1, min(0.9, guide_point_ratio))
        
        try:
            if direction is None:
                # Fix the position of the opposite connection point 
                unchanged_point = self.connection_points[1 - index]
                # Calculate new position on the border if the point lies outside the tile
                position = self._restrict_position_to_selected_tile(position, unchanged_point)
                # New road direction will be the direction from the unchanged point to the new point
                direction = pygame.Vector2(position - unchanged_point.position).normalize()
                new_point = self._border_intersection_from_point(GuidePoint(self, unchanged_point.position, direction))[1]
                self.connection_points[1 - index].direction = -new_point.direction
                self.connection_points[index].update(new_point.position, new_point.direction)
                
            else:
                direction = pygame.Vector2(direction).normalize()
                position = self._restrict_position_to_selected_tile(position, self.connection_points[1 - index])
                new_point = self._border_intersection_from_point(GuidePoint(self, position, -direction))[1]
                self.connection_points[1 - index].update(new_point.position, new_point.direction)  #
                self.connection_points[index].update(position, direction)
            
            self.road_direction = self.connection_points[1].direction
            guide_point_position = self.connection_points[0].position + guide_point_ratio * (self.connection_points[1].position - self.connection_points[0].position)
            self.guide_points[0].update(guide_point_position, self.road_direction)
        except InvalidPositionError as e:
            raise InvalidTrackError(e, self.guide_points[0])
    
    # Restrict the position of a point to the tile borders
    # A line is drawn from position to the guide point
    # The intersection of the line with the tile borders determines the new position of the point
    def _restrict_position_to_selected_tile(self, position, guide_point=None) -> pygame.Vector2:
        # If the position is inside the tile, return
        position = pygame.Vector2(position)
        if pygame.Rect(0, 0, config.tile_size + 1, config.tile_size + 1).collidepoint(position):
            return position
        if guide_point is None:
            # Point in the center of the tile
            guide_position = pygame.Vector2(config.tile_size / 2, config.tile_size / 2)
        else:
            guide_position = guide_point.position
        direction = (position - guide_position).normalize()
        return self._border_intersection_from_point(GuidePoint(None, guide_position, direction))[1].position      
        
    def _distance_from_point_to_borders(self, point: TrackPoint, border_rect: pygame.Rect):
        # Normalize the direction vector
        direction = point.direction.normalize()
        distance_right = (border_rect.right - point.position.x) / direction.x if direction.x != 0 else math.inf
        distance_top = (border_rect.top - point.position.y) / direction.y if direction.y != 0 else math.inf
        distance_left = (border_rect.left - point.position.x) / direction.x if direction.x != 0 else math.inf
        distance_bottom = (border_rect.bottom - point.position.y) / direction.y if direction.y != 0 else math.inf
        return distance_right, distance_top, distance_left, distance_bottom
        
    def _border_intersection_from_point(self, point: TrackPoint) -> tuple[ConnectionPoint, ConnectionPoint]:
        position = point.position
        direction = point.direction
        distances = self._distance_from_point_to_borders(point, pygame.Rect(0, 0, config.tile_size, config.tile_size))
        
        # If the point lies within the tile, point 1 has the smallest positive distance
        # Guide point 0 lies on the border in the opposite direction
        if pygame.Rect(0, 0, config.tile_size + 1, config.tile_size + 1).collidepoint(position):
            distance_front = min(d for d in distances if d > 0)
            distance_back = -min(-d for d in distances if d <= 0)
        # If the point is at the height or width of the tile, point 0 is the one with the smallest distance
        elif 0 <= point.position.x <= config.tile_size or 0 <= point.position.y <= config.tile_size:
            distance_back = min(d for d in distances if d > 0)
            distance_front = min(d for d in distances if d >= 0 and d != distance_back)
        # Ignore the point with the smallest distance since it is not at the height or width of the tile
        else:
            distances = [d for d in distances if d != min(distances)]
            distance_back = min(d for d in distances if d > 0)
            distance_front = min(d for d in distances if d >= 0 and d != distance_back)
        
        # An InvalidPositionError is raised if there is no intersection with the tile
        try: 
            point_front = ConnectionPoint(self, (position.x + distance_front * direction.x, position.y + distance_front * direction.y), direction)
            point_back = ConnectionPoint(self, (position.x + distance_back * direction.x, position.y + distance_back * direction.y), -direction)
        except InvalidPositionError as e:
            string = f"Could not find an intersection with any of the tile borders:", e
            raise InvalidTrackError(string, point)
        
        return point_back, point_front
    
    def _draw_line_dashed(self, surface, color, start_pos, end_pos, width = 1, dash_length = 10, exclude_corners = True):
        # convert tuples to numpy arrays
        start_pos = numpy.array(start_pos)
        end_pos   = numpy.array(end_pos)

        # get euclidian distance between start_pos and end_pos
        length = numpy.linalg.norm(end_pos - start_pos)

        # get amount of pieces that line will be split up in (half of it are amount of dashes)
        dash_amount = int(length / dash_length)

        # x-y-value-pairs of where dashes start (and on next, will end)
        dash_knots = numpy.array([numpy.linspace(start_pos[i], end_pos[i], dash_amount) for i in range(2)]).transpose()
        
        for n in range(int(exclude_corners), dash_amount - int(exclude_corners) - 1, 2):
            pygame.draw.line(surface, color, tuple(dash_knots[n]), tuple(dash_knots[n+1]), width)

    
