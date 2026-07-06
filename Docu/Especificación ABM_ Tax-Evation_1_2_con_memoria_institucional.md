# Especificación ABM: Tax-Evation_1_2 con Memoria Institucional

**Alcance y criterio de trazabilidad**
- Este documento describe el modelo `Tax-Evation_1_2.nlogo` incluyendo la feature de **memoria institucional** agregada sobre la versión base.
- Cuando se interpreta el significado real de una variable/proceso, se etiqueta como supuesto por nomenclatura, sin agregar mecanismos no codificados.

---

## 1) Agentes

### 1.1 Tipos de agentes
- **tax-payers** (breed `tax-payers`)
- **auditors** (breed `auditors`)

### 1.2 Variables asociadas

#### a) `tax-payers-own`

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `pct-income-report` | Float [0,1] | Proporción de ingreso reportado |
| `income` | Float ≥0 | Ingreso del período (draw log-normal cada tick) |
| `audit?` | Boolean | Indicador de si fue seleccionado para auditoría en el tick |
| `income-reported` | Float ≥0 | Ingreso reportado en el tick (`pct-income-report × income`) |
| `after-tax-income` | Float ≥0 | Ingreso neto tras impuestos/penalidad según resultado de auditoría |
| `risk-aversion` | Float [0,1] | Aversión al riesgo del contribuyente |
| `fraud-detected?` | Boolean | Indicador de detección de subreporte (en tick actual) |
| `fiscal-risk-score` | Float | Puntaje de riesgo fiscal usado en selección estratégica |
| `fraud-detect-hist` | Lista de [0,1] | Historial deslizante de detecciones por ventana temporal (`period-frauds`) |
| `under_rep_income` | Float | Monto subreportado en el tick (si aplica) |
| **`income-history`** | Lista de [income, income-reported] | **NUEVO:** Historial de ingresos reales y reportados por tick (profundidad = `institutional-memory`, FIFO) |
| **`audited-periods`** | Lista de Boolean | **NUEVO:** Registro booleano de qué períodos (offset 0 = actual, 1 = anterior, etc.) ya fueron auditados. Se expande dinámicamente y marca `true` cuando se audita. |

#### b) `auditors-own`

| Variable | Tipo | Descripción |
|----------|------|-------------|
| `pct-audit-efficiency` | Float [0.5,1) | Probabilidad/eficiencia operativa individual del auditor |
| `selected-txp-audit` | Lista de turtles | Contribuyentes asignados a ese auditor |
| `nr-audits` | Int | Número de auditorías asignadas en el tick |
| `cumulative-nr-audits` | Int | Acumulado para ajuste de eficiencia |
| `cumulative-nr-audits-OK` | Int | Acumulado de detecciones exitosas para ajuste de eficiencia |

### 1.3 Variables globales nuevas

| Variable | Tipo | Rango | Descripción |
|----------|------|-------|-------------|
| **`institutional-memory`** | Int | [1, 15] | **NUEVO:** Profundidad de revisión histórica. Cuántos períodos hacia atrás (incluyendo el actual) puede auditar un contribuyente. |
| **`audit-noise`** | Float | [0, 0.5] | **NUEVO:** Factor de ruido que dificulta detecciones en períodos pasados. Se aplica como `audit-noise × period-offset` reduciendo la probabilidad de detección. |

### 1.4 Comportamientos

#### a) Contribuyentes (tax-payers)

**Inicialización (`setup-tax-payers`):**
- Nacen en parches aleatorios (`sprout-tax-payers`)
- `pct-income-report` aleatorio en [0,1)
- `income` generado por `log-normal-x 16 7`
- `risk-aversion` = `initial-Risk-aversion`
- `income-history` = [] (vacio)
- `audited-periods` = [] (vacio)
- Estados de auditoría/detección inicializados en falso

**Dinámica por tick:**
1. Participa en proceso de auditoría (`make-audit`)
2. Ajusta `risk-aversion` con `txp-adjust-risk-aversion` según vecinos e historial percibido de sanciones
3. Ajusta `pct-income-report` con regla multiplicativa dependiente de `audit?`, `fraud-detected?` y `risk-aversion`
4. Se guarda el par `[income, income-reported]` en `income-history` (FIFO, profundidad máxima = `institutional-memory`)
5. Se recalcula `income` cada tick con `log-normal-x 16 7`

#### b) Auditores (auditors)

**Inicialización (`setup-auditors`):**
- Se crean `nr-auditors` auditores
- `pct-audit-efficiency` inicial aleatoria en [0.5, 1)
- Se ocultan (`hide-turtle`)

**Dinámica por tick:**
1. Reciben asignación de contribuyentes (`select-auditors`)
2. Ejecutan detección con **memoria institucional**:
   - Por cada contribuyente auditado, revisan hasta `institutional-memory` períodos hacia atrás
   - Cada período se audita **solo si no fue auditado antes** (según `audited-periods`)
   - La eficiencia se reduce por: **fatiga** (5% por período) + **ruido histórico** (`audit-noise × period-offset`)
   - Se acumulan todas las penalidades detectadas en distintos períodos y se **aplican en conjunto** en el tick actual
3. Al terminar la auditoría, se marcan todos los períodos revisados como auditados en `audited-periods`
4. Actualizan métricas acumuladas de desempeño
5. Ajustan eficiencia periódicamente (`auditors-adjust-pct-eff`) cada 100 auditorías acumuladas

### 1.5 Lo que representan
- **tax-payers**: contribuyentes que deciden cuánto ingreso reportar
- **auditors**: agentes de fiscalización con capacidad de detección imperfecta y memoria histórica
- **risk-aversion**: predisposición conductual a evitar riesgo de sanción
- **fraud-detect-hist**: memoria social reciente de detecciones observadas (ventana `period-frauds`)
- **income-history**: registro contable del contribuyente para revisión retrospectiva
- **audited-periods**: tracking de qué períodos fiscales ya fueron auditados (evita re-auditoría)
- **institutional-memory**: capacidad legal/institucional de revisar períodos pasados
- **audit-noise**: degradación de la calidad de detección cuanto más lejano es el período revisado

---

## 2) Espacio

- Mundo GRAPHICS-WINDOW de NetLogo con parches en grilla
- `max-pop-size = (max-pxcor + 1) × (max-pycor + 1)`
- Contribuyentes sobre parches (uno por parche)
- Interacción local: vecindad `neighbors` (8 vecinos de Moore)
- Auditores no ocupan rol espacial explícito (ocultos)

---

## 3) Time step: interacciones por tick

### Orden lógico de `go`:

1. **Condición de parada**: si `ticks = max-nr-simulated-steps`, se detiene
2. **Registro de series**: agrega media de `pct-income-report` a `PIAR_ticks` y media de `risk-aversion` a `RA_ticks`
3. **Detección de pseudo estado estacionario**: umbral `PIAR < 0.000001`, `RA < 0.0005`
4. **Checkpoint tick 10000**: guarda `PIAR_10000` y `PRA_10000`
5. **Guardar historial contable (incluye período actual)**: cada contribuyente agrega `[income, income-reported]` a `income-history` y `false` a `audited-periods`. Si excede `institutional-memory`, elimina el más antiguo de AMBAS listas en lockstep (FIFO, ventana deslizante)
6. **Ejecuta auditoría (`make-audit`)** — ver sección 3.1
7. **Acumulación de métricas** (si `ticks ≥ 25000`)
8. **Ajuste de auditores (`auditors-adjust-pct-eff`)**
9. **Ajuste conductual (`tax-payers-adjust-pct-inc-rep`)**:
   - Ajusta `risk-aversion` por influencia vecinal
   - Ajusta `pct-income-report` con reglas multiplicativas
   - Acota `pct-income-report` a máximo 1
   - Limpia `audit?` y `fraud-detected?`
10. **Reasigna `income`** con nuevo draw log-normal
11. **`tick`**

### 3.1 Proceso detallado de auditoría con memoria institucional (`make-audit`)

```
1. Reset under_rep_income = 0 para todos los tax-payers
2. (Si ticks ≥ 25000) Contar todos los fraudes perpetrados (income-reported < income)
3. Seleccionar contribuyentes a auditar (select-tax-p-audit):
   - random: n-of (round(actual-audit-rate × nr-tax-payers))
   - income-level: prioriza income-reported por encima de mediana
   - strategic: prioriza mayor fiscal-risk-score
4. Asignar contribuyentes a auditores (select-auditors, round-robin)
5. Cada auditor procesa sus asignados:

   Por cada contribuyente x:
   
   a. Inicializar total-penalty = 0, detected-any-fraud = false
   
   b. Para period-offset = 0 hasta (institutional-memory - 1):
      
      Si este período NO fue auditado antes (has-period-been-audited?):
          noise-reduction = audit-noise × period-offset
          effective-efficiency = pct-audit-efficiency × nr-audits-done × (1 - noise-reduction)
          
          Si effective-efficiency > random-float 1:
              Obtener hist-income, hist-income-reported del período
              Si hist-income-reported < hist-income:
                  period-penalty = (hist-income - hist-income-reported) × penalty-rate
                  total-penalty += period-penalty
                  detected-any-fraud = true
                  cumulative-nr-audits-OK += 1
      
      nr-audits-done -= 0.05  (fatiga, 5% por período)
      period-offset += 1
   
   c. Aplicar penalidad acumulada al contribuyente:
      Si detected-any-fraud:
          after-tax-income = max(0, (1-tax-rate)×income - total-penalty)
          fraud-detected? = true
          fraud-detect-hist ← append 1
          under_rep_income = (income - income-reported)
          acum_frauds_detected += 1 (si ticks ≥ 25000)
      Sino:
          after-tax-income = income - tax-rate × income-reported
          fraud-detect-hist ← append 0
      
      Marcar TODOS los períodos revisados como auditados (add-period-to-audited)
   
   d. (Si ticks ≥ 25000) Contar fraude perpetrado si income-reported < income
```

---

## 4) Variables manipulables

### 4.1 Interfaz existente (sin cambios)

| Variable | Control | Rango | Descripción |
|----------|---------|-------|-------------|
| `nr-tax-payers` | slider | 1 - max-pop-size | Contribuyentes iniciales |
| `nr-auditors` | slider | 1 - 100 | Auditores |
| `actual-audit-rate` | slider | [0, 1] | Fracción auditada por tick |
| `tax-payer-audit-selection` | chooser | {random, income-level, strategic} | Estrategia de selección |
| `tax-rate` | slider | [0, 1] | Tasa impositiva |
| `penalty-rate` | slider | [0, 5] | Penalidad por fraude |
| `treshold-influence-income` | slider | [0, 10] | Umbral comparación social |
| `period-frauds` | slider | 1 - 10 | Ventana de memoria social |
| `learning-rate` | slider | [0, 1] | Velocidad de adaptación social |
| `initial-Risk-aversion` | slider | [0, 1] | Aversión al riesgo inicial |
| `max-nr-simulated-steps` | slider | 1 - 100000 | Duración de simulación |

### 4.2 Variables NUEVAS de memoria institucional

| Variable | Control | Rango | Default | Descripción |
|----------|---------|-------|---------|-------------|
| **`institutional-memory`** | slider | [1, 15] | 1 | **NUEVO:** Cantidad de períodos (incluyendo actual) que los auditores pueden revisar retrospectivamente. Con `institutional-memory = 1` y `audit-noise = 0` el comportamiento es **idéntico** al modelo original (validado con misma seed: 42, 7, 100). |
| **`audit-noise`** | slider | [0, 0.5] | 0.0 | **NUEVO:** Factor de ruido que reduce la probabilidad de detección en períodos pasados. La reducción es `audit-noise × period-offset`, donde `period-offset` es la distancia al presente. Con `audit-noise = 0` no hay degradación. |

---

## 5) Nuevas funciones implementadas

| Función | Tipo | Descripción |
|---------|------|-------------|
| `get-income-history-entry [period-offset]` | Reporter | Retorna lista `[income, income-reported]` del período solicitado. Si el offset excede el historial disponible, retorna `[0, 0]`. |
| `has-period-been-audited [period-offset]` | Reporter | Retorna `true` si el offset de período especificado ya fue auditado anteriormente. |
| `add-period-to-audited [period-offset]` | Command | Marca un período como auditado. Expande la lista `audited-periods` con `false` si es necesario, luego cambia a `true` en la posición indicada. |
| `calculate-historical-noise [period-offset]` | Reporter | Calcula el factor de ruido como `audit-noise × period-offset`. |

---

## 6) Lógica de detección de duplicados y ventana deslizante

Cuando un contribuyente es seleccionado para auditoría:
- Se revisa la ventana de `institutional-memory` períodos hacia atrás (incluyendo el actual)
- **Cada período se audita solo si NO fue auditado antes dentro de la ventana actual** (marcado en `audited-periods`)
- Si el período ya fue auditado, se salta la verificación de eficiencia (no se consume `random-float`)
- La fatiga (`nr-audits-done`) se aplica a TODOS los períodos revisados (se salten o no), representando el costo del proceso de revisión
- **Ventana deslizante**: `audited-periods` se recorta en lockstep con `income-history` cada tick. Cuando un dato viejo se elimina de `income-history` (FIFO), su marca correspondiente en `audited-periods` también se elimina. Esto garantiza que cada período se audite como máximo una vez durante su vida en la ventana de memoria institucional
- El `ask x [...]` que aplica el resultado al contribuyente SOLO se ejecuta si el auditor efectivamente pasó la verificación de eficiencia en al menos un período (guarda `any-audit-happened`). Esto replica el comportamiento del modelo original, donde `after-tax-income` y `fraud-detect-hist` solo se actualizan si la auditoría procedió

Esto evita:
- Penalizaciones múltiples por el mismo fraude
- Re-auditoría innecesaria de períodos ya revisados (dentro de la ventana)
- "Bolas de nieve" de auditorías acumuladas
- Acoplamiento de la secuencia aleatoria con la presencia de memoria institucional en estado base

---

## 7) Flujo del historial de ingresos y de períodos auditados

```
Cada tick, AL INICIO del tick (antes de la auditoría):
  income-history ← append [income, income-reported]
  audited-periods ← append false
  Si length(income-history) > institutional-memory:
    income-history ← sublist(income-history, -institutional-memory, length)
    audited-periods ← sublist(audited-periods, -institutional-memory, length)
```

- **FIFO sincronizado**: ambas listas se recortan en lockstep, manteniendo la correspondencia índice-a-índice entre dato y marca
- **Al inicio del tick (no al final)**: la captura se hace ANTES de `make-audit` para que el offset 0 de `income-history` contenga el par `[income, income-reported]` del período que se está auditando. Esto es lo que permite que `institutional-memory = 1` sea equivalente al modelo original
- **Deep copy**: se guarda una copia del par `[income, income-reported]` en el momento de la captura
- **`false` en audited-periods**: el slot recién agregado para el período actual entra con marca `false` (no auditado todavía); el `ask x [...]` al final del loop lo marca como `true` si la auditoría procedió

---

## 8) Resultados mostrados

### 8.1 Visuales en interfaz (sin cambios)
- Histograma doble (IR: `pct-income-report`, RA: `risk-aversion`)
- Gráfico de medias temporales (MPIR, MPAE, MRA)

### 8.2 Variables globales de medición (sin cambios)
- `global-audit-perc-eff`
- `PIAR_10000`, `PRA_10000`
- `SS_PIAR`, `SS_RA`
- `acum_prom_PIAR_ags`, `acum_prom_RA_ags` (desde tick 25000)
- `acum_delta_inc_real_inc_report` (desde tick 25000)
- `acum_frauds_detected`, `acum_frauds_perpretated`, `acum_frauds_perpretated_all_ags` (desde tick 25000)

### 8.3 Efectos esperados de la memoria institucional
- **Mayor detección**: al revisar más períodos, más fraudes totales detectados
- **Mayor fatiga**: auditores se desgastan más por contribuyente revisado
- **Penalidades mayores**: acumulación de multas de múltiples períodos → mayor castigo → mayor incentivo a reportar completo
- **Interacción con memoria social**: detecciones retrospectivas se comunican a vecinos como fraudes detectados en tick actual, potenciando el aprendizaje social
