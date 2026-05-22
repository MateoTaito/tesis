# Análisis Comparativo: ABM_Original vs Tax-Evation con institutional-memory=1

## Conclusiones Principales

### ❌ NO SON EQUIVALENTES

**Los modelos ABM_Original y Tax-Evation_1_2 con institutional-memory=1 NO producen resultados equivalentes.**

---

## Evidencias Encontradas

### 1. Anomalías en ABM_Original

El modelo ABM_Original muestra valores extremadamente anómalos en la variable `mean [risk-aversion] of tax-payers`:

| Strategy | Period | Run 1 | Run 2 | Run 3 | Media | Std Dev |
|----------|--------|-------|-------|-------|-------|---------|
| random | 1 | 0.8517 | 0 | 0 | 0.284 | 0.492 |
| random | 5 | 0 | 0 | 0 | 0.000 | 0.000 |
| **income-level** | **1** | **2911** | **3** | **10000** | **4305** | **5142** |
| income-level | 5 | 0.4276 | 0.7511 | 0 | 0.393 | 0.377 |
| strategic | 1 | 0 | 0 | 0 | 0.000 | 0.000 |
| **strategic** | **5** | **0** | **0** | **4655** | **2328** | **3292** |

**Outliers detectados:**
- income-level × P=1, Run 2: 2911.00
- income-level × P=1, Run 3: 10000.00
- strategic × P=5, Run 3: 4655.00

Estos valores son imposibles para una métrica que debería oscilar entre 0 y 1 (es la media de risk-aversion de los agentes).

### 2. Estabilidad de Tax-Evation

El modelo Tax-Evation_1_2 muestra valores consistentes y razonables:

| Strategy | Period | Run 1 | Run 2 | Run 3 | Media | Std Dev |
|----------|--------|-------|-------|-------|-------|---------|
| random | 1 | 0.3925 | 0.3934 | 0.3909 | 0.3920 | 0.0013 |
| random | 5 | 0.3943 | 0.3965 | 0.3932 | 0.3947 | 0.0017 |
| income-level | 1 | 0.3932 | 0.3934 | 0.3930 | 0.3932 | 0.0002 |
| income-level | 5 | 0.3935 | 0.3948 | 0.3919 | 0.3934 | 0.0014 |
| strategic | 1 | 0.3937 | 0.3945 | 0.3942 | 0.3942 | 0.0012 |
| strategic | 5 | 0.3944 | 0.3928 | 0.3927 | 0.3933 | 0.0017 |

**Características:**
- Rango: 0.3909 - 0.3965 (razonable)
- Varianza muy baja entre repeticiones (~0.0002 a 0.0017)
- Comportamiento consistente y predecible

---

## Análisis del Problema

### Causa Raíz

Del análisis exhaustivo del código, se identificó que **cuando institutional-memory=1, Tax-Evation aún ejecuta código diferente al original**:

1. **Diferencia en Timing**: 
   - Tax-Evation guarda `income-history` DESPUÉS de `make-audit`
   - Pero `make-audit` intenta acceder a `income-history` que está vacío

2. **Lógica de Auditoría Diferente**:
   - ABM_Original: Audita income/income-reported ACTUAL del agente
   - Tax-Evation: Intenta auditar datos históricos (que no existen en primer tick)
   
3. **Período 0 vs Período 1**:
   - ABM_Original: Audita el período actual (period-offset implícito)
   - Tax-Evation: Usa period-offset=0 que accede a income-history[0] (vacío)

### Por Qué ABM_Original tiene Anomalías

El análisis de código sugiere que los valores extremos en ABM_Original podrían ser:
- **Bug en el modelo original**: Posible desbordamiento de variables
- **Corrupción de datos**: Errores en la grabación de resultados
- **Comportamiento no documentado**: Feature/bug que sale de rango

Los valores > 1000 para una métrica de 0-1 sugieren **error grave en el cálculo o grabación**.

---

## Impacto de institutional-memory=1

Cuando institutional-memory=1 se establece en Tax-Evation:
- ✅ El loop de auditoría se ejecuta 1 sola vez (correcto)
- ❌ Pero sigue usando income-history en lugar de income actual
- ❌ Sigue ejecutando lógica de "multi-período" (solo 1 período, pero estructura diferente)

**Conclusión**: institutional-memory=1 NO replica el comportamiento original porque la estructura subyacente es diferente.

---

## Recomendaciones

### Opción 1: Verificar ABM_Original
- Revisar si los valores extremos (2911, 10000, 4655) son correctos
- Ejecutar ABM_Original nuevamente con logging habilitado
- Verificar si hay bugs en el modelo original

### Opción 2: Implementar Modo Compatible
Agregar lógica especial en Tax-Evation para cuando institutional-memory=1:

```netlogo
if institutional-memory = 1 [
  ; Use original ABM_Original logic directly
  ; Bypass income-history system
  ; Use current agent's income/income-reported
]
```

### Opción 3: Validar Ambos Modelos
- Ejecutar ambos con identical.seed para análisis detallado
- Agregar logs en cada paso de auditoría
- Comparar line-by-line los valores intermedios

---

## Archivos Generados

```
Comparacion_ABM_vs_TaxEvation/
├── comparison_line_with_anomalies.png     (Visualización con outliers)
├── comparison_line_zoomed.png             (Visualización sin outliers)
├── comparison_table.png                   (Tabla de comparación)
├── comparison_boxplot.png                 (Distribuciones)
├── comparison_grouped_bars.png            (Barras agrupadas)
├── comparison_difference_heatmap.png      (Heatmap de diferencias)
├── summary_comparison.csv                 (Resumen estadístico)
├── abm_original_raw_data.csv             (Datos crudos ABM)
├── taxevation_raw_data.csv               (Datos crudos Tax-Evation)
└── comparison_analysis_final.py          (Script de análisis)
```

---

## Veredicto Final

**Status: NO EQUIVALENTE**

- **ABM_Original**: Datos con anomalías graves (outliers > 1000)
- **Tax-Evation (inst_mem=1)**: Datos consistentes (~0.39)
- **Implicación**: No se pueden usar los resultados de ABM_Original para validar Tax-Evation

**Próximo Paso Recomendado**: Investigar la causa de los outliers en ABM_Original antes de continuar.
