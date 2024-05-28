# Введите ваше решение ниже
import csv
import logging

logger = logging.getLogger(__name__)
format_to_logger = '{levelname:<10} - {asctime:<10} - {funcName} - {msg}'
logging.basicConfig(level=logging.INFO, filemode='a', filename='mylog.log', style='{', format=format_to_logger, encoding='UTF-8')


class NameStudentError(Exception):
    def __init__(self, name, value):
        self.name = value
        self.value = value

    def __str__(self):
        return f'Имя студента должно начинаться с заглавной буквы и состоять из букв: {self.value}'


class SubjectStudentError(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f'Урок {self.name} не найден'


class GradeStudentError(Exception):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f'Оценка за урок {self.name} должна быть целым числом от 2 до 5, а не {self.value}'


class TestStudentError(Exception):

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def __str__(self):
        return f'Результат теста за {self.name} должен быть целым числом от 0 до 100, а не {self.value}'


class Student:

    def __init__(self, name, subjects_file):
        self.name = name
        self.subjects = {}
        self.load_subjects(subjects_file)
        logger.info(msg=f'Атрибут класса {Student.__name__} прошёл инициализацию. '
                        f'Имя студента: {self.name}, Оценки студента: {self.subjects}')

    def __setattr__(self, name, value):
        if name == 'name':
            if not value.replace(' ', '').isalpha() or not value.istitle():
                logger.error(msg=f'{NameStudentError(name, value)}')
                return
        super().__setattr__(name, value)

    def __getattr__(self, name):
        if name in self.subjects:
            return self.subjects[name]
        else:
            logger.error(msg=f'{SubjectStudentError(name)}')
            return

    def __str__(self):
        return f"Студент: {self.name}\nПредметы: {', '.join(self.subjects.keys())}"

    def load_subjects(self, subjects_file):
        with open(subjects_file, 'r', encoding='UTF-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for i in row:
                    subject = i
                    if subject not in self.subjects:
                        self.subjects[subject] = {'grades': [], 'test_scores': []}

    def add_grade(self, subject, grade):
        if subject not in self.subjects:
            logger.error(msg=f'{SubjectStudentError(subject)}')
            return

        if not isinstance(grade, int) or grade < 2 or grade > 5:
            logger.error(msg=f'{GradeStudentError(self.subject, self.grade)}')
            return

        logger.info(msg=f'Оценка {grade} за урок {subject} добавлена для студента {self.name}')
        self.subjects[subject]['grades'].append(grade)

    def add_test_score(self, subject, test_score):
        if subject not in self.subjects:
            logger.error(msg=f'{SubjectStudentError(subject)}')
            return

        if not isinstance(test_score, int) or test_score < 0 or test_score > 100:
            logger.error(msg=f'{TestStudentError(subject, test_score)}')
            return

        logger.info(msg=f'Результат теста {test_score} за {subject} добавлен для студента {self.name}')
        self.subjects[subject]['test_scores'].append(test_score)

    def get_average_test_score(self, subject):
        if subject not in self.subjects:
            logger.error(msg=f'{SubjectStudentError(subject)}')
            return

        test_scores = self.subjects[subject]['test_scores']
        if len(test_scores) == 0:
            logger.info(msg=f'Средний балл {self.name} по тестам равен 0')
            return 0

        avg_test = sum(test_scores) / len(test_scores)
        logger.info(msg=f'Средний балл {self.name} по тестам равен {avg_test}')
        return avg_test

    def get_average_grade(self):
        total_grades = []
        for subject in self.subjects:
            grades = self.subjects[subject]['grades']
            if len(grades) > 0:
                total_grades.extend(grades)
        if len(total_grades) == 0:
            logger.info(msg=f'Средний балл {self.name} по урокам равен 0')
            return 0
        avg_grade = sum(total_grades) / len(total_grades)
        logger.info(msg=f'Средний балл {self.name} по урокам равен {avg_grade}')
        return avg_grade


# a = Student('Валера', 'Student_file.csv')
# b = Student('Дима', 'Student_file.csv')
#
# # a.add_grade('Чтение', 5)
#
# a.add_grade('Математика', 5)
# a.add_grade('Физика', 5)
# a.add_grade('Литература', 3)
# a.get_average_grade()
#
# a.add_test_score('Математика', 28)
# a.add_test_score('Математика', 142)
# a.get_average_test_score('Математика')
