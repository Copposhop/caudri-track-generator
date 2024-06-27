class RoadElement:
    def __init__(self):
        self.connection_points = []

    def render(self, surface):
        raise NotImplementedError("This method should be overridden by subclasses")

    def connect_to(self, other):
        raise NotImplementedError("This method should be overridden by subclasses")