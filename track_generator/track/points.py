import pygame

import track_generator.config as config
from track_generator.exceptions import InvalidPositionError


class TrackPoint:

    def __init__(self, road_element, position=(0, 0), direction=(0, 0)):
        self._road_element = road_element
        self.position = position
        self.direction = direction
        
    @property
    def position(self) -> pygame.Vector2:
        return self._position
    
    @property
    def direction(self) -> pygame.Vector2:
        return self._direction
    
    @position.setter
    def position(self, position):
        self._position = pygame.Vector2(position)
        
    @direction.setter
    def direction(self, direction):
        self._direction = pygame.Vector2(direction).normalize()
        
    def update(self, position, direction):
        self.position = position
        self.direction = direction

        
class GuidePoint(TrackPoint):

    def __init__(self, road_element, position, direction):
        super().__init__(road_element, position, direction)
        
    def __repr__(self):
        return f"Guide point at tile position {self.position} with direction {self.direction}"

    
class ConnectionPoint(TrackPoint):
    
    def __init__(self, road_element, position, direction):
        
        self.twin = None
        self._is_updated = False
        
        super().__init__(road_element, position, direction)
        self.update(position, direction)
        
    def __repr__(self):
        return f"Connection point at tile position {self.position} with direction {self.direction}"
    
    def position(self, position):
        self.update(position, self.direction)
                
    def direction(self, direction):
        self.update(self.position, direction)
        
    def update(self, position, direction):
        self._update(position, direction)
        self._is_updated = True
        if self.twin:
            self.twin.update_from_twin(position, [-direction[0], -direction[1]])
        self._is_updated = False
            
    def update_from_twin(self, position, direction):
        if self._is_updated:
            return
        self.road_element.update_connection_point(self, position, direction)      
        
    def _update(self, position, direction):
        position = pygame.Vector2(round(position[0]), round(position[1]))
        direction = pygame.Vector2(direction).normalize()
        try:
            border = self._validate_border(position, direction)
        except InvalidPositionError as error:
            raise error
        else:
            self._position = position
            self._direction = direction
            self._border = border
    
    def _validate_border(self, position, direction) -> pygame.Vector2:
        if position.x == 0 and direction.x < 0:
            return pygame.Vector2(-1, 0)  # Left
        elif position.x == config.tile_size and direction.x > 0:
            return pygame.Vector2(1, 0)  # Right
        elif position.y == 0 and direction.y < 0:
            return pygame.Vector2(0, -1)  # Top
        elif position.y == config.tile_size and direction.y > 0:
            return pygame.Vector2(0, 1)  # Bottom
        else:
            raise InvalidPositionError(f"Connection point is not on the border of the tile, or direction is invalid", position, self)
    
