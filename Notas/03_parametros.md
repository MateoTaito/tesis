# 03 — Parámetros alterables (14 oct 2026)

Fuente: `Docu/Especificación ABM_ Tax-Evation_1_2_con_memoria_institucional.md` §4
+ código. Defaults de la interfaz entre paréntesis.

## Población y fiscalización

- `nr-tax-payers` (500): contribuyentes; densidad regula el n° de vecinos (segundo orden).
- `nr-auditors` (20): no intercambiable con la tasa; reparte carga + fatiga intra-tick (−0.05 por período).
- `actual-audit-rate` (0.20): cobertura horizontal por tick.

## Impuestos y sanciones

- `tax-rate` (0.27), `penalty-rate` (1.5): **no entran en ninguna regla conductual**
  (`possible-penalty` se calcula pero el reporter no lo usa). Solo contabilidad.
  La disuasión opera únicamente por el evento de detección.

## Comportamiento social

- `treshold-influence-income` (1.65): umbral del canal "vecino más rico".
- `period-frauds` (5): **ventana en auditorías, no en ticks** (`fraud-detect-hist` solo se
  anexa al ser auditado). Persistencia real ≈ PF/audit-rate ticks. Ver nota 05.
- `learning-rate` (0.05): velocidad de convergencia de `risk-aversion` al nivel vecinal.
- `initial-Risk-aversion` (0.5): aversión inicial; fija la velocidad de deriva inicial.

## Memoria institucional (tesis)

- `institutional-memory` (1), `audit-noise` (0.0). Con 1/0 ≡ original bit a bit.

## Estrategia (chooser, default `strategic`)

- `random` / `income-level` / `strategic`. Score: `(1-pir) × income × (1-ra)`.
  Con ingreso log-normal σ=7 el término `income` domina: strategic ≈ auditar a los ricos
  + ajuste menor por evasión (ver nota 05, confounding).

## Switches y control

- `visual-fraud-spread?` (OFF): solo color, sin efecto en lógica.
- `start-all-honest?` (ON): parte todo en PIR=1.0. Ojo default (ver nota 02).
- `seed-fraud?` (OFF): paciente cero al 2do tick (ver nota 02).
- `max-nr-simulated-steps` (30000): parada de `go`. En XML headless debe ser ≥ `timeLimit`.

## Convenciones de medición (19 oct)

- `acum_*` cuenta desde el tick 25000 → la tasa es `acum/25000`, no `/50000`.
- Cobertura = `count tax-payers with [sum fraud-detect-hist > 0] / count`:
  fracción con detección recordada en sus últimas PF **auditorías** (no "influencia
  actual": a cobertura 0.65–0.72 el PIR va de 0.07 a 0.53).
- Tasa de detección observada ≈ 63% de las auditorías en todos los regímenes
  (6→16/tick según tasa): escala con volumen, no con cumplimiento → coherente con
  detección dominada por lotería contable (libros congelados, ver nota 05).
