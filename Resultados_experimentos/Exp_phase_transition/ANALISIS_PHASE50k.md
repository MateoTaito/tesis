# Experimento `PhaseTransition` — análisis (N=3, 50k ticks)

**Diseño:** `audit-rate ∈ {0.02, 0.03, 0.04, 0.05}` × `{random, strategic}` × `PF ∈ {1,5}`,
3 reps = 48 runs, 50k ticks, métrica final. Fijas: 500 txps, 20 auditores, tax 0.27,
penalty 1.5, learning 0.05, initRA 0.5, threshold 1.65, k=1, noise=0,
`start-all-honest?=false`, `seed-fraud?=false` (comparable con resultados previos).
**CSV:** `phase_transition_50k.csv`. **Gráficos:** 6 PNG (300 dpi, mean±std).
**Estadística:** Welch por celda (n=3+3; gl≈2–4; ojo: potencia baja, |t|>4.3 ⇒ p<0.05 con gl=2).

## 1. PIR final (mean±std, N=3)

| estrategia | PF | 0.02 | 0.03 | 0.04 | 0.05 |
|---|---|---|---|---|---|
| random | 1 | 0.096±0.019 | 0.208±0.028 | 0.383±0.020 | 0.484±0.063 |
| random | 5 | 0.915±0.014 | 0.964±0.007 | 0.978±0.005 | 0.981±0.005 |
| strategic | 1 | 0.908±0.140 | 0.992±0.004 | 0.990±0.004 | 0.988±0.004 |
| strategic | 5 | 0.511±0.285 | 0.960±0.001 | 0.964±0.009 | 0.973±0.007 |

Valores por run en celdas biestables: strategic PF1 0.02 → [0.747, 0.994, 0.984];
strategic PF5 0.02 → [0.431, 0.827, 0.275]. Random: dispersión mínima en las 8 celdas.

## 2. Contrastes strategic vs random (Welch, PIR)

| celda | diff | t | p | veredicto |
|---|---|---|---|---|
| PF1 0.02 | +0.813 | +10.0 | 0.009 | **strat ≫ rand** |
| PF1 0.03 | +0.784 | +47.4 | <0.001 | **strat ≫ rand** |
| PF1 0.04 | +0.606 | +52.1 | <0.001 | **strat ≫ rand** |
| PF1 0.05 | +0.504 | +13.9 | 0.005 | **strat ≫ rand** |
| PF5 0.02 | −0.404 | −2.45 | 0.133 | sugestivo, **sin potencia** (std strat 0.285) |
| PF5 0.03–0.05 | −0.004..−0.014 | ns | ns | equivalentes |

## 3. Hallazgos

**H1. El "colapso strategic bajo 0.04" del barrido 10k era transitorio.**
Comparación mismo setup (sweep N=1 seed 42 @10k vs este N=3 @50k), strategic PF1:
0.02: 0.388→0.908; 0.03: 0.696→0.992; 0.04: 0.981→0.990.
Deltas 10k→50k: strategic PF1 +0.478 (0.02), +0.308 (0.03). El targeting por rotación
necesita >10k ticks para "pasar la escoba" a baja cobertura. A 50k, strategic PF1
domina a random en TODAS las tasas (p<0.01). El cambio de fase en medias **no replica**
a 50k; se reubica en (H2).

**H2. Bajo 0.03, strategic entra en zona biestable (path-dependence).**
A 0.02 los runs se separan (0.75 vs 0.99 en PF1; 0.27/0.43/0.83 en PF5) mientras random
es apretado. Interacción con PF: la peor celda es strategic PF5 0.02 (0.511±0.285;
persiste la "joroba" de N30). Con N=3 la dif. PF5 0.02 no alcanza p<0.05: el N≥30
debe concentrarse en el vecindario 0.02.

**H3. Random PF1 sigue cayendo a 50k; random PF5 sigue subiendo.**
Deltas: random PF1 0.02 → −0.113, 0.03 → −0.063 (piso 0 en camino); random PF5 0.02 →
+0.255 (ni a 50k converge). La respuesta lineal de random esconde no-estacionariedad
en ambos extremos.

**H4. El detector SS es inválido como criterio de convergencia.**
Caso limpio: random PF1 0.02 disparó SS_PIAR en ticks 7343–7541 en los 3 runs, pero el
PIR cayó 0.11 más hasta 50k. Dispara en mesetas transitorias (confirma N30 §5).

## 4. Hallazgo de código: libros congelados (heredado del original)

`income-reported` se asigna SOLO en setup (`ABM_TESIS_CHANGES.nlogo:476`) y nunca se
actualiza. La detección compara ingreso fresco (sorteo log-normal σ=7 cada tick)
contra libros del tick 0: con esa varianza, `income_t > reported_setup` ocurre la
mayoría de las veces **independientemente de la conducta actual**. Implicancias:
(i) la tasa de detección observada (~63% de las auditorías: 6.3/10 a 0.02, 16.8/25
a 0.05) está dominada por lotería, no por evasión real; (ii) `fraud-detect-hist` solo
se anexa al ser auditado (`:343-359`, ventana en *auditorías*, no en ticks), luego la
persistencia real de una señal es PF/audit-rate ticks (50 vs 250 ticks a 0.02);
(iii) `income-level` selecciona por libros congelados. La disuasión del modelo opera
por flujo de señales, no por precisión contable. Pendiente cuantificar: fracción de
detecciones con PIR actual ≈1 ("falsos positivos").

## 5. Qué falta

1. Barrido fino 0.015–0.035 (paso 0.005) N≥30 a 50k, foco en biestabilidad strategic
   (distribución por seed, no solo medias). 2. Métrica de falsos positivos de detección.
   3. Ventana de medición 30k–50k en vez de valor final. 4. ANOVA factorial.

## 6. Actualización N=10 (15 oct, extensión pre-registrada)

Segunda tanda: 112 runs (7 reps/celda), mismo modelo (md5 `9f7147e6…` verificado
idéntico) y mismo XML salvo `repetitions`. Fusionado con `merge_N10.py`:
`phase_transition_50k_N10.csv` (160 filas, `[run number]` 1..10 por combo,
trazabilidad en `MERGE_N10.txt`). Tiempo tanda 2: 59m26s en 9 threads.

PIR (mean±std, N=10) — solo cambios vs N=3: strategic PF1 0.02 → **0.967±0.077**;
strategic PF5 0.02 → **0.598±0.260**. Resto idéntico al decimal.

Welch strategic vs random (10+10): PF1 diffs +0.51…+0.87, todos p<0.0001.
**PF5 0.02: diff −0.327, t=−3.97, p=0.0032 → significativo: strategic peor que random.**
PF5 0.03–0.05: diffs ≤0.014, ns (0.04 da p=0.022 nominal, irrelevante en magnitud y
sin corrección por multiplicidad).

Distribuciones a 0.02 (el hallazgo fino):
- strategic PF1: 9/10 en techo (0.983–0.998) + 1/10 colapsado (0.747). Lock-in malo raro (~10%).
- strategic PF5: [0.275, 0.280, 0.324, 0.431, 0.506, 0.757, 0.821, 0.822, 0.827, 0.936]
  — dispersión total sin clusters: con memoria larga + targeting + auditoría escasa,
  el resultado es lotería de seed. Random en las mismas celdas: std 0.013–0.020.

Revisión de H1–H2 con N=10: el "no colapso en medias" se mantiene (strategic PF1 ≥
random en todo, p<0.0001); la biestabilidad se confirma y se localiza: es un fenómeno
de **strategic × cobertura escasa**, máximo con PF5, inexistente en random.

## 7. Disección de la biestabilidad con N=10 (19 oct, `plot_bistability.py`)

Sin trayectorias (los CSV son valor final + tick 10000): distribuciones por run,
clasificación techo (PIR≥0.9, convencional), abanico y cruces.

- Random es determinista en las 8 celdas: PF1 0/10 en techo (bandas apretadas
  0.07–0.13 a 0.02), PF5 10/10 en techo. Sin dispersión.
- Strategic PF1 0.02: 9/10 en techo + 1 escape (0.747). Lock-in malo raro (~10%).
- Strategic PF5 0.02: 1/10 en techo; valores [0.275…0.936] **continuos, sin clusters**:
  indeterminación, no dos atractores. Con N=10 el IC95 de la tasa de techo es 0.02–0.40.
- Lock-in temprano: r(PIAR_10000, PIR_final) = +0.77 en strategic PF5 0.02
  (+0.65…+0.86 en el resto de strategic). El destino se decide antes del tick 10k.
- Cobertura acompaña (r=+0.95 global) pero **no determina**: a cobertura 0.65–0.72
  el PIR va de 0.07 a 0.53; es en parte consecuencia (más evasión → más detecciones).
- Tasa de detección r=+0.28 con el PIR: la escala con la tasa (6→16/tick), no con
  el cumplimiento — coherente con detección por lotería contable. Clave:
  random PF5 0.02 detecta 6.2/tick → PIR 0.925; strategic detecta 8.5/tick → PIR 0.598.
  **Mismo orden de volumen, resultado opuesto: importa dónde caen las señales
  (concentración vs dispersión), no cuántas.** Cobertura recordada: 0.921 vs 0.823.
- PRA y PIR acoplados a 50k (r=+0.93 por run).
