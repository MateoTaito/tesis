# Especificación: Experimento Exper_emu_paper

## Descripción General
Experimento para analizar la **interacción entre memoria social (period-frauds) y estrategia de selección de auditoría** en el modelo Tax-Evation con memoria institucional.

## Parámetros Fijos del Experimento

### Población y Auditoría
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `nr-tax-payers` | 500 | Número de contribuyentes en la simulación |
| `nr-auditors` | 20 | Número de auditores disponibles |
| `actual-audit-rate` | 0.20 | Tasa de auditoría (20% de contribuyentes auditados) |

### Impuestos y Sanciones
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `tax-rate` | 0.27 | Alícuota de impuesto (27%) |
| `penalty-rate` | 1.5 | Multiplicador de penalización por fraude detectado |

### Comportamiento de Contribuyentes
| Parámetro | Valor | Descripción |
|-----------|-------|-------------|
| `learning-rate` | 0.05 | Velocidad de aprendizaje social (5% ajuste por observación) |
| `initial-Risk-aversion` | 0.5 | Aversión al riesgo inicial (escala 0-1) |
| `treshold-influence-income` | 1.65 | Umbral de influencia del ingreso en decisión de fraude |

### Memoria Social
| Parámetro | Valores | Descripción |
|-----------|--------|-------------|
| `period-frauds` | 1, 5 | Número de períodos previos recordados por contribuyentes |

### Estrategia de Auditoría
| Parámetro | Valores | Descripción |
|-----------|--------|-------------|
| `tax-payer-audit-selection` | random, income-level, strategic | Método de selección de contribuyentes a auditar |

## Configuración de Ejecución
- **Repeticiones**: 3 (tres ejecuciones completas por combinación)
- **Duración**: 10,000 pasos
- **Tipo de reporte**: Final (runMetricsEveryStep = false)

## Métricas Registradas (al final del experimento)
1. `mean [pct-income-report] of tax-payers` - Ingreso promedio reportado (%)
2. `mean [risk-aversion] of tax-payers` - Aversión al riesgo promedio
3. `PIAR_10000` - Ingreso reportado promedio en tick 10000 (si existe)
4. `PRA_10000` - Aversión al riesgo promedio en tick 10000 (si existe)
5. `acum_frauds_detected` - Total de fraudes detectados
6. `acum_frauds_perpretated` - Total de fraudes cometidos
7. `acum_frauds_perpretated_all_ags` - Total de fraudes de todos los agentes
8. `SS_PIAR` - Estado estacionario del ingreso reportado
9. `SS_RA` - Estado estacionario de aversión al riesgo

## Combinaciones del Experimento
**Total de escenarios**: 3 × 2 = **6 combinaciones**

| # | Strategy | Period Frauds | Descripción |
|---|----------|---------------|-------------|
| 1 | random | 1 | Selección aleatoria, baja memoria social |
| 2 | random | 5 | Selección aleatoria, alta memoria social |
| 3 | income-level | 1 | Selección por ingreso, baja memoria social |
| 4 | income-level | 5 | Selección por ingreso, alta memoria social |
| 5 | strategic | 1 | Selección estratégica, baja memoria social |
| 6 | strategic | 5 | Selección estratégica, alta memoria social |

## Preguntas de Investigación
1. ¿Cómo interactúan la memoria social y la estrategia de auditoría?
2. ¿Hay estrategias más efectivas bajo ciertos niveles de memoria social?
3. ¿Varía la aversión al riesgo según la combinación de memoria × estrategia?

## Notas Importantes
- Los parámetros están explícitamente especificados en el XML del experimento
- La reproducibilidad está garantizada al fijar todos los valores
- El experimento no varía `institutional-memory` ni `audit-noise` (mantiene valores por defecto: 1 y 0 respectivamente, que tras el fix de 2026-07-06 son **equivalentes al modelo ABM_Original** bit-a-bit bajo misma seed)
- Cada simulación dura exactamente 10,000 ticks

## Cambios Realizados (2026-05-19)
- Agregados todos los parámetros como `<enumeratedValueSet>` explícitos
- Documentación de especificación completa
- Confirmación de valores: todos coinciden con especificación solicitada

## Cambios Realizados (2026-07-06)
- Sincronización de este documento con el XML efectivo del experimento (3 repeticiones / 10,000 pasos)
- Nota sobre equivalencia bit-a-bit con `ABM_Original.nlogo` bajo `institutional-memory = 1, audit-noise = 0` (validado con seeds 42, 7, 100)
- Resultados pre-fix movidos a `Resultados_experimentos/Exp_fallidos_post_fix/`
