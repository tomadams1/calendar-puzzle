class Point:

    def __init__(self, co_ord: tuple[int,int]):

        self.x = co_ord[0]
        self.y = co_ord[1]

    def __repr__(self):
        return f"({self.x},{self.y})"