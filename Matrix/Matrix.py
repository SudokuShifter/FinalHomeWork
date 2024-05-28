import logging

logger = logging.getLogger(__name__)
format_to_logger = '{levelname:<10} - {asctime:<10} - {funcName} - {msg}'
logging.basicConfig(level=logging.INFO, filemode='a', filename='mylog.log', style='{', format=format_to_logger, encoding='UTF-8')


class Matrix:

    def __init__(self, name: str, rows: int, cols: int):
        self.name = name
        self.rows = rows
        self.cols = cols
        self.data = [[0 for i in range(rows)] for i in range(cols)]
        logger.info(msg=f'Матрица прошла инициализацию: {self.name} '
                        f'атрибут имеет кол-во строк: {self.rows} _ кол-во колонок: {self.cols}')

    def __repr__(self):
        return f'Matrix({self.data})'

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.data])

    def __eq__(self, other):
        for i in range(len(self.data)):
            if len(self.data[i]) != len(other.data[i]):
                logger.info(msg=f'Матрицы не равны друг другу {self.data} и {other.data}')
                return False

            for j in range(len(self.data[i])):
                if self.data[i][j] != other.data[i][j]:
                    logger.info(msg=f'Матрицы не равны друг другу {self.data} и {other.data}')
                    return False

        logger.info(msg=f'Матрицы равны друг другу {self.data} и {other.data}')
        return True

    def __add__(self, other):
        for i, row in enumerate(self.data):
            if len(row) != len(other.data[i]) or len(self.data) != len(other.data):
                logger.error(msg=f'Матрицы нельзя сложить, т.к. они разной длины {self.data} и {other.data}')
                return False

        res = [[self.data[i][j] + other.data[i][j] for j in range(len(self.data[i]))] for i in range(len(self.data))]
        logger.info(msg=f'Результат сложения двух матриц {self.data} и {other.data} является {res}')
        return '\n'.join([' '.join(map(str, row)) for row in res])

    def __mul__(self, other):
        if len(self.data[0]) != len(other.data):
            logger.error(msg=f'Матрицы нельзя умножить, т.к. они разной длины {self.data} и {other.data}')
            return False

        result_data = []
        for i in range(len(self.data)):
            row = []
            for j in range(len(other.data[0])):
                element = sum(self.data[i][k] * other.data[k][j] for k in range(len(self.data[0])))
                row.append(element)
            result_data.append(row)

        logger.info(msg=f'Результат умножения двух матриц {self.data} и {other.data} является {result_data}')
        return '\n'.join([' '.join(map(str, row)) for row in result_data])
