"""Diagnóstico del diseño experimental (copia de 02_diseno_validez_interna)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats


def prob_division_exacta(n: int) -> float:
    """P(S = floor(n/2) o ceil(n/2)) con S ~ Binomial(n, 0.5)."""
    valores = {int(np.floor(n / 2)), int(np.ceil(n / 2))}
    return float(sum(stats.binom.pmf(k, n, 0.5) for k in valores))


def tabla_balance(data: pd.DataFrame, variables: list[str], grupo: str, estrato: str | None = None) -> pd.DataFrame:
    """Medias por grupo, SMD, razón de varianzas y p-valor (HC3, con efectos fijos de estrato opcionales)."""
    filas = []
    for v in variables:
        x1, x0 = data.loc[data[grupo] == 1, v], data.loc[data[grupo] == 0, v]
        sd = np.sqrt((x1.var() + x0.var()) / 2)
        formula = f"{v} ~ {grupo}" + (f" + C({estrato})" if estrato else "")
        p = smf.ols(formula, data=data).fit(cov_type="HC3").pvalues[grupo]
        filas.append({"variable": v, "media_sin_oferta": x0.mean(), "media_con_oferta": x1.mean(),
                      "diferencia": x1.mean() - x0.mean(), "smd": (x1.mean() - x0.mean()) / sd,
                      "razon_var": x1.var() / x0.var(), "p_valor": p})
    return pd.DataFrame(filas).set_index("variable")


def permutar_en_estratos(z: np.ndarray, estratos: list[np.ndarray], rng: np.random.Generator) -> np.ndarray:
    """Permuta z dentro de cada estrato (índices posicionales), conservando el número de tratados."""
    z_perm = z.copy()
    for idx in estratos:
        z_perm[idx] = rng.permutation(z[idx])
    return z_perm


def tipos_cumplimiento(data: pd.DataFrame, z: str, d: str) -> pd.Series:
    """Proporciones de siempre usuarias, nunca usuarias y cumplidoras (bajo monotonicidad)."""
    p1 = data.loc[data[z] == 1, d].mean()
    p0 = data.loc[data[z] == 0, d].mean()
    return pd.Series({"siempre_usuarias": p0, "nunca_usuarias": 1 - p1, "cumplidoras": p1 - p0})
