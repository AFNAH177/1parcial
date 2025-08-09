# Guía de Contribución

Este repositorio usa el flujo de ramas:

- `main`: estable, versionada, solo se fusiona desde `desarrollo` mediante PR.
- `desarrollo`: integración continua. Acepta PRs de ramas de features/bugs.
- `funcionalidad`: rama de ejemplo para una feature en curso.

## Requisitos
- Python 3.12+ (probado en CI)
- `pytest`

## Setup
```powershell
python -m pip install -r requirements.txt
```

## Pruebas locales
```powershell
python -m pytest -q
```

## Estándares
- Mantener tipado estático y docstrings.
- Commits con prefijos convencionales (`feat:`, `fix:`, `chore:`, `test:`, etc.).
- PRs con descripción breve del cambio y resultados de pruebas.

## Flujo de trabajo
1. Crear rama desde `desarrollo`:
   ```powershell
   git checkout desarrollo
   git pull
   git checkout -b feature/nombre-corto
   ```
2. Commits y pruebas.
3. Abrir PR hacia `desarrollo`.
4. Tras aprobación, se hace PR de `desarrollo` hacia `main` para releases. 