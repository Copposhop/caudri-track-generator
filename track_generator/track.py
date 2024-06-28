import track_generator.tile as tile

class Track:
    def __init__(self):
        self.tiles = [] 

    def add_tile(self, new_tile):
        self.tiles.append(new_tile)
        
    def get_tile(self, x, y):
        for tile in self.tiles:
            if tile.x == x and tile.y == y:
                return tile
        return None

    def render(self, screen, scale, offset):
        for tile in self.tiles:
            tile.render(screen, scale, offset)