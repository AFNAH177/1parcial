# Prototipo: Enforzador de Estándares de Calidad (Python)

Este prototipo demuestra una arquitectura simple para reforzar estándares de calidad en código Python, cumpliendo con:

- Clase base: `QualityChecker` (coordina reglas y reporte)
- Dos interfaces: `Rule` y `Reporter` (en `quality/core.py`)
- Implementaciones de interfaces:
  - Reglas: `MaxLineLengthRule`, `NoTodoCommentsRule`
  - Reporteros: `ConsoleReporter`, `JsonFileReporter`
- Buenas prácticas: tipado estático, `dataclass`, docstrings, pruebas unitarias básicas y CLI.

## Uso rápido

Ejecutar desde este directorio (Windows / PowerShell):

```powershell
python -m pip install -r requirements.txt
python -m quality.cli --max-length 100 --reporter console .
```

Para generar un reporte JSON:

```powershell
python -m quality.cli --reporter json --output .\quality_report.json .
```

## Pruebas

```powershell
python -m pytest -q
```

## Estructura

- `quality/core.py`: tipos base (`Violation`) e interfaces (`Rule`, `Reporter`) y clase base `QualityChecker`.
- `quality/rules.py`: reglas concretas.
- `quality/reporters.py`: reporteros concretos.
- `quality/cli.py`: punto de entrada por línea de comandos.
- `tests/`: pruebas unitarias. 