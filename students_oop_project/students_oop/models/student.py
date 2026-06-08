from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from exceptions.custom_exceptions import InvalidScoreError, InvalidDataError

class BaseEntity(ABC):
    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def summary(self) -> str:
        pass


class GradeMixin:
    def get_grade(self, average: float) -> str:
        if average >= 90: return 'A'
        elif average >= 80: return 'B'
        elif average >= 70: return 'C'
        elif average >= 60: return 'D'
        else: return 'F'

    def get_predikat(self, average: float) -> str:
        grade = self.get_grade(average)
        mapping = {'A': 'Sangat Baik', 'B': 'Baik', 'C': 'Cukup',
                   'D': 'Kurang', 'F': 'Tidak Lulus'}
        return mapping[grade]

class Student(BaseEntity, GradeMixin):
    VALID_GENDERS = {'male', 'female'}
    VALID_LUNCH = {'standard', 'free/reduced'}
    VALID_TEST_PREP = {'none', 'completed'}
    _student_count: int = 0

    def __init__(self,
                 gender: str,
                 race_ethnicity: str,
                 parental_education: str,
                 lunch: str,
                 test_prep: str,
                 math_score: int,
                 reading_score: int,
                 writing_score: int):

        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_education = parental_education
        self.lunch = lunch
        self.test_prep = test_prep
        self.math_score = math_score
        self.reading_score = reading_score
        self.writing_score = writing_score

        Student._student_count += 1

    @property
    def math_score(self) -> int:
        return self.__math_score

    @math_score.setter
    def math_score(self, value: int):
        if not isinstance(value, (int, float)):
            raise InvalidDataError("math_score harus berupa angka")
        if not (0 <= int(value) <= 100):
            raise InvalidScoreError(value, "math_score")
        self.__math_score = int(value)

    @property
    def reading_score(self) -> int:
        return self.__reading_score

    @reading_score.setter
    def reading_score(self, value: int):
        if not (0 <= int(value) <= 100):
            raise InvalidScoreError(value, "reading_score")
        self.__reading_score = int(value)

    @property
    def writing_score(self) -> int:
        return self.__writing_score

    @writing_score.setter
    def writing_score(self, value: int):
        if not (0 <= int(value) <= 100):
            raise InvalidScoreError(value, "writing_score")
        self.__writing_score = int(value)

    def average_score(self) -> float:
        return (self.__math_score + self.__reading_score + self.__writing_score) / 3

    def is_passed(self) -> bool:
        return self.average_score() >= 60

    def total_score(self) -> int:
        return self.__math_score + self.__reading_score + self.__writing_score

    @staticmethod
    def score_category(score: int) -> str:
        if score >= 90: return 'Sangat Tinggi'
        elif score >= 75: return 'Tinggi'
        elif score >= 60: return 'Cukup'
        else: return 'Rendah'

    @classmethod
    def get_student_count(cls) -> int:
        return cls._student_count

    @classmethod
    def reset_count(cls):
        cls._student_count = 0

    def to_dict(self) -> dict:                      
        return {
            'gender': self.gender,
            'race_ethnicity': self.race_ethnicity,
            'parental_education': self.parental_education,
            'lunch': self.lunch,
            'test_prep': self.test_prep,
            'math_score': self.__math_score,
            'reading_score': self.__reading_score,
            'writing_score': self.__writing_score,
            'average_score': round(self.average_score(), 2),
            'grade': self.get_grade(self.average_score()),
            'status': 'Lulus' if self.is_passed() else 'Tidak Lulus',
        }

    def summary(self) -> str:
        avg = self.average_score()
        return (f"{self.gender.capitalize()} | {self.race_ethnicity} | "
                f"Avg: {avg:.1f} | Grade: {self.get_grade(avg)} "
                f"({self.get_predikat(avg)})")

    def __str__(self) -> str:
        avg = self.average_score()
        return (f"Student(gender={self.gender}, "
                f"avg={avg:.1f}, grade={self.get_grade(avg)}, "
                f"status={'Lulus' if self.is_passed() else 'Tidak Lulus'})")

    def __repr__(self) -> str:
        return (f"Student(gender='{self.gender}', "
                f"math={self.__math_score}, "
                f"reading={self.__reading_score}, "
                f"writing={self.__writing_score})")

    def __eq__(self, other) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.total_score() == other.total_score()

    def __lt__(self, other) -> bool:
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_score() < other.average_score()

    def __le__(self, other) -> bool:
        return self.average_score() <= other.average_score()
