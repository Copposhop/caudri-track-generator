import pygame
import math

TILE_SIZE = 2000  # Tile size in millimeters
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

ROAD_COLOR = (50, 50, 50)
LINE_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (100, 100, 100)


class RoadElement:
    def __init__(self, midpoint, tilt_angle):
        self.midpoint = midpoint
        self.tilt_angle = tilt_angle

class StraightRoad(RoadElement):
    def __init__(self, midpoint, tilt_angle):
        super().__init__(midpoint, tilt_angle)
        self.start_point = (0, self.midpoint[1] + self.midpoint[0] * math.tan(self.tilt_angle))
        self.end_point = (TILE_SIZE, self.midpoint[1] - (TILE_SIZE - self.midpoint[0]) * math.tan(self.tilt_angle))

class Tile:
    def __init__(self, x, y, road_element):
        self.x = x
        self.y = y
        self.road_element = road_element

    def render(self, screen, scale, offset):
        tile_size_scaled = int(TILE_SIZE * scale)
        surface = pygame.Surface((tile_size_scaled, tile_size_scaled))
        surface.fill(ROAD_COLOR)  # Fill the tile with white before drawing
        
        # Render the road element on the tile
        if isinstance(self.road_element, StraightRoad):
            self._render_straight_road(surface, scale)

        # Calculate the position to blit the scaled tile
        scaled_x = self.x * tile_size_scaled + offset[0]
        scaled_y = self.y * tile_size_scaled + offset[1]
        screen.blit(surface, (scaled_x, scaled_y))

    def _render_straight_road(self, surface, scale):
        road = self.road_element
        scaled_start_point = (road.start_point[0] * scale, road.start_point[1] * scale)
        scaled_end_point = (road.end_point[0] * scale, road.end_point[1] * scale)
        pygame.draw.line(surface, LINE_COLOR, scaled_start_point, scaled_end_point, 10)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('CAuDri-Challenge Track Generator')
    
    tiles = [
        Tile(0, 0, StraightRoad((TILE_SIZE / 2, TILE_SIZE / 2), 0)),
        Tile(1, 0, StraightRoad((TILE_SIZE / 2, TILE_SIZE / 2), math.pi / 4)),
    ]
    
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
