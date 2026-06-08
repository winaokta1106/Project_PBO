import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from patterns.design_patterns import DataConfig, AnalysisEventBus, ConsoleLogger, SummaryCollector, ReportFactory
from repositories.student_repository import StudentRepository
from services.analyzer import ScoreAnalyzer, GenderScoreAnalyzer
from services.visualizer import Visualizer
from exceptions.custom_exceptions import StudentBaseException
class Color:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    RED    = "\033[91m"
    WHITE  = "\033[97m"
    GRAY   = "\033[90m"
    PURPLE = "\033[95m"

def header(text):
    w = 62
    print(f"\n{Color.BLUE}{'═'*w}{Color.RESET}")
    print(f"{Color.BLUE}  {Color.BOLD}{Color.WHITE}{text}{Color.RESET}")
    print(f"{Color.BLUE}{'═'*w}{Color.RESET}")

def section(text):
    pad = max(0, 52 - len(text))
    print(f"\n{Color.CYAN}{Color.BOLD}┌─ {text} {'─'*pad}┐{Color.RESET}")

def row(label, value, color=Color.WHITE):
    print(f"  {Color.GRAY}│{Color.RESET}  {Color.YELLOW}{label:<38}{Color.RESET}{color}{value}{Color.RESET}")

def success(text):
    print(f"  {Color.GREEN}✔  {text}{Color.RESET}")

def info(text):
    print(f"  {Color.CYAN}ℹ  {text}{Color.RESET}")

def error_msg(text):
    print(f"  {Color.RED}✘  {text}{Color.RESET}")

def divider():
    print(f"  {Color.GRAY}{'─'*58}{Color.RESET}")


def main():
    print(f"\n{Color.BLUE}╔{'═'*60}╗{Color.RESET}")
    print(f"{Color.BLUE}║{Color.RESET}{Color.BOLD}{Color.WHITE}{'  ANALISIS PERFORMA SISWA DENGAN OOP':^60}{Color.RESET}{Color.BLUE}║{Color.RESET}")
    print(f"{Color.BLUE}║{Color.RESET}{Color.GRAY}{'  Dataset : Students Performance in Exams (Kaggle)':^60}{Color.RESET}{Color.BLUE}║{Color.RESET}")
    print(f"{Color.BLUE}║{Color.RESET}{Color.GRAY}{'  Matkul  : PBO 2026 — Universitas Mulawarman':^60}{Color.RESET}{Color.BLUE}║{Color.RESET}")
    print(f"{Color.BLUE}╚{'═'*60}╝{Color.RESET}")

    config = DataConfig()
    config.set_filepath("data/StudentsPerformance.csv")
    section("KONFIGURASI  (Singleton Pattern)")
    info(f"File dataset   : {Color.WHITE}{config.filepath}{Color.RESET}")
    info(f"Threshold lulus: {Color.WHITE}{config.pass_threshold}{Color.RESET}")

    event_bus = AnalysisEventBus()
    event_bus.subscribe(ConsoleLogger())
    event_bus.subscribe(SummaryCollector())

    try:
        section("MEMUAT DATASET")
        repo     = StudentRepository(config.filepath)
        students = repo.load_from_csv()
        success(f"{len(students)} data siswa berhasil dimuat tanpa error")

        section("CONTOH OBJEK STUDENT")
        s0 = students[0]
        info(f"__str__  : {Color.WHITE}{s0}{Color.RESET}")
        info(f"__repr__ : {Color.WHITE}{repr(s0)}{Color.RESET}")
        info(f"summary  : {Color.WHITE}{s0.summary()}{Color.RESET}")
        info(f"Total instance Student dibuat: {Color.WHITE}{s0.get_student_count()}{Color.RESET}")

        analyzer        = ScoreAnalyzer(students)
        analyzer_female = GenderScoreAnalyzer(students, 'female')
        analyzer_male   = GenderScoreAnalyzer(students, 'male')

        section("RINGKASAN ANALISIS KESELURUHAN")
        summary = analyzer.summary_dict()
        row("Total Siswa",           summary['Total Siswa'],           Color.WHITE)
        divider()
        row("Rata-rata Matematika",   summary['Rata-rata Math'],        Color.WHITE)
        row("Rata-rata Membaca",      summary['Rata-rata Reading'],     Color.WHITE)
        row("Rata-rata Menulis",      summary['Rata-rata Writing'],     Color.WHITE)
        row("Rata-rata Keseluruhan",  summary['Rata-rata Keseluruhan'], Color.CYAN)
        divider()
        row("Siswa Lulus",            summary['Siswa Lulus'],           Color.GREEN)
        row("Siswa Tidak Lulus",      summary['Siswa Tidak Lulus'],     Color.RED)
        row("Tingkat Kelulusan",      summary['Tingkat Kelulusan'],     Color.YELLOW)
        divider()
        grade = summary['Distribusi Grade']
        row("Grade A (≥ 90)",  grade['A'],  Color.GREEN)
        row("Grade B (80–89)", grade['B'],  Color.CYAN)
        row("Grade C (70–79)", grade['C'],  Color.YELLOW)
        row("Grade D (60–69)", grade['D'],  Color.YELLOW)
        row("Grade F (< 60)",  grade['F'],  Color.RED)

        section("DAMPAK KURSUS PERSIAPAN UJIAN")
        tp = analyzer.test_prep_impact()
        row("Rata-rata — ikut kursus",      tp['completed'], Color.GREEN)
        row("Rata-rata — tidak ikut kursus", tp['none'],     Color.RED)
        row("Selisih",                       tp['selisih'],  Color.YELLOW)

        section("RATA-RATA NILAI PER PENDIDIKAN ORANG TUA")
        for edu, avg_val in analyzer.parental_education_impact().items():
            row(edu.title(), avg_val, Color.WHITE)

        section("STATISTIK NILAI MATEMATIKA")
        for k, v in analyzer.score_stats('math').items():
            row(k.capitalize(), v, Color.WHITE)

        section("ANALISIS PER GENDER")
        f_data = analyzer_female.summary_dict()
        m_data = analyzer_male.summary_dict()
        print(f"\n  {Color.PURPLE}{Color.BOLD}  {'Metrik':<34} {'Perempuan':>10} {'Laki-laki':>10}{Color.RESET}")
        print(f"  {Color.GRAY}  {'─'*56}{Color.RESET}")
        keys = ['Total Siswa','Rata-rata Math','Rata-rata Reading',
                'Rata-rata Writing','Rata-rata Keseluruhan',
                'Siswa Lulus','Siswa Tidak Lulus','Tingkat Kelulusan']
        for k in keys:
            fv = str(f_data.get(k, ''))
            mv = str(m_data.get(k, ''))
            print(f"  {Color.YELLOW}  {k:<34}{Color.RESET}"
                  f"{Color.GREEN}{fv:>10}{Color.RESET}  "
                  f"{Color.CYAN}{mv:>10}{Color.RESET}")

        section("EVENT NOTIFICATION")
        event_bus.notify("analisis_selesai", {
            "total_siswa" : len(students),
            "pass_rate"   : f"{analyzer.pass_rate():.1f}%",
            "overall_avg" : f"{analyzer.overall_average():.2f}",
        })

        section("MEMBUAT LAPORAN")
        factory     = ReportFactory()
        text_report = factory.create("text")
        print(f"\n{Color.GRAY}{text_report.generate(summary)}{Color.RESET}")

        md_report = factory.create("markdown")
        os.makedirs("output", exist_ok=True)
        with open("output/laporan.md", "w", encoding="utf-8") as f:
            f.write(md_report.generate(summary))
        success("Laporan Markdown tersimpan  →  output/laporan.md")

        repo.save_to_json("output/students_data.json")
        success("Data JSON tersimpan         →  output/students_data.json")

        section("MEMBUAT VISUALISASI")
        viz = Visualizer(students, output_dir="output")
        viz.generate_all()

        print(f"\n{Color.GREEN}╔{'═'*60}╗{Color.RESET}")
        print(f"{Color.GREEN}║{Color.RESET}{Color.BOLD}{Color.WHITE}{'  SEMUA PROSES SELESAI!':^60}{Color.RESET}{Color.GREEN}║{Color.RESET}")
        print(f"{Color.GREEN}║{Color.RESET}{Color.GRAY}{'  Cek folder output/ untuk grafik & laporan':^60}{Color.RESET}{Color.GREEN}║{Color.RESET}")
        print(f"{Color.GREEN}╚{'═'*60}╝{Color.RESET}\n")

    except StudentBaseException as e:
        error_msg(f"Error sistem: {e}")
        sys.exit(1)
    except Exception as e:
        error_msg(f"Error tak terduga: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()