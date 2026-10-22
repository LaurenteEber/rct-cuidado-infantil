import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def experimento():
    """Experimento sintético estratificado (4 estratos × 200), efecto ITT conocido y cumplimiento imperfecto."""
    rng = np.random.default_rng(0)
    filas = []
    for c in range(4):
        n = 200
        z = rng.permutation(np.repeat([0, 1], n // 2))
        x = rng.normal(0, 1, n)
        tipo = rng.choice(["c", "a", "n"], size=n, p=[0.6, 0.2, 0.2])
        d = np.where(tipo == "a", 1, np.where(tipo == "n", 0, z))
        y = 1.0 + 0.5 * c + 0.8 * x + 2.0 * d + rng.normal(0, 1, n)
        filas.append(pd.DataFrame({"centro": c, "z": z, "d": d, "x": x, "y": y}))
    return pd.concat(filas, ignore_index=True)
