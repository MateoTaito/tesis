# AGENTS.md — Tesis Magíster: ABM Tax Evasion con Memoria Institucional

## Projecto

Tesis de magíster. Simulaciones NetLogo de evasión tributaria (modelo basado en agentes).
- **Modelo base**: `ABM_Original.nlogo` (modelo de Canessa)
- **Modelo de trabajo**: `ABM_TESIS_CHANGES.nlogo` — añade **memoria institucional** (auditores pueden revisar períodos pasados)
- **Repo**: `git@github.com:MateoTaito/tesis.git` (branch `main`)
- **Sin reglas estrictas de contribución** — es investigación académica, se itera libremente

## NetLogo

Instalado en `/home/MTS/local/netlogo` (v6.4.0, Java 25).

| Comando | Uso |
|---------|-----|
| `netlogo` | Abre la GUI. Opcional: `netlogo modelo.nlogo` |
| `netlogo-headless` | Ejecuta BehaviorSpace sin UI. Requiere `--model`, `--setup-file`/`--experiment`, y `--table` o `--spreadsheet` |

### Ejemplo headless

```bash
netlogo-headless \
  --model "ABM_TESIS_CHANGES.nlogo" \
  --setup-file experiment.xml \
  --experiment "my-experiment" \
  --table results.csv
```

### Experimentos existentes

- `Especificacion_Exper_emu_paper.md` — especificación del experimento `Exper_emu_paper` (interacción memoria social × estrategia de auditoría)
- Los XML de experimentos se guardan dentro de los `.nlogo` o como archivos `.xml` separados

## Modelo: Tax-Evation con Memoria Institucional

### Agentes
- **tax-payers**: contribuyentes que deciden cuánto ingreso reportar (`pct-income-report`)
- **auditors**: fiscalizadores con eficiencia imperfecta y memoria histórica

### Feature clave: memoria institucional
- `institutional-memory` (1–15): cuántos períodos hacia atrás pueden auditar
- `audit-noise` (0–0.5): degradación de detección en períodos lejanos
- Cada contribuyente mantiene `income-history` (FIFO) y `audited-periods` (ventana deslizante sincronizada: marca por `institutional-memory` ticks, no permanente)
- Ver `Especificación ABM_ Tax-Evation_1_2_con_memoria_institucional.md` para detalle completo

### Métricas principales
- `PIAR_ticks`: serie temporal de % ingreso reportado
- `RA_ticks`: serie temporal de aversión al riesgo
- `acum_frauds_detected`, `acum_frauds_perpretated`: fraudes detectados/cometidos
- `SS_PIAR`, `SS_RA`: ticks donde se alcanza pseudo estado estacionario

## Análisis de resultados

Scripts Python en `Resultados_experimentos/`:
- `plot_interaction_analysis.py` — genera gráficos de interacción (líneas, barras, heatmap, facetas)
- `plot_interaction_analysis_3runs.py` — variante para múltiples repeticiones
- Requiere: `pandas`, `matplotlib`, `seaborn`, `numpy`
- Los datos de entrada son CSV de BehaviorSpace (6 filas de metadata, datos desde fila 7)

### Re-generar gráficos

```bash
cd Resultados_experimentos
python3 plot_interaction_analysis.py
```

## Documentos de referencia

| Archivo | Contenido |
|---------|-----------|
| `Especificación ABM_ Tax-Evation_1_2_con_memoria_institucional.md` | Especificación completa del modelo (agentes, variables, flujo de ticks) |
| `Especificacion_Exper_emu_paper.md` | Parámetros del experimento de interacción |
| `vODD_docs.pdf` | Protocolo ODD del modelo |
| `Tax-Evation_ODD_Optional.svg` | Diagrama visual ODD |
| `Resultados_experimentos/ANALYSIS_SUMMARY.txt` | Resumen de hallazgos de experimentos |

## Notas para agentes

- **No hay tests automatizados** — la verificación es visual (GUI) o por análisis de resultados CSV
- **El modelo tarda miles de ticks** en converger; experimentos largos son normales (50k+ steps)
- **Los experimentos se definen en XML** compatible con BehaviorSpace (DTD `behaviorspace.dtd`)
- **Los CSV de salida tienen 6 filas de metadata** antes de los datos — los scripts de análisis las saltan
- **No modificar `ABM_Original.nlogo`** — es la referencia base, todo cambio va en `ABM_TESIS_CHANGES.nlogo`
- **Equivalencia bit-a-bit**: con `institutional-memory=1, audit-noise=0` (defaults del slider), `ABM_TESIS_CHANGES.nlogo` produce **resultados idénticos** a `ABM_Original.nlogo` bajo la misma seed (validado para seeds 42, 7, 100 en 1000 ticks con 3 estrategias). Esto se logra porque (a) la captura de historial se hace al inicio de `go` antes de `make-audit` (offset 0 = período actual) y (b) la guarda `any-audit-happened` evita que el `ask x [...]` se ejecute cuando el auditor no pasó la verificación de eficiencia, replicando exactamente la guarda del modelo original
- **Estructura clave del fix** (2026-07-06): la captura de historial es `ask turtle w` por who-number (no `ask tax-payers`) para evitar consumo aleatorio del agentset; la auditoría está envuelta en `if any-audit-happened [...]` para mantener la guarda original
