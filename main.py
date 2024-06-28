import pygame
import math

from track_generator.track_generator import TrackGenerator
import track_generator.config as config

from track_generator.road_elements.straight_road import StraightRoad
from track_generator.tile import Tile
from track_generator.track import Track

def main():
    track_generator = TrackGenerator()

    angle = math.radians(20)
    initial_road = StraightRoad(guide_direction=(math.cos(angle), math.sin(angle)))
    track_generator.track.add_tile(Tile(0, 0, initial_road))
    track_generator.track.add_tile(Tile(1, 0, StraightRoad(guide_direction=(1, 0))))

    while track_generator.running:
        track_generator.update()

    pygame.quit()


if __name__ == "__main__":
    main()
