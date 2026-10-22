"""Construcción de variables analíticas del caso 5 (copia de 01_datos_auditoria_construccion).

Los notebooks son autocontenidos; este módulo replica sus funciones para poder probarlas.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def indice_kling(data: pd.DataFrame, componentes: list[str], grupo: str) -> pd.Series:
    """Índice resumen (Kling, Liebman y Katz, 2007): promedio de puntajes z
    estandarizados con media y DE del grupo de control (grupo == 0)."""
    ctrl = data.loc[data[grupo] == 0, componentes]
    z = (data[componentes] - ctrl.mean()) / ctrl.std()
    return z.mean(axis=1, skipna=True)


def construir_variables(df: pd.DataFrame, z: str = "oferta_sorteo", d: str = "uso_horario_ampliado") -> pd.DataFrame:
    """Agrega las variables construidas en 01 sin modificar el DataFrame original."""
    out = df.copy()
    out["ingreso_imput_logica"] = (out["ingreso_post"].isna() & (out["empleo_post"] == 0)).astype(int)
    out["ingreso_post_c"] = np.where(out["empleo_post"] == 0, 0.0, out["ingreso_post"])
    out["R_ingreso"] = out["ingreso_post_c"].notna().astype(int)
    for v in ["empleo", "horas"]:
        out[f"d_{v}"] = out[f"{v}_post"] - out[f"{v}_pre"]
    out["d_ingreso"] = out["ingreso_post_c"] - out["ingreso_pre"]
    out["sin_red"] = 1 - out["red_cuidado"]
    out["restriccion_alta"] = ((out["madre_sola"] == 1) & (out["sin_red"] == 1)).astype(int)
    celda = out[z].astype(int).astype(str) + "-" + out[d].astype(int).astype(str)
    out["celda_cumplimiento"] = celda.map({
        "1-1": "Sorteada y usa", "1-0": "Sorteada, no usa",
        "0-1": "No sorteada, usa", "0-0": "No sorteada, no usa",
    })
    out["indice_laboral"] = indice_kling(out, ["empleo_post", "horas_post", "ingreso_post_c"], z)
    return out
