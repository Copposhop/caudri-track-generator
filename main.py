from track_generator import TrackGenerator, Track

from track_generator.track.road_elements.straight_road import StraightRoad
from track_generator.track.points import GuidePoint


def main():
    track = Track()
    straight_road = StraightRoad(GuidePoint(None, (1200, 900), (1, 0)))
    straight_road_2 = StraightRoad(GuidePoint(None, (1200, 900), (5, 1)))
    straight_road_3 = StraightRoad(GuidePoint(None, (1200, 900), (5, 1)))
    
    track.add_tile((0, 0), straight_road)
    track.add_tile((1, 0), straight_road_2)
    straight_road.connection_points[1].set_twin(straight_road_2.connection_points[0])
    track.add_tile((2, 0), straight_road_3)
    straight_road_2.connection_points[1].set_twin(straight_road_3.connection_points[0])
    
    # straight_road.update_connection_point(0, (0, 800), (-1, 0))
    
    
    track_gen = TrackGenerator(track)
    track_gen.run()
    
if __name__ == '__main__':
    main()
