from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
 
class DataConfig:                                   
    _instance: DataConfig = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self.filepath: str = "data/StudentsPerformance.csv"
        self.pass_threshold: float = 60.0
        self.top_n: int = 10
        self._initialized = True

    def set_filepath(self, path: str):
        self.filepath = path

    def __repr__(self):
        return f"DataConfig(filepath='{self.filepath}', threshold={self.pass_threshold})"

class AnalysisObserver(ABC):
    @abstractmethod
    def on_analysis_complete(self, event: str, data: dict):
        pass

class ConsoleLogger(AnalysisObserver):
    def on_analysis_complete(self, event: str, data: dict):
        print(f"[LOG] Event: {event}")
        for key, val in data.items():
            print(f"      {key}: {val}")

class SummaryCollector(AnalysisObserver):
    def __init__(self):
        self.records: List[dict] = []

    def on_analysis_complete(self, event: str, data: dict):
        self.records.append({"event": event, **data})

    def get_all(self) -> List[dict]:
        return self.records

class AnalysisEventBus:
    def __init__(self):
        self._observers: List[AnalysisObserver] = []

    def subscribe(self, observer: AnalysisObserver):
        self._observers.append(observer)

    def unsubscribe(self, observer: AnalysisObserver):
        self._observers.remove(observer)

    def notify(self, event: str, data: dict):
        for obs in self._observers:
            obs.on_analysis_complete(event, data)

class BaseReport(ABC):
    @abstractmethod
    def generate(self, data: dict) -> str:
        pass

class TextReport(BaseReport):
    def generate(self, data: dict) -> str:
        lines = ["=" * 45, "LAPORAN ANALISIS SISWA", "=" * 45]
        for k, v in data.items():
            lines.append(f"  {k:<30}: {v}")
        lines.append("=" * 45)
        return "\n".join(lines)

class MarkdownReport(BaseReport):
    def generate(self, data: dict) -> str:
        lines = ["# Laporan Analisis Performa Siswa", ""]
        lines.append("| Metrik | Nilai |")
        lines.append("|--------|-------|")
        for k, v in data.items():
            lines.append(f"| {k} | {v} |")
        return "\n".join(lines)

class ReportFactory:
    @staticmethod
    def create(report_type: str) -> BaseReport:
        mapping = {
            "text": TextReport,
            "markdown": MarkdownReport,
        }
        cls = mapping.get(report_type.lower())
        if cls is None:
            raise ValueError(f"Report type tidak dikenal: '{report_type}'. "
                             f"Pilihan: {list(mapping.keys())}")
        return cls()
