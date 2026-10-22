# 01 — Ambiente de trabajo (13–14 oct 2026)

## Estado: operativo

- **NetLogo 6.4.0** en `/home/mts/local/netlogo` (tarball oficial, trae Java 17 propio).
  Wrappers `netlogo` / `netlogo-headless` en `~/.local/bin` (debe estar en `PATH`).
  Commit `53c4a42` del modelo declara 6.4.0: no usar el 7.x del AUR.
- **Python**: `Resultados_experimentos/venv/` (creado con `uv`, se auto-ignora en git)
  con `pandas, matplotlib, seaborn, numpy` (+ `scipy` instalado el 15 oct para tests).
  Si falta: `uv venv Resultados_experimentos/venv && uv pip install --python
  Resultados_experimentos/venv/bin/python pandas matplotlib seaborn numpy scipy`.
- **Git**: identidad local `MateoTaito <mtaito@alumnos.uai.cl>`.

## Correcciones aplicadas (commit `f93a937`)

- `AGENTS.md`: path NetLogo (era `/home/MTS/...` con mayúscula, inexistente en Linux)
  + documentación del venv.
- Scripts con paths absolutos rotos `/home/MTS/UAI/...` migrados a
  `Path(__file__).parent`: `plot_interaction_analysis.py`,
  `plot_interaction_analysis_3runs.py`,
  `Comparacion_ABM_vs_TaxEvation/comparison_analysis.py`.
  Verificado: cero ocurrencias de `/home/MTS` en `*.py`.
- `README_interaction_analysis.md`: path `cd` corregido.

## Verificaciones hechas

- `plot_full_inst_mem.py` regenera 6 PNG + 3 CSV correctamente.
- Smoke headless 100 ticks (seed 42): `PIR 0.5215681726813337` — corre y produce CSV válido.
- Ojo: `/tmp` se limpia entre sesiones; los XML de prueba (`smoke*.xml`) hay que recrearlos.

## Experimentos corridos en esta sesión (15–19 oct)

- `Exp_phase_transition/`: barrido tasa 0.02–0.05 × {random, strategic} × PF {1,5},
  N=3+7=10, 50k ticks (48 + 112 runs). Fusión con `merge_N10.py` (`MERGE_N10.txt` con
  md5s y conteos). Modelo congelado durante las tandas (md5 `9f7147e6…` verificado).
- `Exp_trajectories/` (19 oct, corriendo): solo tasa 0.02, {random, strategic} × PF {1,5}
  × 10 reps, 50k ticks, `runMetricsEveryStep=true` con 3 métricas (PIR, PRA, cobertura).
