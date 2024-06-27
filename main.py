import pygame
import math

TILE_SIZE = 2000  # Tile size in millimeters
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (100, 100, 100)


# ConnectionPoint class representing a point on a tile border where another road element can connect
# Direction is a unit vector pointing outwards from the tile
# Points should always lie on the border of the tile
# The border is represented by a vector pointing outwards from the tile
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

    def adjust_to_connect(self, other_point, this_point_index):
        raise NotImplementedError("This method should be overridden by subclasses")


class StraightRoad(RoadElement):

    def __init__(self, midpoint=(TILE_SIZE / 2, TILE_SIZE / 2), direction=(1, 0)):
        super().__init__()
        self.midpoint = midpoint
        self.direction = direction
        self._calc_connection_points_from_midpoint(midpoint, direction)
        
    # Calculate the connection points for the road element from a given midpoint and direction
    def _calc_connection_points_from_midpoint(self, midpoint, direction):
        distance_right = (TILE_SIZE - midpoint[0]) / direction[0] if direction[0] != 0 else math.inf
        distance_top = -(TILE_SIZE - midpoint[1]) / direction[1] if direction[1] != 0 else math.inf
        distnace_left = midpoint[0] / -direction[0] if direction[0] != 0 else math.inf
        distance_bottom = midpoint[1] / direction[1] if direction[1] != 0 else math.inf
        
        # Determine the closest border considering only positive distances
        min_distance = min(d for d in (distance_right, distance_top, distnace_left, distance_bottom) if d > 0)
        
        if min_distance == distance_right:
            connection_point_a = ConnectionPoint((TILE_SIZE, midpoint[1] + min_distance * direction[1]), direction)
        elif min_distance == distance_top:
            connection_point_a = ConnectionPoint((midpoint[0] + min_distance * direction[0], TILE_SIZE), direction)
        elif min_distance == distnace_left:
            connection_point_a = ConnectionPoint((0, midpoint[1] - min_distance * direction[1]), direction)
        elif min_distance == distance_bottom:
            connection_point_a = ConnectionPoint((midpoint[0] - min_distance * direction[0], 0), direction)
        else:
            raise ValueError("No valid connection point found")     
        
        if len(self.connection_points) == 0:
            self.connection_points.append(connection_point_a)
        else:
            self.connection_points[0] = connection_point_a
        
        # Find the closest border to the midpoint in the direction of the road
        min_distance = min(distance_right, distance_top, distnace_left, distance_bottom)

    def render(self, surface):
        pygame.draw.line(surface, LINE_COLOR, self.connection_points[0].position, self.midpoint, 10)
        
        if self.connection_points[0].border == (1, 0):
            # Draw right border
            pygame.draw.line(surface, (0,200,0), (TILE_SIZE, 0), (TILE_SIZE, TILE_SIZE), 5)
            print("right")
        elif self.connection_points[0].border == (0, 1):
            # Draw top border
            pygame.draw.line(surface, (0,200,0), (0, TILE_SIZE), (TILE_SIZE, TILE_SIZE), 5)
            print("top")
        elif self.connection_points[0].border == (-1, 0):
            # Draw left border
            pygame.draw.line(surface, (0,200,0), (0, 0), (0, TILE_SIZE), 5)
            print("left")
        elif self.connection_points[0].border == (0, -1):
            # Draw bottom border
            pygame.draw.line(surface, (0,200,0), (0, 0), (TILE_SIZE, 0), 5)
            print("bottom")

class Tile:

    def __init__(self, x, y, road_element):
        self.x = x
        self.y = y
        self.road_element = road_element

    def render(self, screen, scale, offset):
        # Create a surface for the tile
        tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
        tile_surface.fill(ROAD_COLOR)  # Fill the tile with the road color
        
        # Render the road element on the tile surface
        self.road_element.render(tile_surface)

        # Scale the tile surface
        tile_size_scaled = int(TILE_SIZE * scale)
        scaled_tile_surface = pygame.transform.scale(tile_surface, (tile_size_scaled, tile_size_scaled))

        # Calculate the position to blit the scaled tile
        scaled_x = self.x * tile_size_scaled + offset[0]
        scaled_y = self.y * tile_size_scaled + offset[1]
        screen.blit(scaled_tile_surface, (scaled_x, scaled_y))


def add_tile(tiles, new_tile):
    # Find a neighboring tile to connect to
    for tile in tiles:
        for i, conn_point in enumerate(tile.road_element.connection_points):
            for j, new_conn_point in enumerate(new_tile.road_element.connection_points):
                # If the connection points are aligned, adjust the new tile to connect
                if math.isclose(conn_point.position[0], new_conn_point.position[0], abs_tol=1e-2) and \
                   math.isclose(conn_point.position[1], new_conn_point.position[1], abs_tol=1e-2):
                    new_tile.road_element.adjust_to_connect(conn_point, j)
                    tiles.append(new_tile)
                    return
    tiles.append(new_tile)  # If no connections found, just add the tile


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('CAuDri-Challenge Track Generator')
    
    # Create initial road elements
    angle = math.radians(90)
    initial_road = StraightRoad((TILE_SIZE / 2, TILE_SIZE / 2), (math.cos(angle), math.sin(angle)))
    next_road = StraightRoad()

    tiles = [
        Tile(0, 0, initial_road),
    ]
    # add_tile(tiles, Tile(1, 0, next_road))
    
    scale = 0.1  # Initial scale factor (e.g., 0.1 pixels per mm)
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

        screen.fill(BACKGROUND_COLOR)  # Fill the screen with a light grey before drawing
        
        for tile in tiles:
            tile.render(screen, scale, offset)
        
        pygame.display.update()
        
    pygame.quit()


if __name__ == "__main__":
    main()
