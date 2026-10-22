import numpy as np
import pandas as pd

from impact_eval.estimation.effects import (
    bootstrap_estratificado,
    estimar_itt,
    lee_bounds,
    media_cumplidoras,
    ri_itt,
    wald_late,
)


def test_itt_recupera_efecto(experimento):
    # Verdadero ITT = efecto del uso (2.0) × proporción de cumplidoras (~0.6)
    r = estimar_itt(experimento, "y", "z", estrato="centro", covariables=["x"])
    assert r["ic_inf"] < 1.2 < r["ic_sup"]
    simple = estimar_itt(experimento, "y", "z")
    dm = experimento.groupby("z")["y"].mean().diff().iloc[-1]
    assert np.isclose(simple["itt"], dm)


def test_wald_recupera_late(experimento):
    assert abs(wald_late(experimento, "y", "z", "d") - 2.0) < 0.5


def test_ri_coincide_con_mco_y_rechaza(experimento):
    obs, sims, p = ri_itt(experimento, "y", "z", "centro", ["x"], B=300)
    mco = estimar_itt(experimento, "y", "z", estrato="centro", covariables=["x"])["itt"]
    assert np.isclose(obs, mco)
    assert p < 0.01 and len(sims) == 300


def test_media_cumplidoras_de_constante():
    df = pd.DataFrame({"z": [0, 0, 1, 1, 1, 0], "d": [0, 1, 1, 1, 0, 0], "k": 7.0})
    assert np.isclose(media_cumplidoras(df, "k", "z", "d"), 7.0)


def test_lee_sin_seleccion_diferencial_es_diferencia_de_medias():
    df = pd.DataFrame({"z": [0, 0, 1, 1], "s": [1, 1, 1, 1], "y": [1.0, 3.0, 4.0, 6.0]})
    lo, hi, p = lee_bounds(df, "y", "z", "s")
    assert p == 0 and lo == hi == 3.0


def test_lee_recorta_grupo_con_mas_seleccion():
    # z=1: 4 seleccionadas, z=0: 2 de 4 -> recorta 50 % del grupo tratado
    df = pd.DataFrame({"z": [0, 0, 0, 0, 1, 1, 1, 1], "s": [1, 1, 0, 0, 1, 1, 1, 1],
                       "y": [2.0, 2.0, np.nan, np.nan, 1.0, 2.0, 3.0, 4.0]})
    lo, hi, p = lee_bounds(df, "y", "z", "s")
    assert p == 0.5 and lo == 1.5 - 2.0 and hi == 3.5 - 2.0


def test_bootstrap_estratificado_conserva_celdas(experimento):
    b = bootstrap_estratificado(experimento, ["centro", "z"], np.random.default_rng(0))
    pd.testing.assert_series_equal(b.groupby(["centro", "z"]).size(), experimento.groupby(["centro", "z"]).size())


def test_lee_redondea_recorte_hacia_arriba():
    # p = 1/10 de 9 observaciones = 0.9 obs -> se recorta 1 (conservador)
    df = pd.DataFrame({"z": [1] * 10 + [0] * 10, "s": [1] * 10 + [1] * 9 + [0],
                       "y": list(range(1, 11)) + [5.0] * 9 + [np.nan]})
    lo, hi, p = lee_bounds(df, "y", "z", "s")
    assert np.isclose(p, 0.1)
    assert np.isclose(lo, np.mean(range(1, 10)) - 5.0) and np.isclose(hi, np.mean(range(2, 11)) - 5.0)
