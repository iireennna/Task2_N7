from abc import ABC
from typing import List

class Command(ABC):

    def execute(self):
        pass

    def undo(self):
        pass

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def __str__(self):
        return f"{self.__class__.__name__}(x={self.x}, y={self.y}, color={self.color})"

class Rectangle(Shape):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, color)
        self.width = width
        self.height = height

class Circle(Shape):
    def __init__(self, x, y, radius, color):
        super().__init__(x, y, color)
        self.radius = radius

class Line(Shape):
    def __init__(self, x1, y1, x2, y2, color):
        super().__init__(x1, y1, color)
        self.x2 = x2
        self.y2 = y2


class CreateShapeCommand(Command):
    def __init__(self, shape: Shape):
        self.shape = shape
        global shapes
        self.shapes = shapes

    def execute(self):
        self.shapes.append(self.shape)
        print(f"Создана фигура: {self.shape}")

    def undo(self):
        if self.shapes:
            self.shapes.pop()
            print(f"Откат создания фигуры: {self.shape}")

class MoveShapeCommand(Command):
    def __init__(self, shape: Shape, dx, dy):
        self.shape = shape
        self.dx = dx
        self.dy = dy
        self.old_x = shape.x
        self.old_y = shape.y

    def execute(self):
        self.shape.x += self.dx
        self.shape.y += self.dy
        print(f"Фигура {self.shape} перемещена на ({self.dx}, {self.dy})")

    def undo(self):
        self.shape.x = self.old_x
        self.shape.y = self.old_y
        print(f"Откат перемещения фигуры {self.shape}")

class DeleteShapeCommand(Command):
    def __init__(self, shape: Shape, shapes: List[Shape]):
        self.shape = shape
        self.shapes = shapes
        self.old_shape = None

    def execute(self):
        if self.shape in self.shapes:
            self.old_shape = self.shape
            self.shapes.remove(self.shape)
            print(f"Удалена фигура: {self.shape}")

    def undo(self):
        if self.old_shape:
            self.shapes.append(self.old_shape)
            print(f"Откат удаления фигуры: {self.old_shape}")

class Invoker:
    def __init__(self):
        self.history: List[Command] = []
        self.undo_stack: List[Command] = []

    def execute(self, command: Command):
        command.execute()
        self.history.append(command)
        self.undo_stack.clear()

    def undo(self):
        if self.history:
            command = self.history.pop()
            command.undo()
            self.undo_stack.append(command)

    def redo(self):
        if self.undo_stack:
            command = self.undo_stack.pop()
            command.execute()
            self.history.append(command)


if __name__ == "__main__":
    shapes = []
    invoker = Invoker()



    invoker.execute(CreateShapeCommand(Circle(100, 100, 20, "blue")))
    invoker.execute(CreateShapeCommand(Line(20, 20, 150, 150, "green")))
    invoker.execute(MoveShapeCommand(shapes[0], 20, 30))
    invoker.execute(DeleteShapeCommand(shapes[1], shapes))
    invoker.undo()
    invoker.undo()
    invoker.redo()



"""invoker = Invoker()
shapes = []
invoker.execute(CreateShapeCommand(Rectangle(10, 10, 50, 30, "red")))
invoker.execute(MoveShapeCommand(shapes[0], 20, 30))
invoker.undo()
invoker.redo()"""