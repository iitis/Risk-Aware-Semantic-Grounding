from point import Point

class BasePlanner(object):
    def plan(self, start: Point, instruction: str):
        raise NotImplementedError("Please implement this method")
