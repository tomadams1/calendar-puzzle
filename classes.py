class Point:
    "A tuple of and x and y co-ordinate."

    def __init__(self, co_ord: tuple[int,int]):

        self.x = co_ord[0]
        self.y = co_ord[1]

    def __repr__(self):
        return f"({self.x},{self.y})"
    
    def __eq__(self,other):
        return (self.x==other.x) and (self.y==other.y)
    
    def __hash__(self):
        return hash((self.x,self.y))


class Block:
    "A frozen set of several points."

    def __init__(self, points: set[Point]):

        self.points = frozenset(points)

    def __repr__(self):

        sorted_points = sorted(self.points, key=lambda p: (p.x,p.y))
        list_of_points = [str(point) for point in sorted_points]

        return f"[{','.join(list_of_points)}]"

    def __eq__(self,other):

        return self.points == other.points
    
    def __hash__(self):

        return hash(self.points)