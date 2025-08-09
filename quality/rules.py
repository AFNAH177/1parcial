from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .core import Rule, Violation


@dataclass
class MaxLineLengthRule(Rule):
    """Regla que verifica el largo máximo de línea."""

    max_length: int = 100

    def name(self) -> str:
        return "MaxLineLength"

    def check(self, file_path: str, code: str) -> List[Violation]:
        violations: List[Violation] = []
        for idx, raw_line in enumerate(code.splitlines(keepends=False), start=1):
            line = raw_line.rstrip("\n")
            if len(line) > self.max_length:
                violations.append(
                    Violation(
                        file_path=file_path,
                        line=idx,
                        column=self.max_length + 1,
                        message=(
                            f"La línea supera el máximo de {self.max_length} caracteres "
                            f"(tiene {len(line)})."
                        ),
                        rule_name=self.name(),
                        severity="MEDIUM",
                    )
                )
        return violations


@dataclass
class NoTodoCommentsRule(Rule):
    """Regla que evita comentarios TODO/FIXME en el código."""

    def name(self) -> str:
        return "NoTodoComments"

    def check(self, file_path: str, code: str) -> List[Violation]:
        violations: List[Violation] = []
        for idx, raw_line in enumerate(code.splitlines(keepends=False), start=1):
            lowered = raw_line.lower()
            if "todo" in lowered or "fixme" in lowered:
                violations.append(
                    Violation(
                        file_path=file_path,
                        line=idx,
                        column=(lowered.find("todo") + 1) if "todo" in lowered else (lowered.find("fixme") + 1),
                        message="Evite TODO/FIXME en el código; registre tareas en el sistema de issues.",
                        rule_name=self.name(),
                        severity="LOW",
                    )
                )
        return violations 