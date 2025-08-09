from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Sequence


@dataclass(frozen=True)
class Violation:
    """Representa una infracción a una regla de calidad.

    Attributes:
        file_path: Ruta del archivo donde ocurrió la infracción.
        line: Número de línea (1-indexado) donde ocurre la infracción.
        column: Número de columna (1-indexado) si aplica; None si no aplica.
        message: Descripción legible de la infracción.
        rule_name: Nombre de la regla que generó la infracción.
        severity: Severidad de la infracción (LOW, MEDIUM, HIGH).
    """

    file_path: str
    line: int
    column: int | None
    message: str
    rule_name: str
    severity: str = "MEDIUM"


class Rule(ABC):
    """Contrato para una regla de verificación de calidad."""

    @abstractmethod
    def name(self) -> str:
        """Nombre corto de la regla (para reportes)."""

    @abstractmethod
    def check(self, file_path: str, code: str) -> List[Violation]:
        """Evalúa el contenido de un archivo y retorna las infracciones encontradas."""


class Reporter(ABC):
    """Contrato para reportar el resultado de la verificación de calidad."""

    @abstractmethod
    def report(self, violations: Sequence[Violation]) -> None:
        """Emite un reporte a partir de las infracciones encontradas."""


class QualityChecker:
    """Clase base que orquesta la ejecución de reglas y el reporte de resultados."""

    def __init__(self, rules: Sequence[Rule], reporter: Reporter) -> None:
        self._rules: List[Rule] = list(rules)
        self._reporter: Reporter = reporter

    def run(self, targets: Iterable[str | Path]) -> int:
        """Ejecuta todas las reglas sobre los archivos indicados.

        Retorna el número total de infracciones encontradas.
        """
        violations: List[Violation] = []
        for target in targets:
            path = Path(target)
            if path.is_file():
                if path.suffix.lower() == ".py":
                    violations.extend(self._run_on_file(path))
            elif path.is_dir():
                for py_file in path.rglob("*.py"):
                    violations.extend(self._run_on_file(py_file))
        self._reporter.report(violations)
        return len(violations)

    def _run_on_file(self, file_path: Path) -> List[Violation]:
        try:
            code = file_path.read_text(encoding="utf-8", errors="replace")
        except Exception as exc:  # pragma: no cover - robustez de IO
            return [
                Violation(
                    file_path=str(file_path),
                    line=1,
                    column=None,
                    message=f"No se pudo leer el archivo: {exc}",
                    rule_name="IOError",
                    severity="HIGH",
                )
            ]

        file_violations: List[Violation] = []
        for rule in self._rules:
            file_violations.extend(rule.check(str(file_path), code))
        return file_violations 