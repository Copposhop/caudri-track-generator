import pygame

import track_generator.config as config
from track_generator.exceptions import InvalidPositionError, InvalidTrackError


class TrackPoint:
    def __init__(self, road_element, position=(0, 0), direction=(0, 0)):
        self._road_element = road_element
        self._position = pygame.Vector2(position)
        self._direction = pygame.Vector2(direction).normalize()

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
        super().__init__(road_element, position, direction)
        
        self.twin = None
        self._was_visited = False
        self._border = self._validate_border(self.position, self.direction)
        self._fixed_to_border = False

    def __repr__(self):
        return f"Connection point at {self.position} with direction {self.direction}"

    @TrackPoint.position.setter
    def position(self, position):
        self.update(position, self.direction)

    @TrackPoint.direction.setter
    def direction(self, direction):
        self.update(self.position, direction)

    def update(self, position, direction):
        self._was_visited = True
        if self.twin:
            mirrored_position = self.get_mirrored_position(position)
            self.twin.handle_update_from_twin(mirrored_position, -direction)
        self._update(position, direction)
        self._was_visited = False

    def set_twin(self, twin):
        self.twin = twin
        self.twin.twin = self
        position = self.twin.get_mirrored_position()
        self._was_visited = True
        self._road_element.update_connection_point(self._get_index(), position, -twin.direction)
        self.fix_to_border()
        self.twin.fix_to_border()
        self._was_visited = False

    def handle_update_from_twin(self, position, direction):
        if self._was_visited:
            return
        self._road_element.update_connection_point(self._get_index(), position, direction)

    def fix_to_border(self):
        self._fixed_to_border = True

    def release_from_border(self):
        self._fixed_to_border = False

    def is_fixed_to_border(self):
        return self._fixed_to_border

    def get_border(self):
        return self._border

    def get_mirrored_position(self, position: pygame.Vector2=None):
        if position is None:
            position = self.position
        if self._border.x != 0:
            return pygame.Vector2(config.tile_size - position.x, position.y)
        elif self._border.y != 0:
            return pygame.Vector2(position.x, config.tile_size - position.y)

    def _get_index(self):
        return self._road_element.connection_points.index(self)

    def _update(self, position, direction):
        position = pygame.Vector2(round(position[0]), round(position[1]))
        direction = pygame.Vector2(direction).normalize()
        border = self._validate_border(position, direction)
        if self.is_fixed_to_border() and border != self._border:
            raise InvalidPositionError(f"Connection point is fixed to border {self.get_border()}, but new border is {border}", position, self)
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
            raise InvalidPositionError("Connection point is not on the border of the tile, or direction is invalid", position, self)
