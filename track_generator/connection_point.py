import track_generator.config as config

class ConnectionPoint:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.border = self._get_border(position, direction)

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