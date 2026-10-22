"""Estimadores de efectos causales (copia de 04_analisis_causal y 05_sensibilidad_robustez)."""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def estimar_itt(data: pd.DataFrame, resultado: str, z: str, estrato: str | None = None,
                covariables: list[str] | None = None, alpha: float = 0.05, escala: float = 1.0) -> dict:
    """ITT por MCO con errores HC3. Sin estrato ni covariables equivale a diferencia de medias."""
    terminos = [z] + ([f"C({estrato})"] if estrato else []) + list(covariables or [])
    muestra = data.dropna(subset=[resultado])
    m = smf.ols(f"{resultado} ~ " + " + ".join(terminos), data=muestra).fit(cov_type="HC3")
    ic = m.conf_int(alpha=alpha).loc[z]
    return {"resultado": resultado, "n": int(m.nobs),
            "media_control": escala * muestra.loc[muestra[z] == 0, resultado].mean(),
            "itt": escala * m.params[z], "ee": escala * m.bse[z],
            "ic_inf": escala * ic.iloc[0], "ic_sup": escala * ic.iloc[1], "p_valor": m.pvalues[z]}


def ri_itt(data: pd.DataFrame, resultado: str, z: str, estrato: str, covariables: list[str],
           B: int = 5000, seed: int = 2026) -> tuple[float, np.ndarray, float]:
    """Inferencia por aleatorización del coeficiente ajustado (FWL), permutando z dentro de estratos.
    Devuelve (coeficiente observado, coeficientes simulados, p-valor bilateral)."""
    d = data.dropna(subset=[resultado]).reset_index(drop=True)
    X = pd.get_dummies(d[estrato].astype("category"), drop_first=True, dtype=float)
    X = pd.concat([pd.Series(1.0, index=d.index, name="const"), X, d[covariables].astype(float)], axis=1).to_numpy()
    Q, _ = np.linalg.qr(X)

    def resid(v):
        return v - Q @ (Q.T @ v)

    y_r = resid(d[resultado].to_numpy(float))
    zv = d[z].to_numpy(float)

    def coef(zz):
        r = resid(zz)
        return r @ y_r / (r @ r)

    rng = np.random.default_rng(seed)
    estratos = list(d.groupby(estrato).indices.values())
    obs, sims = coef(zv), np.empty(B)
    for b in range(B):
        zp = zv.copy()
        for idx in estratos:
            zp[idx] = rng.permutation(zv[idx])
        sims[b] = coef(zp)
    p = (1 + np.sum(np.abs(sims) >= abs(obs))) / (B + 1)
    return float(obs), sims, float(p)


def media_cumplidoras(data: pd.DataFrame, variable: str, z: str, d: str) -> float:
    """E[X | cumplidora] = (E[X·D | Z=1] − E[X·D | Z=0]) / (E[D | Z=1] − E[D | Z=0])  (Abadie, 2003)."""
    z1, z0 = data[data[z] == 1], data[data[z] == 0]
    pi = z1[d].mean() - z0[d].mean()
    return float(((z1[variable] * z1[d]).mean() - (z0[variable] * z0[d]).mean()) / pi)


def wald_late(data: pd.DataFrame, resultado: str, z: str, d: str) -> float:
    """Estimador de Wald sin covariables: ITT / primera etapa."""
    dd = data.dropna(subset=[resultado])
    itt = dd.loc[dd[z] == 1, resultado].mean() - dd.loc[dd[z] == 0, resultado].mean()
    pi = dd.loc[dd[z] == 1, d].mean() - dd.loc[dd[z] == 0, d].mean()
    return float(itt / pi)


def lee_bounds(data: pd.DataFrame, y: str, z: str, sel: str) -> tuple[float, float, float]:
    """Cotas de Lee (2009) del efecto de z sobre y con selección sel (1 = observado).
    Devuelve (cota inferior, cota superior, proporción recortada)."""
    q1 = data.loc[data[z] == 1, sel].mean()
    q0 = data.loc[data[z] == 0, sel].mean()
    g_rec = 1 if q1 >= q0 else 0
    p = abs(q1 - q0) / max(q1, q0)
    y_rec = np.sort(data.loc[(data[z] == g_rec) & (data[sel] == 1), y].dropna().to_numpy())
    y_otro = data.loc[(data[z] != g_rec) & (data[sel] == 1), y].dropna().mean()
    k = int(np.ceil(p * len(y_rec)))  # redondeo hacia arriba: conservador
    sin_altos = y_rec[: len(y_rec) - k].mean()
    sin_bajos = y_rec[k:].mean()
    if g_rec == 1:
        return float(sin_altos - y_otro), float(sin_bajos - y_otro), float(p)
    return float(y_otro - sin_bajos), float(y_otro - sin_altos), float(p)


def bootstrap_estratificado(data: pd.DataFrame, celdas: list[str], rng: np.random.Generator) -> pd.DataFrame:
    """Remuestreo con reposición dentro de cada celda (p. ej., centro × Z)."""
    partes = [g.sample(len(g), replace=True, random_state=int(rng.integers(1e9)))
              for _, g in data.groupby(celdas)]
    return pd.concat(partes, ignore_index=True)
