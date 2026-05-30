import os
from typing import List
from models.student import Student
from services.analyzer import ScoreAnalyzer


class Visualizer:
    """
    Bertanggung jawab HANYA untuk membuat chart & visualisasi.
    Relasi Agregasi: menggunakan Student list dari luar.
    """

    def __init__(self, students: List[Student], output_dir: str = "output"):
        self._students = students
        self._output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def _get_df(self):
        import pandas as pd
        return pd.DataFrame([s.to_dict() for s in self._students])

    def plot_grade_distribution(self):
        import matplotlib.pyplot as plt
        df = self._get_df()
        counts = df['grade'].value_counts().reindex(['A','B','C','D','F'], fill_value=0)
        colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B']
        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(counts.index, counts.values, color=colors, edgecolor='white', linewidth=1.5)
        for bar, val in zip(bars, counts.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
                    str(val), ha='center', va='bottom', fontweight='bold', fontsize=11)
        ax.set_title('Distribusi Grade Siswa', fontsize=14, fontweight='bold', pad=15)
        ax.set_xlabel('Grade', fontsize=12)
        ax.set_ylabel('Jumlah Siswa', fontsize=12)
        ax.set_ylim(0, counts.max() * 1.15)
        ax.grid(axis='y', linestyle='--', alpha=0.5)
        ax.spines[['top','right']].set_visible(False)
        plt.tight_layout()
        path = os.path.join(self._output_dir, 'grade_distribution.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"   📊 Tersimpan: {path}")

    def plot_score_by_gender(self):
        import matplotlib.pyplot as plt
        import numpy as np
        df = self._get_df()
        subjects = ['math_score', 'reading_score', 'writing_score']
        labels = ['Matematika', 'Membaca', 'Menulis']
        male_avgs   = [df[df.gender=='male'][s].mean() for s in subjects]
        female_avgs = [df[df.gender=='female'][s].mean() for s in subjects]
        x = np.arange(len(labels))
        width = 0.35
        fig, ax = plt.subplots(figsize=(9, 5))
        b1 = ax.bar(x - width/2, male_avgs,   width, label='Laki-laki', color='#2E74B5', alpha=0.85)
        b2 = ax.bar(x + width/2, female_avgs, width, label='Perempuan',  color='#E84855', alpha=0.85)
        for bar in list(b1) + list(b2):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                    f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9)
        ax.set_title('Rata-rata Nilai Berdasarkan Gender', fontsize=14, fontweight='bold', pad=15)
        ax.set_xticks(x); ax.set_xticklabels(labels, fontsize=11)
        ax.set_ylabel('Rata-rata Nilai', fontsize=12)
        ax.set_ylim(0, 100)
        ax.legend(fontsize=11)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.spines[['top','right']].set_visible(False)
        plt.tight_layout()
        path = os.path.join(self._output_dir, 'score_by_gender.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"   📊 Tersimpan: {path}")

    def plot_test_prep_effect(self):
        import matplotlib.pyplot as plt
        df = self._get_df()
        groups = df.groupby('test_prep')['average_score'].mean()
        labels = {'completed': 'Ikut Kursus', 'none': 'Tidak Ikut Kursus'}
        colors = ['#27AE60', '#E74C3C']
        display_labels = [labels.get(k, k) for k in groups.index]
        fig, ax = plt.subplots(figsize=(7, 5))
        bars = ax.bar(display_labels, groups.values, color=colors, width=0.45, edgecolor='white')
        for bar, val in zip(bars, groups.values):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                    f'{val:.1f}', ha='center', va='bottom', fontweight='bold', fontsize=12)
        ax.set_title('Pengaruh Kursus Persiapan Terhadap Nilai', fontsize=13, fontweight='bold', pad=15)
        ax.set_ylabel('Rata-rata Nilai', fontsize=12)
        ax.set_ylim(0, 100)
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.spines[['top','right']].set_visible(False)
        plt.tight_layout()
        path = os.path.join(self._output_dir, 'test_prep_effect.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"   📊 Tersimpan: {path}")

    def plot_parental_education(self):
        import matplotlib.pyplot as plt
        df = self._get_df()
        edu_avg = df.groupby('parental_education')['average_score'].mean().sort_values()
        fig, ax = plt.subplots(figsize=(10, 5))
        bars = ax.barh(edu_avg.index, edu_avg.values, color='#2E74B5', alpha=0.8)
        for bar, val in zip(bars, edu_avg.values):
            ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
                    f'{val:.1f}', va='center', fontsize=10)
        ax.set_title('Pengaruh Pendidikan Orang Tua Terhadap Nilai Siswa',
                     fontsize=13, fontweight='bold', pad=15)
        ax.set_xlabel('Rata-rata Nilai', fontsize=12)
        ax.set_xlim(0, 85)
        ax.grid(axis='x', linestyle='--', alpha=0.4)
        ax.spines[['top','right']].set_visible(False)
        plt.tight_layout()
        path = os.path.join(self._output_dir, 'parental_education.png')
        plt.savefig(path, dpi=150, bbox_inches='tight')
        plt.close()
        print(f"   📊 Tersimpan: {path}")

    def generate_all(self):
        print("\n🎨 Membuat visualisasi...")
        self.plot_grade_distribution()
        self.plot_score_by_gender()
        self.plot_test_prep_effect()
        self.plot_parental_education()
        print("✅ Semua chart selesai dibuat!\n")
