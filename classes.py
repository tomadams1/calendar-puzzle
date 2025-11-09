class Point:
    "A tuple of and x and y co-ordinate."

    def __init__(self, co_ord: tuple[int,int]):

        self.x = co_ord[0]
        self.y = co_ord[1]

    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def __eq__(self,other):
        return (self.x==other.x) and (self.y==other.y)
    

class Block:
    "A set of several points."

    def __init__(self, points: set[Point]):

        self.points = points
        self.centre()

    def __repr__(self):

        sorted_points = sorted(self.points, key=lambda p: (p.x,p.y))
        list_of_points = [str(point) for point in sorted_points]

        return f"[{','.join(list_of_points)}]"

    def centre(self):

        min_x = min([point.x for point in self.points])
        min_y = min([point.y for point in self.points])

        self.points = [Point((point.x-min_x, point.y-min_y)) for point in self.points]

    def __eq__(self,other):

        return self.points = other.points