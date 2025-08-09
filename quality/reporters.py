from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .core import Reporter, Violation


class ConsoleReporter(Reporter):
    """Reporta infracciones a la consola en un formato legible."""

    def report(self, violations: Sequence[Violation]) -> None:  # pragma: no cover (E/S)
        if not violations:
            print("✅ Sin infracciones. ¡Buen trabajo!")
            return

        print("❌ Infracciones encontradas:")
        for v in violations:
            location = f"{v.file_path}:{v.line}"
            if v.column is not None:
                location += f":{v.column}"
            print(f"- [{v.severity}] {location} - {v.rule_name}: {v.message}")
        print(f"\nTotal: {len(violations)} infracciones")


@dataclass
class JsonFileReporter(Reporter):
    """Escribe las infracciones en formato JSON en un archivo."""

    output_path: str

    def report(self, violations: Sequence[Violation]) -> None:  # pragma: no cover (E/S)
        data = [
            {
                "file_path": v.file_path,
                "line": v.line,
                "column": v.column,
                "message": v.message,
                "rule": v.rule_name,
                "severity": v.severity,
            }
            for v in violations
        ]
        path = Path(self.output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"Reporte JSON escrito en: {path}") 