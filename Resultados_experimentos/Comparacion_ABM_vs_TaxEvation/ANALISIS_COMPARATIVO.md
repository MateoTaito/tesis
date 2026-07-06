# Análisis Comparativo: ABM_Original vs Tax-Evation con institutional-memory=1

## Conclusiones Principales

### ✅ SÍ SON EQUIVALENTES (post-fix 2026-07-06)

Tras el fix aplicado a `ABM_TESIS_CHANGES.nlogo`, los modelos `ABM_Original` y `ABM_TESIS_CHANGES` con `institutional-memory = 1` y `audit-noise = 0` producen **resultados idénticos bit-a-bit** bajo la misma seed aleatoria.

---

## Evidencias

### 1. Validación con seed fija (experimento `Validation`)

Experimento corto (1000 steps, 1 repetición, 3 estrategias) ejecutado con `random-seed 42`:

| Estrategia | ABM_Original (PIR / PRA) | ABM_TESIS_CHANGES (PIR / PRA) | Match |
|---|---|---|---|
| random | 0.5978588931629338 / 0.8378434305378016 | 0.5978588931629338 / 0.8378434305378016 | ✅ |
| income-level | 0.37792733687601177 / 0.5444350547293152 | 0.37792733687601177 / 0.5444350547293152 | ✅ |
| strategic | 0.7515042258717759 / 0.9572866935599085 | 0.7515042258717759 / 0.9572866935599085 | ✅ |

### 2. Validación con múltiples seeds

| Seed | random | income-level | strategic |
|---|---|---|---|
| 42  | ✅ idéntico | ✅ idéntico | ✅ idéntico |
| 7   | ✅ idéntico | ✅ idéntico | ✅ idéntico |
| 100 | ✅ idéntico | ✅ idéntico | ✅ idéntico |

---

## Cambios aplicados para lograr la equivalencia

### 1. Orden de captura del historial

**Antes:** la captura de `income-history` se hacía DESPUÉS de `make-audit` y ANTES de `set income`, lo que producía un rezago de 1 tick. El offset 0 de `income-history` siempre correspondía al tick anterior, nunca al actual.

**Después:** la captura se hace al INICIO del tick, ANTES de `make-audit`. El offset 0 de `income-history` contiene el par `[income, income-reported]` que se está auditando en este tick.

### 2. Ventana deslizante para `audited-periods`

**Antes:** `audited-periods` crecía monotónicamente y nunca se recortaba. Una vez que un período se marcaba como auditado, nunca se re-auditoria. Con `institutional-memory=1`, esto significaba que cada contribuyente era auditado una sola vez y luego ignorado por el resto de la simulación.

**Después:** `audited-periods` se recorta en lockstep con `income-history` cada tick. Cuando un dato viejo se elimina de `income-history` (FIFO), su marca correspondiente en `audited-periods` también se elimina. Esto permite que cada contribuyente sea re-auditable en cada tick, replicando el comportamiento del modelo original.

### 3. Quitar hacks `+ 1` en `num-periods-to-audit` y marcado

Eran workarounds para "fingir" que el período actual estaba en `income-history`. Con la captura movida al inicio, ya no son necesarios.

### 4. Guarda `any-audit-happened` (CRÍTICO)

**Problema detectado:** en la versión inicial del fix, el `ask x [...]` que aplica el resultado al contribuyente se ejecutaba SIEMPRE (incluso cuando el `random-float 1` fallaba). El modelo original solo ejecuta ese `ask x [...]` si pasa la verificación de eficiencia. Cada `ask` consume un número aleatorio, así que ejecutar el `ask` adicional alteraba la secuencia aleatoria y rompía la equivalencia.

**Solución:** introducir un flag `any-audit-happened` que se pone en `true` solo si algún período pasa la verificación de eficiencia, y envolver el `ask x [...]` en `if any-audit-happened [...]`. Esto replica exactamente la guarda del modelo original.

### 5. Iteración por who-number en captura

**Problema detectado:** `ask tax-payers [...]` sobre un agentset dispara comportamiento interno de NetLogo que consume números aleatorios de forma no documentada, alterando la secuencia aleatoria.

**Solución:** usar `repeat n-capture [ask turtle i-capture [...]]` para iterar por who-number. Esto evita el consumo aleatorio espurio del agentset.

---

## Por qué el análisis previo mostraba "no equivalentes"

El análisis comparativo previo (`ANALISIS_COMPARATIVO.md` original) llegaba a la conclusión "no equivalentes" basándose en:

1. **Outliers espurios**: el script `comparison_analysis_final.py` tenía un bug de parseo (`col_offset += 11` debería ser `+= 10`) que leía columnas incorrectas del CSV. Los valores `2911`, `10000`, `4655` que parecían outliers son en realidad `SS_PIAR`/`SS_RA`, no `mean [risk-aversion]`.

2. **Diferencia real en el modelo**: la TESIS original tenía el bug de captura post-audit que producía detección casi nula con `institutional-memory=1` (los datos leídos eran siempre `[0 0]` en el primer tick, y luego se reusaba el mismo slot para siempre). Por eso los `risk_aversion` se quedaban en ~0.39 (sin castigo, sin aprendizaje) en lugar de ~0.5-0.9 (con castigo).

Tras el fix, ambos problemas están resueltos.

---

## Archivos Generados

```
Comparacion_ABM_vs_TaxEvation/
├── abm_orig_emupaper.csv         # ABM_Original.nlogo, experimento ExperEmuPaper
├── tesis_emupaper_postfix.csv    # ABM_TESIS_CHANGES.nlogo, experimento Exper_emu_paper
├── taxevation_postfix.csv        # ABM_TESIS_CHANGES.nlogo, Exper_emu_paper (versión de Exp_post_fix)
└── ANALISIS_COMPARATIVO.md       # Este archivo
```

## Veredicto Final

**Status: EQUIVALENTES (con caveats)**

- ✅ Con `institutional-memory = 1` y `audit-noise = 0`, los modelos producen resultados idénticos bit-a-bit bajo la misma seed.
- ✅ Validado con seeds 42, 7 y 100.
- ⚠️ Con `institutional-memory > 1` o `audit-noise > 0`, los modelos difieren por diseño (es la feature que se está estudiando).
- ⚠️ El experimento `Exper_emu_paper` (3 reps, 10000 steps) NO usa seed fija, por lo que las corridas individuales entre ABM_Original y ABM_TESIS_CHANGES usan seeds distintas y producen resultados diferentes. Esto es esperado: son corridas independientes. La equivalencia bit-a-bit se valida con el experimento `Validation` (seed fija).
