from track_generator import TrackGenerator

def main():
    track_generator = TrackGenerator()
    
    track_generator.create_new_track()
    track_generator.add_road_element(None , (0, 0))
    
    track_generator.start()
    
if __name__ == '__main__':
    main()