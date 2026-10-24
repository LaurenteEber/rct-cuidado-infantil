# ¿El horario ampliado de cuidado infantil aumenta el empleo de las madres?

**Evaluación experimental (RCT) con 1 500 madres postulantes en 5 centros de cuidado infantil.**

🌐 **Sitio:** https://laurenteeber.github.io/rct-cuidado-infantil/

## Resultados principales

IC 95 % agrupados por centro (wild cluster bootstrap con pesos de Webb y $t(4)$):

| Resultado | Efecto de ofrecer el servicio (ITT) | Efecto de usarlo (LATE) |
|---|---|---|
| Empleo | **+9.7 pp** (IC 95 %: 3.4 a 16.0) | **+15.5 pp** (6.1 a 24.9) |
| Horas semanales | +5.5 (3.0 a 8.0) | +8.8 (5.3 a 12.3) |
| Ingreso mensual (u.m.) | +189 (74 a 303) | +302 (151 a 454) |
| Bienestar (0-100) | +3.4 (2.4 a 4.5) | +5.5 (4.4 a 6.6) |

El efecto es robusto a especificaciones alternativas, a la exclusión de cada centro, a la corrección por multiplicidad, a la inferencia por aleatorización, al agrupamiento por centro y al peor escenario de datos faltantes.

## Qué contiene

| Notebook | Etapa |
|---|---|
| [`00`](notebooks/00_planteamiento_teoria_cambio.ipynb) | Planteamiento, teoría de cambio y DAG |
| [`01`](notebooks/01_datos_auditoria_construccion.ipynb) | Auditoría de datos y construcción de variables |
| [`02`](notebooks/02_diseno_validez_interna.ipynb) | Diseño muestral y validez interna |
| [`03`](notebooks/03_eda.ipynb) | Análisis exploratorio |
| [`04`](notebooks/04_analisis_causal.ipynb) | Análisis causal: ITT, LATE (2SLS), subgrupos |
| [`05`](notebooks/05_sensibilidad_robustez.ipynb) | Sensibilidad y robustez: Lin, IPW, cotas de Lee y Manski |
| [`06`](notebooks/06_inferencia_conglomerados.ipynb) | Revisión: inferencia agrupada por centro (wild cluster bootstrap) |

Además: [decisiones metodológicas](https://laurenteeber.github.io/rct-cuidado-infantil/decisiones.html) (por qué agrupar por centro, por qué 2SLS…), [resumen ejecutivo](https://laurenteeber.github.io/rct-cuidado-infantil/resumen.html) y [English summary](https://laurenteeber.github.io/rct-cuidado-infantil/en/summary.html).

## Reproducir

```bash
uv sync
uv run pytest -v        # pruebas (no requieren datos)
uv run jupyter lab      # notebooks 00 → 06 (requieren la base en data/raw/)
```

Los datos son material del curso y **no se incluyen**. Los notebooks se publican con sus resultados ya ejecutados.

## English

Randomized evaluation of extended childcare hours: offering a slot raised maternal employment by 9.7 percentage points (LATE among compliers: +15.5 pp). See the [English summary](https://laurenteeber.github.io/rct-cuidado-infantil/en/summary.html).

---

Análisis de **Eber Laurente**, como parte del **Grupo 5** del curso de Evaluación de Políticas Públicas del CIES. Código bajo licencia MIT.
