from operator import pos


class TrackGeneratorError(Exception):
    """Base class for exeptions in this module."""


class InvalidTrackError(TrackGeneratorError):

    def __init__(self, message, origin=None):
        self.message = message
        self.origin = origin
        
    def __str__(self):
        return f"Invalid Track Configuration: {self.message} at {self.origin}"

    
class InvalidPositionError(TrackGeneratorError):

    def __init__(self, message, position, origin=None):
        self.message = message
        self.position = position
        self.origin = origin
        
    def __str__(self):
        return f"Invalid Position: {self.message} at {self.position} in {self.origin}"
