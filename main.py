from track_generator import TrackGenerator, Track

from track_generator.track.road_elements.straight_road import StraightRoad


def main():
    track = Track()
    straight_road = StraightRoad()
    
    track.add_tile((0, 0), straight_road)
    track.add_tile((1, 0))
    track.add_tile((0, 1))
    
    track_gen = TrackGenerator(track)
    track_gen.run()

    
if __name__ == '__main__':
    main()
