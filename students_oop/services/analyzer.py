from abc import ABC, abstractmethod
from typing import List, Dict
from collections import Counter

from models.student import Student


# SOLID ISP Interface kecil per tanggung jawab
class IScoreAnalysis(ABC):
    @abstractmethod
    def average_math(self) -> float: pass

    @abstractmethod
    def average_reading(self) -> float: pass

    @abstractmethod
    def average_writing(self) -> float: pass


class IPassRateAnalysis(ABC):
    @abstractmethod
    def pass_rate(self) -> float: pass

    @abstractmethod
    def pass_count(self) -> int: pass

    @abstractmethod
    def fail_count(self) -> int: pass


class IDistributionAnalysis(ABC):
    @abstractmethod
    def grade_distribution(self) -> Dict[str, int]: pass

    @abstractmethod
    def gender_distribution(self) -> Dict[str, int]: pass


# SOLID OCP Bisa diperluas tanpa mengubah kelas ini
class ScoreAnalyzer(IScoreAnalysis, IPassRateAnalysis, IDistributionAnalysis):
    """
    Analyzer utama — mengimplementasikan semua interface analisis.
    Materi 07: Polimorfisme — setiap subclass bisa override metode analisis.
    """

    def __init__(self, students: List[Student]):
        if not students:
            raise ValueError("Daftar siswa tidak boleh kosong.")
        self._students = students

    # IScoreAnalysis
    def average_math(self) -> float:
        return sum(s.math_score for s in self._students) / len(self._students)

    def average_reading(self) -> float:
        return sum(s.reading_score for s in self._students) / len(self._students)

    def average_writing(self) -> float:
        return sum(s.writing_score for s in self._students) / len(self._students)

    def overall_average(self) -> float:
        return sum(s.average_score() for s in self._students) / len(self._students)

    def pass_rate(self) -> float:
        return (self.pass_count() / len(self._students)) * 100

    def pass_count(self) -> int:
        return sum(1 for s in self._students if s.is_passed())

    def fail_count(self) -> int:
        return len(self._students) - self.pass_count()

    # IDistributionAnalysis
    def grade_distribution(self) -> Dict[str, int]:
        grades = [s.get_grade(s.average_score()) for s in self._students]
        result = dict(Counter(grades))
        # Urutan A–F
        return {g: result.get(g, 0) for g in ['A', 'B', 'C', 'D', 'F']}

    def gender_distribution(self) -> Dict[str, int]:
        return dict(Counter(s.gender for s in self._students))

    def test_prep_impact(self) -> Dict[str, float]:
        """Bandingkan rata-rata nilai siswa yang ikut vs tidak ikut test prep."""
        completed = [s for s in self._students if s.test_prep == 'completed']
        none_group = [s for s in self._students if s.test_prep == 'none']

        def avg(lst): return sum(s.average_score() for s in lst) / len(lst) if lst else 0
        return {
            'completed': round(avg(completed), 2),
            'none': round(avg(none_group), 2),
            'selisih': round(avg(completed) - avg(none_group), 2),
        }

    def parental_education_impact(self) -> Dict[str, float]:
        """Rata-rata nilai per tingkat pendidikan orang tua."""
        groups: Dict[str, List] = {}
        for s in self._students:
            edu = s.parental_education
            groups.setdefault(edu, []).append(s.average_score())
        return {edu: round(sum(v)/len(v), 2) for edu, v in sorted(groups.items())}

    def lunch_impact(self) -> Dict[str, float]:
        """Rata-rata nilai berdasarkan jenis makan siang."""
        groups: Dict[str, List] = {}
        for s in self._students:
            groups.setdefault(s.lunch, []).append(s.average_score())
        return {k: round(sum(v)/len(v), 2) for k, v in groups.items()}

    def score_stats(self, subject: str) -> Dict[str, float]:
        """Statistik deskriptif untuk satu mata pelajaran."""
        mapping = {
            'math': [s.math_score for s in self._students],
            'reading': [s.reading_score for s in self._students],
            'writing': [s.writing_score for s in self._students],
        }
        scores = mapping.get(subject.lower())
        if scores is None:
            raise ValueError(f"Subject tidak dikenal: {subject}")
        sorted_scores = sorted(scores)
        n = len(sorted_scores)
        mid = n // 2
        median = (sorted_scores[mid] if n % 2 != 0
                  else (sorted_scores[mid-1] + sorted_scores[mid]) / 2)
        return {
            'min': min(scores), 'max': max(scores),
            'mean': round(sum(scores) / n, 2),
            'median': median,
            'range': max(scores) - min(scores),
        }

    def summary_dict(self) -> dict:
        """Kembalikan ringkasan lengkap sebagai dictionary."""
        return {
            'Total Siswa': len(self._students),
            'Rata-rata Math': f"{self.average_math():.2f}",
            'Rata-rata Reading': f"{self.average_reading():.2f}",
            'Rata-rata Writing': f"{self.average_writing():.2f}",
            'Rata-rata Keseluruhan': f"{self.overall_average():.2f}",
            'Siswa Lulus': self.pass_count(),
            'Siswa Tidak Lulus': self.fail_count(),
            'Tingkat Kelulusan': f"{self.pass_rate():.1f}%",
            'Distribusi Grade': self.grade_distribution(),
        }

class GenderScoreAnalyzer(ScoreAnalyzer):                               # Polimorfisme (subclass dengan perilaku berbeda)
    """
    Subclass ScoreAnalyzer khusus analisis berdasarkan gender.
    Materi 07: method override (polimorfisme).
    """

    def __init__(self, students: List[Student], gender: str):
        filtered = [s for s in students if s.gender == gender.lower()]
        super().__init__(filtered)
        self.gender = gender

    def summary_dict(self) -> dict:
        base = super().summary_dict()
        base['Filter Gender'] = self.gender.capitalize()
        return base
