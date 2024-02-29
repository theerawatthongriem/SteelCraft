class Rectangle(object):
    def __init__(self, height: float, width: float):
        self.height = height
        self.width = width

    def area()-> float:
        return self.height*self.width

class Draw(Rectangle):
    def draw(self) -> VisualRepresentation:
        return visual_representation(self)