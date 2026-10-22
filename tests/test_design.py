import numpy as np
from scipy import stats

from impact_eval.estimation.design import (
    permutar_en_estratos,
    prob_division_exacta,
    tabla_balance,
    tipos_cumplimiento,
)


def test_prob_division_exacta_par_e_impar():
    assert np.isclose(prob_division_exacta(10), stats.binom.pmf(5, 10, 0.5))
    assert np.isclose(prob_division_exacta(11), 2 * stats.binom.pmf(5, 11, 0.5))


def test_permutacion_conserva_tratados_por_estrato(experimento):
    rng = np.random.default_rng(3)
    estratos = list(experimento.groupby("centro").indices.values())
    z = experimento["z"].to_numpy()
    zp = permutar_en_estratos(z, estratos, rng)
    for idx in estratos:
        assert zp[idx].sum() == z[idx].sum()
    assert not np.array_equal(z, zp)


def test_balance_en_experimento(experimento):
    b = tabla_balance(experimento, ["x"], "z", "centro")
    assert abs(b.loc["x", "smd"]) < 0.15
    assert b.loc["x", "p_valor"] > 0.01


def test_tipos_cumplimiento_suman_uno(experimento):
    t = tipos_cumplimiento(experimento, "z", "d")
    assert np.isclose(t.sum(), 1)
    assert 0.5 < t["cumplidoras"] < 0.7
