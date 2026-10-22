import numpy as np
import pandas as pd

from impact_eval.processing.variables import construir_variables, indice_kling


def _base():
    return pd.DataFrame({
        "oferta_sorteo":        [0, 0, 1, 1],
        "uso_horario_ampliado": [0, 1, 1, 0],
        "empleo_pre":  [0, 1, 0, 1], "horas_pre": [0, 30, 0, 40], "ingreso_pre": [0, 900, 0, 1200],
        "empleo_post": [0, 1, 1, 0], "horas_post": [0, 35, 20, 0], "ingreso_post": [np.nan, np.nan, 600, 0],
        "madre_sola": [1, 0, 1, 0], "red_cuidado": [0, 0, 1, 1],
    })


def test_imputacion_logica_solo_en_no_empleadas():
    out = construir_variables(_base())
    assert out.loc[0, "ingreso_post_c"] == 0 and out.loc[0, "ingreso_imput_logica"] == 1
    assert np.isnan(out.loc[1, "ingreso_post_c"]) and out.loc[1, "R_ingreso"] == 0
    assert out["ingreso_imput_logica"].sum() == 1


def test_variables_derivadas():
    out = construir_variables(_base())
    assert out["restriccion_alta"].tolist() == [1, 0, 0, 0]
    assert out["d_horas"].tolist() == [0, 5, 20, -40]
    assert out["celda_cumplimiento"].tolist() == ["No sorteada, no usa", "No sorteada, usa",
                                                   "Sorteada y usa", "Sorteada, no usa"]


def test_no_modifica_original():
    base = _base()
    construir_variables(base)
    assert "ingreso_post_c" not in base.columns


def test_indice_kling_estandarizado_en_control():
    rng = np.random.default_rng(1)
    df = pd.DataFrame({"g": np.repeat([0, 1], 500), "a": rng.normal(5, 2, 1000), "b": rng.normal(-1, 3, 1000)})
    idx = indice_kling(df, ["a", "b"], "g")
    assert abs(idx[df["g"] == 0].mean()) < 1e-10
