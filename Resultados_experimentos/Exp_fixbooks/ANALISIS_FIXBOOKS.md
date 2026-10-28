# Tercer modelo: libros vivos — réplica y comparación (22 oct 2026)

**Modelo:** `ABM_TESIS_FIXBOOKS.nlogo` = tesis + 3 líneas: `set income-reported
pct-income-report * income` cada tick tras el ajuste conductual (diff verificado,
cero RNG adicional, OFF-equivalente N/A — es otro modelo).
**Experimento:** `Exp_fixbooks/fixbooks.xml`, réplica exacta del PhaseTransition
(16 celdas × 10 reps, 50k ticks; md5 `7e3ac246…` idéntico antes/después).
Tanda única: 89m22s, 9 threads, EXIT=0, 160 runs. Comparación:
`compare_fixbooks.py` (3 PNG + `summary_old_vs_new_pir.csv`).

## 1. Niveles: todo sube, la varianza colapsa

PIR vivos − congelados por celda: random PF1 +0.12/+0.12/+0.045/−0.003;
random PF5 +0.02…+0.05; strategic PF1 +0.03/+0.004/+0.008/+0.009;
strategic PF5 0.02: 0.598→0.583 (−0.015, misma media).
Desviaciones colapsan: stds 0.001–0.009 en 15/16 celdas (vs hasta 0.26).
Excepción: strategic PF5 0.02 conserva std 0.295.

Lectura: con detección genuina la disuasión premia exactamente al cumplidor
total (único escape del flag binario), el sistema sube de nivel y se estabiliza.

## 2. Firma conductual pre-registrada: CONFIRMADA con el control correcto

Test ingenuo (r global det vs evasión): −0.28 / −0.04 — **no informativo**,
confundido por volumen (la tasa mueve ambas en sentido opuesto).
Test correcto (r intra-tasa): congelados −0.02/−0.55/−0.09/−0.19;
**vivos +0.38/+0.25/+0.18/+0.14 en 0.02/0.03/0.04/0.05** (cae con la tasa porque
el techo comprime varianza). La detección con libros vivos sigue a la evasión
real; con libros congelados no (lotería). El bug era load-bearing, no cosmético.

## 3. Biestabilidad: sobrevive y se afina

- Strategic PF1 0.02: el escape (0.747) **desaparece** — 10/10 en ≥0.995.
  Era artefacto de señales espurias, no segunda cuenca.
- Strategic PF5 0.02: la dispersión **persiste** (0.27–0.98) pero cambia de forma:
  continuo uniforme → **dos clusters** (6 runs 0.27–0.38 + 4 runs 0.85–0.98).
  Con disuasión informativa, la indeterminación se vuelve biestabilidad genuina.

## 4. Qué replica y qué no del modelo original

Replica: dominancia strategic PF1 en todo el rango; peor celda strategic PF5 0.02;
random lineal PF1 / techo PF5; orden de tasas de detección por volumen.
No replica: niveles absolutos (vivos +0.02…+0.12), varianzas (colapsan),
forma de la zona indeterminada (uniforme → bimodal), escape PF1 (desaparece).
**El fenómeno central (focalización frágil a baja cobertura + memoria) es
robusto al fix; los niveles y la forma de la dispersión, no.**

## 5. Pendiente

Incluir `ABM_TESIS_FIXBOOKS.nlogo` en el commit (quedó fuera por la corrida en
curso); decidir modelo canónico de la tesis (recomendación: vivos, documentando
la diferencia con Canessa); falsos positivos con libros vivos (fracción en pir≈1
detectada por redondeo vs 1.0 exacto — borde numérico, revisar).
