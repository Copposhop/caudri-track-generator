import pygame
import math

TILE_SIZE = 2000  # Tile size in millimeters
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (100, 100, 100)


class ConnectionPoint:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.border = self._get_border(position, direction)

    def _get_border(self, position, direction):
        if position[0] == 0 and direction[0] < 0:
            return (-1, 0)
        elif position[0] == TILE_SIZE and direction[0] > 0:
            return (1, 0)
        elif position[1] == 0 and direction[1] < 0:
            return (0, -1)
        elif position[1] == TILE_SIZE and direction[1] > 0:
            return (0, 1)
        else:
            raise ValueError("Connection point is not on the border of the tile or direction is invalid", position, direction)


class RoadElement:
    def __init__(self):
        self.connection_points = []

    def render(self, surface):
        raise NotImplementedError("This method should be overridden by subclasses")

    def connect_to(self, other):
        raise NotImplementedError("This method should be overridden by subclasses")


class StraightRoad(RoadElement):
    def __init__(self, midpoint=(TILE_SIZE / 2, TILE_SIZE / 2), direction=(1, 0)):
        super().__init__()
        self.midpoint = midpoint
        self.direction = direction
        self._calc_connection_points_from_midpoint(midpoint, direction)

    def _calc_connection_points_from_midpoint(self, midpoint, direction):
        distance_right = (TILE_SIZE - midpoint[0]) / direction[0] if direction[0] != 0 else math.inf
        distance_top = (TILE_SIZE - midpoint[1]) / direction[1] if direction[1] != 0 else math.inf
        distance_left = midpoint[0] / -direction[0] if direction[0] != 0 else math.inf
        distance_bottom = midpoint[1] / -direction[1] if direction[1] != 0 else math.inf

        min_distance = min(d for d in (distance_right, distance_top, distance_left, distance_bottom) if d > 0)

        if min_distance == distance_right:
            connection_point_a = ConnectionPoint((TILE_SIZE, midpoint[1] + min_distance * direction[1]), direction)
        elif min_distance == distance_top:
            connection_point_a = ConnectionPoint((midpoint[0] + min_distance * direction[0], TILE_SIZE), direction)
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

    def render(self, surface):
        pygame.draw.line(surface, LINE_COLOR, self.connection_points[0].position, self.midpoint, 10)
        print(self.connection_points[0].border)


class Tile:
    def __init__(self, x, y, road_element):
        self.x = x
        self.y = y
        self.road_element = road_element

    def __repr__(self):
        return f"Tile at ({self.x}, {self.y}) with road element {self.road_element}"

    def render(self, screen, scale, offset):
        tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile_surface.fill(ROAD_COLOR)
        self.road_element.render(tile_surface)

        tile_size_scaled = int(TILE_SIZE * scale)
        scaled_tile_surface = pygame.transform.scale(tile_surface, (tile_size_scaled, tile_size_scaled))

        scaled_x = self.x * tile_size_scaled + offset[0]
        scaled_y = self.y * tile_size_scaled + offset[1]
        screen.blit(scaled_tile_surface, (scaled_x, scaled_y))


class Track:
    def __init__(self):
        self.tiles = []

    def add_tile(self, new_tile):
        self.tiles.append(new_tile)

    def render(self, screen, scale, offset):
        for tile in self.tiles:
            tile.render(screen, scale, offset)


def main():
    track = Track()

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('CAuDri-Challenge Track Generator')

    angle = 0
    initial_road = StraightRoad(direction=(math.cos(angle), math.sin(angle)))
    track.add_tile(Tile(0, 0, initial_road))

    scale = 0.1
    offset = [0, 0]
    pan_speed = 20

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    offset[1] += pan_speed
                elif event.key == pygame.K_DOWN:
                    offset[1] -= pan_speed
                elif event.key == pygame.K_LEFT:
                    offset[0] += pan_speed
                elif event.key == pygame.K_RIGHT:
                    offset[0] -= pan_speed
            elif event.type == pygame.MOUSEWHEEL:
                scale = max(scale * (1 + event.y * 0.1), 0.05)

        screen.fill(BACKGROUND_COLOR)

        track.render(screen, scale, offset)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
