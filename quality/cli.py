from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import List

from .core import QualityChecker
from .reporters import ConsoleReporter, JsonFileReporter
from .rules import MaxLineLengthRule, NoTodoCommentsRule


def _discover_targets(paths: List[str]) -> List[str]:
    targets: List[str] = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix.lower() == ".py":
            targets.append(str(path))
        elif path.is_dir():
            targets.append(str(path))
    return targets


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="quality-enforcer",
        description="Prototipo: verificador de estándares de calidad en Python.",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Archivos o directorios a analizar (recursivo para directorios)",
    )
    parser.add_argument(
        "--max-length",
        type=int,
        default=100,
        help="Largo máximo permitido por línea (por defecto: 100)",
    )
    parser.add_argument(
        "--reporter",
        choices=["console", "json"],
        default="console",
        help="Tipo de reporte a generar",
    )
    parser.add_argument(
        "--output",
        default="quality_report.json",
        help="Ruta del archivo de salida para el reporte JSON",
    )
    return parser


def main(argv: List[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    rules = [
        MaxLineLengthRule(max_length=args.max_length),
        NoTodoCommentsRule(),
    ]

    reporter = ConsoleReporter() if args.reporter == "console" else JsonFileReporter(args.output)

    checker = QualityChecker(rules=rules, reporter=reporter)
    targets = _discover_targets(args.paths)
    total = checker.run(targets)

    # Salir con código 1 si hay infracciones (útil para CI)
    return 1 if total > 0 else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main()) 