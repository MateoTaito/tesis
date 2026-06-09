# Lámina: Formulación de Hipótesis Alterna

**Tesis:** *Simulaciones de Cumplimiento Tributario: La Interacción entre la Memoria Institucional y la Memoria Social en Modelos Basados en Agentes*

---

## H1: Formulación de la hipótesis alterna

> **H1:** *En un Modelo Basado en Agentes de cumplimiento tributario, incrementar la profundidad de la memoria institucional del ente fiscalizador (es decir, su capacidad de auditar períodos fiscales pasados) aumenta la tasa agregada de cumplimiento (medida como porcentaje de ingreso reportado, PIAR) en el estado estacionario, y este efecto es **mayor** cuando la memoria social de los contribuyentes (su capacidad de recordar y aprender de las experiencias de fiscalización de sus pares) es alta.*

En palabras operativas:
- **Variable independiente 1:** `institutional-memory` ∈ {1, 3, 5, 7, 15} — períodos retrospectivos auditables.
- **Variable independiente 2:** `period-frauds` ∈ {1, 5} — ventana de memoria social del contribuyente.
- **Variable dependiente:** `mean [pct-income-report] of tax-payers` en el estado estacionario (`SS_PIAR`) y/o `acum_frauds_detected`.
- **Predicción direccional:** la pendiente de `PIAR` respecto a `institutional-memory` es positiva, y se acentúa cuando `period-frauds` es alto, porque la disuasión retrospectiva se propaga horizontalmente con mayor eficiencia en redes con memoria social prolongada.

La hipótesis nula (H0) asociada plantea que la memoria institucional **no tiene efecto**, o que su efecto **no depende** del nivel de memoria social (es decir, la pendiente es nula o constante entre niveles de `period-frauds`).

---

## Breve descripción del protocolo

**Tipo de protocolo:** simulación computacional (ABM) con barrido factorial completo, ejecutada en NetLogo 6.4.0.

**Diseño experimental — 3 × 2 factorial:**

| Factor | Niveles |
|--------|---------|
| Estrategia de auditoría (`tax-payer-audit-selection`) | random, income-level, strategic |
| Memoria social (`period-frauds`) | 1 (baja), 5 (alta) |
| Memoria institucional (`institutional-memory`) | 1, 3, 5, 7, 15 |

Para cada combinación: **N = 30 repeticiones independientes** con semillas aleatorias distintas, **duración = 5 000 ticks** (acorde a `Especificacion_Exper_emu_paper.md`).

**Parámetros fijos (del experimento base):**
- Población: `nr-tax-payers = 500`, `nr-auditors = 20`
- `actual-audit-rate = 0.20`
- `tax-rate = 0.27`, `penalty-rate = 1.5`
- `learning-rate = 0.05`, `initial-Risk-aversion = 0.5`

**Métricas registradas al final de cada corrida:**
- `mean [pct-income-report] of tax-payers` (PIAR final / `SS_PIAR`)
- `acum_frauds_detected`, `acum_frauds_perpretated`
- `mean [risk-aversion] of tax-payers` (MRA / `SS_RA`)

**Análisis estadístico:**
- ANOVA factorial de dos vías (`institutional-memory` × `period-frauds`) sobre `PIAR` en estado estacionario.
- Término de **interacción** explícito: si el efecto de `institutional-memory` difiere significativamente entre `period-frauds = 1` y `period-frauds = 5`, se rechaza H0 en favor de H1.
- Gráficos de líneas de interacción (estilo `plot_interaction_analysis.py` ya disponible).

**Ejecución headless:**
```bash
netlogo-headless \
  --model "ABM_TESIS_CHANGES.nlogo" \
  --setup-file experiment.xml \
  --experiment "memoria_institucional_x_social" \
  --table resultados.csv
```

---

## Identificación de un posible sesgo

**Sesgo principal: dependencia de la condición inicial (*initial-condition bias* / *path dependence*).**

El modelo incluye procesos de **memoria estructural** que acumulan información a lo largo de los ticks:
- `income-history` (FIFO de profundidad `institutional-memory`).
- `audited-periods` (registro de períodos ya fiscalizados).
- `fraud-detect-hist` (ventana de `period-frauds`).
- `cumulative-nr-audits` y `cumulative-nr-audits-OK` (ajustan la eficiencia del auditor cada 100 auditorías).

Durante los **primeros miles de ticks**, estas estructuras se están "llenando" y los agentes aún no han explorado su espacio de comportamiento. Por tanto, una corrida de 5 000 ticks —o incluso 10 000— puede capturar estados **transitorios** altamente sensibles a la semilla aleatoria inicial (posición de los contribuyentes en la grilla, draws log-normales de `income`, valores iniciales de `pct-income-report`).

Esto introduce dos problemas concretos:
1. **Alta varianza intra-celda** → se requieren muchas repeticiones para detectar efectos moderados.
2. **Riesgo de confundir convergencia con estado estacionario genuino** → los detectores automáticos (`PIAR < 0.000001`) podrían activarse en mesetas transitorias.

Adicionalmente, existe un **sesgo de selección de semillas**: si las 30 réplicas se inicializan con semillas consecutivas (`random-seed 0`, `1`, …, `29`), se corre el riesgo de que la secuencia del generador pseudoaleatorio de NetLogo tenga patrones de baja cobertura en ese tramo del espacio de semillas.

---

## Forma de reducir o eliminar el sesgo detectado

Para abordar el problema de **dependencia de la condición inicial** se proponen tres contramedidas complementarias:

### 1. Aumento de la corrida de equilibración (*warm-up*) y descarte transitorio
- Extender la duración total a **20 000 – 50 000 ticks** (consistente con la nota de AGENTS.md: *"el modelo tarda miles de ticks en converger"*).
- Descartar explícitamente los primeros **10 000 ticks** del análisis (alineado con el checkpoint `PIAR_10000` ya existente en el modelo) y medir `SS_PIAR`/`SS_RA` solo sobre los ticks 10 001–50 000.
- Verificar visualmente con gráficos de series de tiempo (`PIAR_ticks`) que la fase medida está claramente en estado estacionario.

### 2. Mayor número de repeticiones con semillas dispersas
- Aumentar de **N = 30 a N ≥ 100** réplicas por celda factorial.
- Utilizar **salto de semilla** (`random-seed (n * 1000 + 1)`) en lugar de semillas consecutivas, para garantizar cobertura uniforme del espacio aleatorio.
- Calcular **intervalos de confianza al 95%** mediante *bootstrap* sobre las réplicas (consistente con `plot_interaction_analysis_3runs.py`).

### 3. Validación cruzada con un experimento "limpio" (*fresh-start*)
- Ejecutar una réplica adicional con `institutional-memory` y `audit-noise` forzados a sus **valores por defecto** (1 y 0 respectivamente) durante los primeros 5 000 ticks, y luego **activar** la memoria institucional a partir del tick 5 000. Comparar la trayectoria post-activación contra la condición control.
- Si las trayectorias convergen al mismo `SS_PIAR`, hay evidencia robusta de que el estado estacionario **no depende de la historia previa** → el sesgo se controla experimentalmente.

Con estas tres medidas combinadas, se minimiza la probabilidad de que un resultado favorable a H1 sea un artefacto de la condición inicial, y se fortalece la **validez interna** del contraste H0 vs. H1.
