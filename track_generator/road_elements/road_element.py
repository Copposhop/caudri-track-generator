class RoadElement:
    def __init__(self):
        # Connection points are points on the border of the road element where other road elements can connect to
        self.connection_points = []
        # Guide points are additional points that are used to calculate the shape of the road element
        self.guide_points = []

    def render(self, surface):
        raise NotImplementedError("This method should be overridden by subclasses")

    def update_guide_points(self, index, position, direction):
        raise NotImplementedError("This method should be overridden by subclasses")
    
    def update_connection_points(self, index, position, direction):
        raise NotImplementedError("This method should be overridden by subclasses")