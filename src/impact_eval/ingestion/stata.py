from pathlib import Path

import pandas as pd
import pyreadstat


def read_stata(
    filepath: str | Path,
    columns: list[str] | None = None,
    preserve_missing: bool = False,
) -> tuple[pd.DataFrame, object]:
    """
    Lee un archivo Stata y devuelve:
    - DataFrame con los datos
    - Objeto con los metadatos originales
    """
    path = Path(filepath)

    if not path.is_file():
        raise FileNotFoundError(f"No se encontró el archivo: {path}")

    if path.suffix.lower() != ".dta":
        raise ValueError("se requiere un archivo .dta")

    df, metadata = pyreadstat.read_dta(
        str(path),
        usecols=columns,
        apply_value_formats=False,
        user_missing=preserve_missing,
    )

    return df, metadata


def describe_stata(filepath: str | Path) -> None:
    """Muestra la estructura de un archivo Stata."""

    path = Path(filepath)

    if not path.is_file():
        raise FileNotFoundError(path)

    _, metadata = pyreadstat.read_dta(
        str(path),
        metadataonly=True,
    )

    print(f"Archivo: {path.name}")
    print(f"Observasiones: {metadata.number_rows}")
    print(f"Variables: {metadata.number_columns}")

    print("\nDiccionario de variables:")

    for name, label in metadata.column_names_to_labels.items():
        print(f"{name}: {label or '(sin etiqueta)'}")
