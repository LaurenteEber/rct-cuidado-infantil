import pandas as pd
import pyreadstat

from impact_eval.ingestion.stata import read_stata


def test_read_stata(tmp_path):
    # Base sintética
    df_original = pd.DataFrame(
        {
            "id": [1, 2, 3, 4],
            "tratamiento": [1, 0, 1, 0],
            "resultado": [120.5, 90.0, 150.3, 80.2],
        }
    )

    path = tmp_path / "test.dta"

    # Generar archivo Stata
    pyreadstat.write_dta(
        df_original,
        str(path),
        column_labels={
            "id": "Identificador",
            "tratamiento": "Grupo de tratamiento",
            "resultado": "Variable de resultado",
        },
    )

    # Lectura
    df, metadata = read_stata(path)

    assert df.shape == (4, 3)
    assert df["tratamiento"].sum() == 2
    assert metadata.column_names_to_labels["tratamiento"] == "Grupo de tratamiento"

    pd.testing.assert_frame_equal(
        df.reset_index(drop=True),
        df_original,
        check_dtype=False,
    )
