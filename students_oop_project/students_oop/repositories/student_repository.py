import csv
import json
import os
from typing import List, Optional

from models.student import Student
from exceptions.custom_exceptions import DataNotFoundError, FileLoadError, InvalidDataError


class StudentRepository:

    def __init__(self, filepath: str):
        self._filepath: str = filepath
        self._students: List[Student] = []

    def load_from_csv(self) -> List[Student]:
        if not os.path.exists(self._filepath):
            raise FileLoadError(self._filepath)

        Student.reset_count()
        self._students = []
        errors = 0

        try:
            with open(self._filepath, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for i, row in enumerate(reader, start=1):
                    try:
                        student = Student(
                            gender=row['gender'].strip().lower(),
                            race_ethnicity=row['race/ethnicity'].strip(),
                            parental_education=row['parental level of education'].strip(),
                            lunch=row['lunch'].strip().lower(),
                            test_prep=row['test preparation course'].strip().lower(),
                            math_score=int(row['math score']),
                            reading_score=int(row['reading score']),
                            writing_score=int(row['writing score']),
                        )
                        self._students.append(student)
                    except (ValueError, KeyError) as e:
                        errors += 1
        except Exception as e:
            raise FileLoadError(self._filepath) from e

        print(f" {len(self._students)} data berhasil dimuat "
              f"({'0 error' if errors == 0 else f'{errors} baris dilewati'})")
        return self._students

    def save_to_json(self, output_path: str):
        """Ekspor seluruh data ke file JSON (Materi 14 — File I/O)."""
        os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
        data = [s.to_dict() for s in self._students]
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f" Data tersimpan ke {output_path}")

    def get_all(self) -> List[Student]:
        if not self._students:
            raise DataNotFoundError("Belum ada data. Jalankan load_from_csv() terlebih dahulu.")
        return self._students

    def find_by_gender(self, gender: str) -> List[Student]:
        return [s for s in self._students if s.gender == gender.lower()]

    def find_by_test_prep(self, status: str) -> List[Student]:
        return [s for s in self._students if s.test_prep == status.lower()]

    def find_by_grade(self, grade: str) -> List[Student]:
        return [s for s in self._students
                if s.get_grade(s.average_score()) == grade.upper()]

    def find_by_parental_education(self, edu: str) -> List[Student]:
        return [s for s in self._students
                if s.parental_education.lower() == edu.lower()]

    def top_students(self, n: int = 10) -> List[Student]:
        return sorted(self._students, reverse=True)[:n]

    def count(self) -> int:
        return len(self._students)