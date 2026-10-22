# 05 — Cambio de fase: del barrido 10k al experimento 50k (14–19 oct 2026)

## Punto de partida

Barrido `Exp_audit_sweep` (N=1, seed 42 fijo, 10k ticks, valor final): strategic PF1
sigmoide con salto 0.03→0.04 (0.696→0.981); random lineal sin umbral; PF5 suaviza;
`income-level` colapsado en todas partes. Firma específica del targeting, no del fraude.

## Experimento `PhaseTransition` (15 oct)

48 runs headless (~20 min, 9 threads): rates {0.02,0.03,0.04,0.05} × {random, strategic}
× PF {1,5} × 3 reps, 50k ticks, 11 métricas (incl. cobertura de detecciones recordadas
y `mean fiscal-risk-score`, sin tocar el modelo). Seeds aleatorias (N=3 real).
Dir: `Resultados_experimentos/Exp_phase_transition/` (XML, CSV, script, 6 PNG).
Análisis completo: `ANALISIS_PHASE50k.md`.

## Resultados

| PF | 0.02 | 0.03 | 0.04 | 0.05 (PIR strategic / random) |
|---|---|---|---|---|
| 1 | 0.908±0.140 / 0.096±0.019 | 0.992 / 0.208 | 0.990 / 0.383 | 0.988 / 0.484 |
| 5 | 0.511±0.285 / 0.915±0.014 | 0.960 / 0.964 | 0.964 / 0.978 | 0.973 / 0.981 |

Welch strategic vs random PF1: diffs +0.50…+0.81, todos p<0.01. PF5 0.02: −0.404,
p=0.133 (sin potencia).

## Conclusiones

1. **El colapso en medias bajo 0.04 no replica a 50k: era transitorio.**
   Strategic PF1 0.02: 0.388 (10k) → 0.908 (50k, delta +0.478). La rotación del targeting
   tarda >10k ticks en "pasar la escoba" a baja cobertura.
2. **Lo que lo reemplaza: biestabilidad bajo ~0.03.** A 0.02 los runs strategic se separan
   (PF1: 0.747 vs ~0.99; PF5: 0.27/0.43/0.83); random es apretado. Peor celda:
   strategic PF5 0.02 (persiste la "joroba" de N30).
3. **No-convergencia generalizada**: random PF1 0.02 sigue cayendo (delta −0.113);
   random PF5 0.02 sigue subiendo (+0.255). Ni 50k alcanza en los extremos.
4. **Detector SS inválido**: random PF1 0.02 disparó `SS_PIAR` en ~7400 y cayó 0.11 más.
   Dispara en mesetas transitorias (confirma N30 §5).
5. **Libros congelados (heredado del original, grave)**: `income-reported` se fija solo
   en setup (`:476`); la detección compara ingreso fresco (σ=7) contra libros del tick 0,
   así que dispara por lotería (~63% de auditorías) más que por conducta. La disuasión
   opera por flujo de señales, no por precisión. Pendiente cuantificar falsos positivos
   (detecciones con PIR actual ≈1) antes de afirmar nada sobre precisión del targeting.

## Disección de la biestabilidad (19 oct, `plot_bistability.py`, N=10)

- Random determinista en las 8 celdas (PF1 0/10 en techo, PF5 10/10).
  Strategic PF1 0.02: 9/10 techo + 1 escape. Strategic PF5 0.02: 1/10 techo,
  valores continuos 0.27–0.94 **sin clusters** → indeterminación, no dos atractores.
- Lock-in temprano: r(PIAR_10000, final) +0.65…+0.86 en strategic.
- Cobertura acompaña (r=+0.95) pero **no determina** (0.65–0.72 → PIR 0.07–0.53).
  Detección ortogonal al PIR (r=+0.28; 6→16/tick según tasa).
- Evidencia concentración vs dispersión: random PF5 0.02 detecta 6.2/tick → 0.925;
  strategic 8.5/tick → 0.598 (cobertura recordada 0.921 vs 0.823).
- PRA–PIR acoplados a 50k (r=+0.93). Detalle en `ANALISIS_PHASE50k.md` §7.

## Experimento de trayectorias (19 oct, completado)

`Exp_trajectories/trajectory.xml`: solo tasa 0.02, {random, strategic} × PF {1,5} ×
10 reps, 50k ticks, `runMetricsEveryStep=true` (PIR, PRA, cobertura; 2M filas).
Análisis: `ANALISIS_TRAJECTORIES.md`. Resultado: divergencia **tardía** (std cruza 0.1
en ~21–25k) con ranking temprano (r 0.65–0.86 a 10k). PF1 = un atractor + despegues
dispersos que convergen (std en baja a 0.04); PF5 = despegues tan dispersos que a 50k
coexisten regímenes — indistinguible entre biestabilidad y transitorio ultra-lento
sin 100k+ ticks. Varias runs PF5 aún subiendo a 50k (+0.04/ktick máx).

## Caveats y pendientes

- ~~N=3 sin potencia en la zona biestable~~ **Resuelto parcial 15 oct**: extensión
  pre-registrada a N=10 (tanda 2: 112 runs, 59 min; modelo md5 idéntico; merge con
  procedencia en `MERGE_N10.txt`). PF5 0.02 ahora significativo (p=0.0032);
  distribuciones: strategic PF1 0.02 → 9/10 techo + 1/10 en 0.747; strategic PF5 0.02 →
  dispersión total 0.27–0.94 sin clusters. El N≥30 sigue pendiente, focalizado en 0.015–0.035.
- Ventana de medición 30k–50k en vez de valor final; falta ANOVA factorial.
- Historia a contar en la tesis: 10k transitorio → 50k biestable/convergente (régimen +
  histéresis, no umbral nítido en medias). Implicancia de política falsable: bajo
  cobertura escasa, focalizar por riesgo rinde peor que aleatorizar (el SII real <1%
  está bajo la zona de colapso).
