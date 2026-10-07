"""Compara risk_estimators.py con la copia de AM-PM, función por función.

Informa, no modifica nada. Uso:
    python scripts/check_risk_estimators_sync.py [ruta/a/AM-PM/risk_estimators.py] [--strict]

La ruta también puede darse con la variable AM_PM_RISK_ESTIMATORS. Con --strict el código de salida
es 1 si alguna función presente en ambos archivos difiere (útil para CI).
"""
from __future__ import annotations

import ast
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1] / "risk_estimators.py"
DEFAULT_OTHER = Path.home() / "AM-PM-Architecture" / "risk_estimators.py"


def definitions(path: Path) -> dict[str, str]:
    """Nombre → fuente normalizada (ast.dump ignora comentarios, docstrings no) de cada def/constante."""
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: dict[str, str] = {}
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            out[node.name] = ast.dump(node)
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    out[target.id] = ast.dump(node.value)
    return out


def main(argv: list[str]) -> int:
    strict = "--strict" in argv
    args = [a for a in argv if not a.startswith("--")]
    other = Path(args[0] if args else os.environ.get("AM_PM_RISK_ESTIMATORS", DEFAULT_OTHER))
    if not other.exists():
        print(f"No se encontró {other}. Indique la ruta como argumento o en AM_PM_RISK_ESTIMATORS.")
        return 2
    mine, theirs = definitions(HERE), definitions(other)
    differ = sorted(n for n in mine.keys() & theirs.keys() if mine[n] != theirs[n])
    only_here = sorted(mine.keys() - theirs.keys())
    only_there = sorted(theirs.keys() - mine.keys())
    same = len(mine.keys() & theirs.keys()) - len(differ)
    print(f"Local: {HERE}\nOtro:  {other}\n")
    print(f"Idénticas: {same}")
    print(f"Difieren ({len(differ)}): {', '.join(differ) or '-'}")
    print(f"Solo en este repo ({len(only_here)}): {', '.join(only_here) or '-'}")
    print(f"Solo en la otra copia ({len(only_there)}): {', '.join(only_there) or '-'}")
    return 1 if strict and differ else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
