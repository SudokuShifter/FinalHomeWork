import logging

logger = logging.getLogger(__name__)
format_to_logger = '{levelname:<10} - {asctime:<10} - {funcName} - {msg}'
logging.basicConfig(level=logging.INFO, filemode='a', filename='mylog.log', style='{', format=format_to_logger, encoding='UTF-8')
MSG_ERROR = f'Один из прямоугольников не соответствует заданным параметрам для этой операции'


class NegativeValueError(Exception):
    def __init__(self, name, side):
        self.side = side
        self.name = name.replace('_', '', 1)

    def __str__(self):
        if self.name == 'width':
            return f'Ширина должна быть положительной, а не {self.side}'
        return f'Высота должна быть положительной, а не {self.side}'


class CheckSideRectangle:
    def __set_name__(self, owner, name):
        self.param_name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.param_name)

    def __set__(self, instance, value):
        self.validate(value)
        setattr(instance, self.param_name, value)

    def validate(self, value):
        if isinstance(value, int) and value > 0 or isinstance(value, float) and float(value) > 0 or value is None:
            return value
        logger.error(msg=f'Треугольник не прошёл инициализацию: {NegativeValueError(self.param_name, value)}')
        raise NegativeValueError(self.param_name, value)


class Rectangle:
    width = CheckSideRectangle()
    height = CheckSideRectangle()

    def __init__(self, width: int, height=None, name='some_rectangle',):
        self.width = width
        if height is None:
            self.height = width
        else:
            self.height = height
        self.name = name
        logger.info(msg=f'Прямоугольник {self.name} прошёл инициализацию. Ширина: {self.width}, Высота: {self.height}')

    def perimeter(self):
        perimeter = (self.width + self.height) * 2
        logger.info(msg=f'Периметр прямоугольника {self.name} составляет {perimeter}')
        return perimeter

    def area(self):
        area = self.width * self.height
        logger.info(msg=f'Площадь прямоугольника {self.name} составляет {area}')
        return area

    def __add__(self, other):
        if isinstance(other, Rectangle):
            new_attr = Rectangle(self.width + other.width, self.height + other.height)
            logger.info(msg=f'В результате сложения прямоугольников {self.name} и {other.name} '
                            f'получился новый аттрибут класса {Rectangle.__name__} - {new_attr.name} '
                            f'со сторонами {new_attr.width} и {new_attr.height}')
            return new_attr
        logger.error(msg=MSG_ERROR)

    def __sub__(self, other):
        if isinstance(other, Rectangle) and self.perimeter() > other.perimeter():
            new_attr = Rectangle(self.width - other.width, self.height - other.height)
            logger.info(msg=f'В результате вычитания прямоугольников {self.name} и {other.name} '
                            f'получился новый аттрибут класса {Rectangle.__name__} - {new_attr.name} '
                            f'со сторонами {new_attr.width} и {new_attr.height}')
            return new_attr
        logger.error(msg=MSG_ERROR)

    def __lt__(self, other):
        if isinstance(other, Rectangle):
            logger.info(msg=f'Результат сравнения двух прямоугольников: {self.area()} < {other.area()}: {bool(self.area() < other.area())}')
            return self.area() < other.area()
        logger.error(msg=MSG_ERROR)

    def __eq__(self, other):
        if isinstance(other, Rectangle):
            logger.info(msg=f'Результат сравнения двух прямоугольников: {self.area()} == {other.area()}: {bool(self.area() == other.area())}')
            return self.area() == other.area()
        logger.error(msg=MSG_ERROR)

    def __le__(self, other):
        if isinstance(other, Rectangle):
            logger.info(msg=f'Результат сравнения двух прямоугольников: {self.area()} <= {other.area()}: {bool(self.area() <= other.area())}')
            return self.area() <= other.area()
        logger.error(msg=MSG_ERROR)

    def __str__(self):
        return f'Прямоугольник {self.name} со сторонами {self.width} и {self.height}'

    def __repr__(self):
        return f'Rectangle({self.width}, {self.height})'


# a = Rectangle(1, 2)
# b = Rectangle(1, 2)
# a == b
# c = a + b
# w = a - b
# c = Rectangle('v', 3.14)
# d = Rectangle(2, 4)

# a.perimeter()