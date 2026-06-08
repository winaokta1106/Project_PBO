import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

from patterns.design_patterns import DataConfig, AnalysisEventBus, ConsoleLogger, SummaryCollector, ReportFactory
from repositories.student_repository import StudentRepository
from services.analyzer import ScoreAnalyzer, GenderScoreAnalyzer
from services.visualizer import Visualizer
from exceptions.custom_exceptions import StudentBaseException


def main():
    print("=" * 60)
    print("  ANALISIS PERFORMA SISWA DENGAN OOP")
    print("  Dataset: Students Performance in Exams (Kaggle)")
    print("  Universitas Mulawarman — PBO 2026")
    print("=" * 60)

    base_dir = os.path.dirname(os.path.abspath(__file__))
    config = DataConfig()
    config.set_filepath(os.path.join(base_dir, "data", "StudentsPerformance.csv"))
    print(f"\n📁 Konfigurasi: {config}")

# pattren
    event_bus = AnalysisEventBus()
    logger    = ConsoleLogger()
    collector = SummaryCollector()
    event_bus.subscribe(logger)
    event_bus.subscribe(collector)

# Exception Handling 
    try:  
        print("\n📂 Memuat dataset...")                         # buat membaca CSV dataset nya
        repo     = StudentRepository(config.filepath)
        students = repo.load_from_csv()
        print(f"\n🔍 Contoh objek Student pertama:")            # Magic Methods
        print(f"   __str__ : {students[0]}")
        print(f"   __repr__: {repr(students[0])}")
        print(f"   summary : {students[0].summary()}")
        print(f"\n📌 Total instance Student dibuat: {students[0].get_student_count()}")         # Class method
        analyzer        = ScoreAnalyzer(students)                                           # Polimorfisme (analyzer umum, analyzer per gender)
        analyzer_female = GenderScoreAnalyzer(students, 'female')
        analyzer_male   = GenderScoreAnalyzer(students, 'male')

        print("\n" + "─" * 60)                          # Analisis Utamanya (Sang bintang dari analisis ini)
        summary = analyzer.summary_dict()
        for k, v in summary.items():
            print(f"   {k:<35}: {v}")

        print("\n📊 Dampak Test Preparation Course:")
        for k, v in analyzer.test_prep_impact().items():
            print(f"   {k:<20}: {v}")

        print("\n📊 Rata-rata Nilai per Pendidikan Orang Tua:")
        for edu, avg in analyzer.parental_education_impact().items():
            print(f"   {edu:<40}: {avg}")

        print("\n📊 Statistik Nilai Matematika:")
        for k, v in analyzer.score_stats('math').items():
            print(f"   {k:<10}: {v}")

        print("\n📊 Analisis Per Gender:")  
        print("   PEREMPUAN:", analyzer_female.summary_dict())
        print("   LAKI-LAKI:", analyzer_male.summary_dict())

        event_bus.notify("analisis_selesai", {                  # Observer notify
            "total_siswa": len(students),
            "pass_rate": f"{analyzer.pass_rate():.1f}%",
            "overall_avg": f"{analyzer.overall_average():.2f}",
        })

        print("\n" + "─" * 60)                      # Factory Pattern
        print("📝 Membuat laporan...\n")
        factory     = ReportFactory()
        text_report = factory.create("text")
        print(text_report.generate(summary))

        md_report = factory.create("markdown")
        output_dir = os.path.join(base_dir, "output")
        os.makedirs(output_dir, exist_ok=True)
        with open(os.path.join(output_dir, "laporan.md"), "w", encoding="utf-8") as f:
            f.write(md_report.generate(summary))
        print(f"   📄 Laporan Markdown tersimpan: {os.path.join(output_dir, 'laporan.md')}")

        repo.save_to_json(os.path.join(output_dir, "students_data.json"))

        viz = Visualizer(students, output_dir=output_dir)         # Visualisasi
        viz.generate_all()

        print("\n✅ Selesai! Cek folder output/ untuk hasil.")
        print("=" * 60)

    except StudentBaseException as e:
        print(f"\n❌ Error sistem: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error tak terduga: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
