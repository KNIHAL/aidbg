# aidbg/languages/base.py
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Tuple


class LanguageAdapter(ABC):
    @abstractmethod
    def detect_crash(self, output: str) -> bool:
        pass

    @abstractmethod
    def extract_location(self, output: str) -> Tuple[Optional[str], Optional[int]]:

        pass

    @abstractmethod
    def get_snippet(self, file_path: str, line_no: int, context: int = 3) -> str:
        pass

    @abstractmethod
    def classify_error(self, output: str) -> str:
        pass
