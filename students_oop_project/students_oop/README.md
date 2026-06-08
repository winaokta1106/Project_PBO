# Analisis Performa Siswa dengan OOP
**Dataset:** Students Performance in Exams — Kaggle  
**Mata Kuliah:** Pemrograman Berorientasi Objek (PBO) 2026  
**Universitas Mulawarman — Informatika**


## 🗺️ Pemetaan Materi ke Kode

| Materi | Topik | File |
|--------|-------|------|
| 01 | Pengantar OOP | semua file |
| 02 | Kelas & Objek | `models/student.py` |
| 03 | Atribut & Method | `models/student.py` |
| 04 | Enkapsulasi | `models/student.py` |
| 05 | Hubungan Kelas & UML | `repositories/`, `services/` |
| 06 | Pewarisan | `GradeMixin`, `GenderScoreAnalyzer` |
| 07 | Polimorfisme | `services/analyzer.py` |
| 08 | Abstraksi | `BaseEntity`, `IScoreAnalysis` |
| 09 | Magic Methods | `models/student.py` |
| 10 | Exception Handling | `exceptions/custom_exceptions.py` |
| 11 | Prinsip SOLID | Semua file (SRP, OCP, ISP) |
| 12 | Design Patterns | `patterns/design_patterns.py` |
| 13 | OOP Modern Python | Type Hints di semua file |
| 14 | OOP File & Database | `repositories/student_repository.py` |

## ▶️ Cara Menjalankan

```bash
# 1. Install dependencies
pip install pandas matplotlib seaborn numpy

# 2. Jalankan
python main.py