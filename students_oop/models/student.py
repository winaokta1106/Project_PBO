from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from exceptions.custom_exceptions import InvalidScoreError, InvalidDataError

class BaseEntity(ABC):
    """Abstract base class untuk semua entitas data."""

    @abstractmethod
    def to_dict(self) -> dict:
        """Konversi objek ke dictionary."""
        pass

    @abstractmethod
    def summary(self) -> str:
        """Ringkasan singkat entitas."""
        pass


class GradeMixin:
    """Mixin class untuk logika grade."""

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
    """
    Representasi satu siswa dalam dataset.

    Atribut:
        gender (str)              : Jenis kelamin siswa
        race_ethnicity (str)      : Kelompok ras/etnis
        parental_education (str)  : Tingkat pendidikan orang tua
        lunch (str)               : Jenis makan siang (standard/free-reduced)
        test_prep (str)           : Status kursus persiapan (completed/none)
        math_score (int)          : Nilai matematika (0–100)
        reading_score (int)       : Nilai membaca (0–100)
        writing_score (int)       : Nilai menulis (0–100)
    """

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
    def gender(self) -> str:
        return self.__gender

    @gender.setter
    def gender(self, value: str):
        val = str(value).strip().lower()
        if val not in self.VALID_GENDERS:
            raise InvalidDataError(f"Gender tidak valid: {value}. Harus salah satu dari {self.VALID_GENDERS}")
        self.__gender = val

    @property
    def race_ethnicity(self) -> str:
        return self.__race_ethnicity

    @race_ethnicity.setter
    def race_ethnicity(self, value: str):
        self.__race_ethnicity = str(value).strip()

    @property
    def parental_education(self) -> str:
        return self.__parental_education

    @parental_education.setter
    def parental_education(self, value: str):
        self.__parental_education = str(value).strip()

    @property
    def lunch(self) -> str:
        return self.__lunch

    @lunch.setter
    def lunch(self, value: str):
        val = str(value).strip().lower()
        if val not in self.VALID_LUNCH:
            raise InvalidDataError(f"Lunch tidak valid: {value}. Harus salah satu dari {self.VALID_LUNCH}")
        self.__lunch = val

    @property
    def test_prep(self) -> str:
        return self.__test_prep

    @test_prep.setter
    def test_prep(self, value: str):
        val = str(value).strip().lower()
        if val not in self.VALID_TEST_PREP:
            raise InvalidDataError(f"Test preparation tidak valid: {value}. Harus salah satu dari {self.VALID_TEST_PREP}")
        self.__test_prep = val

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
        """Hitung rata-rata nilai dari tiga mata pelajaran."""
        return (self.__math_score + self.__reading_score + self.__writing_score) / 3

    def is_passed(self) -> bool:
        """Siswa lulus jika rata-rata >= 60."""
        return self.average_score() >= 60

    def total_score(self) -> int:
        """Total skor semua mata pelajaran."""
        return self.__math_score + self.__reading_score + self.__writing_score

    @staticmethod
    def score_category(score: int) -> str:
        """Kategorikan satu nilai (0–100) ke dalam label."""
        if score >= 90: return 'Sangat Tinggi'
        elif score >= 75: return 'Tinggi'
        elif score >= 60: return 'Cukup'
        else: return 'Rendah'

    @classmethod
    def get_student_count(cls) -> int:
        """Kembalikan total siswa yang telah dibuat."""
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
        """Dua siswa dianggap sama jika total skor-nya sama."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.total_score() == other.total_score()

    def __lt__(self, other) -> bool:
        """Perbandingan berdasarkan rata-rata nilai (untuk sorting)."""
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_score() < other.average_score()

    def __le__(self, other) -> bool:
        return self.average_score() <= other.average_score()
