import track_generator.config as config


class Point:

    def __init__(self, position):
        self._position = self._round_position(position)
        
    # Round position to 1mm precision
    def _round_position(self, position):
        return (round(position[0]), round(position[1]))
        
    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, position):
        self._position = self._round_position(position)


class GuidePoint(Point):

    def __init__(self, position, direction):
        super().__init__(position)
        self._direction = direction
        
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, direction):
        self._direction = direction
        
    def __repr__(self):
        return f"Guide point at tile position {self.position} with direction {self.direction}"
        

class ConnectionPoint(Point):

    def __init__(self, position, direction):
        super().__init__(position)
        self._direction = direction
        self.border = self._get_border(self._position, direction)

    def _get_border(self, position, direction):
        if position[0] == 0 and direction[0] < 0:
            return (-1, 0) # Left
        elif position[0] == config.tile_size and direction[0] > 0:
            return (1, 0) # Right
        elif position[1] == 0 and direction[1] < 0:
            return (0, -1) # Top
        elif position[1] == config.tile_size and direction[1] > 0:
            return (0, 1) # Bottom
        else:
            raise ValueError("Connection point is not on the border of the tile or direction is invalid", position, direction)
        
    @property
    def direction(self):
        return self._direction
    
    @direction.setter
    def direction(self, direction):
        self._direction = direction
        self.border = self._get_border(self.position, direction)
        
    def __repr__(self):
        return f"Connection point at tile position {self.position} with direction {self.direction}"

