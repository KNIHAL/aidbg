# aidbg/languages/base.py

from abc import ABC, abstractmethod
from typing import Optional, Tuple


class LanguageAdapter(ABC):
    @abstractmethod
    def detect_crash(self, output: str) -> bool:
        """Return True if output represents a crash for this language."""
        pass

    @abstractmethod
    def extract_location(self, output: str) -> Tuple[Optional[str], Optional[int]]:
        """Extract file path and line number from error output."""
        pass

    @abstractmethod
    def get_snippet(self, file_path: str, line_no: int, context: int = 3) -> str:
        """Return code snippet around failing line."""
        pass

    @abstractmethod
    def classify_error(self, output: str) -> str:
        """Return 'simple' or 'complex'."""
        pass
