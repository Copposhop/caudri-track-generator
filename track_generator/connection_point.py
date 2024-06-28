import track_generator.config as config

class ConnectionPoint:
    def __init__(self, position, direction):
        self._position = position
        self._direction = direction
        self.border = self._get_border(position, direction)
        
        self.is_highlighted = False
        self.is_dragging = False

    def _get_border(self, position, direction):
        if position[0] == 0 and direction[0] < 0:
            return (-1, 0)
        elif position[0] == config.tile_size and direction[0] > 0:
            return (1, 0)
        elif position[1] == 0 and direction[1] < 0:
            return (0, -1)
        elif position[1] == config.tile_size and direction[1] > 0:
            return (0, 1)
        else:
            raise ValueError("Connection point is not on the border of the tile or direction is invalid", position, direction)
        
    @property
    def position(self):
        return self._position
    
    @property
    def direction(self):
        return self._direction
        
    def set_position(self, position):
        self._position = position
        self.border = self._get_border(position, self.direction)

    def set_direction(self, direction):
        self._direction = direction
        self.border = self._get_border(self.position, direction)
        