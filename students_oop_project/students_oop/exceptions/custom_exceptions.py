class StudentBaseException(Exception):
    def __init__(self, message: str, code: str = "ERR_000"):
        self.message = message
        self.code = code
        super().__init__(self.message)

    def __str__(self):
        return f"[{self.code}] {self.message}"


class DataNotFoundError(StudentBaseException):
    def __init__(self, message="Data tidak ditemukan"):
        super().__init__(message, code="ERR_001")


class InvalidScoreError(StudentBaseException):
    def __init__(self, score, field="score"):
        message = f"Nilai '{field}' tidak valid: {score}. Harus antara 0–100."
        super().__init__(message, code="ERR_002")


class InvalidDataError(StudentBaseException):
    def __init__(self, message="Data tidak valid"):
        super().__init__(message, code="ERR_003")


class FileLoadError(StudentBaseException):
    def __init__(self, filepath):
        super().__init__(f"Gagal memuat file: {filepath}", code="ERR_004")
