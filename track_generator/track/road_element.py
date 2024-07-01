class RoadElement:

    def __init__(self):
        self.connection_points = []
        self.guide_points = []

    def render(self, surface):
        raise NotImplementedError("This method should be overridden by subclasses")

    def update_guide_point(self, index, position, direction):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def update_connection_point(self, index, position, direction):
        raise NotImplementedError("This method should be overridden by subclasses")
