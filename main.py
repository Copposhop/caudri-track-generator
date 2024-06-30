from track_generator import TrackGenerator, Track

def main():
    track = Track()
    
    track.add_tile((0, 0))
    track.add_tile((1, 0))
    track.add_tile((0, 1))
    
    track_gen = TrackGenerator(track)
    track_gen.run()
    
if __name__ == '__main__':
    main()