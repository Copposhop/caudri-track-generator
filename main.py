import pygame
import math

import track_generator.config as config
from track_generator.road_elements.straight_road import StraightRoad
from track_generator.tile import Tile
from track_generator.track import Track

def main():
    track = Track()

    pygame.init()
    screen = pygame.display.set_mode((config.screen_width, config.screen_height), pygame.RESIZABLE)
    pygame.display.set_caption('CAuDri-Challenge Track Generator')

    angle = math.radians(20)
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

        screen.fill(config.color_background)

        track.render(screen, scale, offset)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
