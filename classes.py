class Point:
    "A tuple of and x and y co-ordinate."

    def __init__(self, co_ord: tuple[int,int]):

        self.x = co_ord[0]
        self.y = co_ord[1]

    def __repr__(self):
        return f"({self.x},{self.y})"
    

class Block:
    "A set of several points."

    def __init__(self, points: set[Point]):

        self.points = points

    def __repr__(self):

        list_of_points = [str(point) for point in self.points]

        return f"[{','.join(list_of_points)}]"    