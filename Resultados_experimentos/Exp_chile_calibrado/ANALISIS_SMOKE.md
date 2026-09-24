# Smoke test `Exper_chile_calibrado` — 1 rep/celda, 30k ticks, N=1 (SIN significancia)

**Fecha:** 2026-09-24. **Diseño:** `audit-rate 0.02`, `k∈{1,3,5,7,15}`, `noise 0`, `PF∈{1,5}`, 3 estrategias = 30 runs.
**Archivo:** `chile_smoke.csv` (formato tabla BehaviorSpace habitual, 6 filas metadata).
**Advertencia:** sin seed fija, cada celda trae seed distinta → celda confunde tratamiento + seed. Todo lo de abajo es lectura direccional, no contraste.

## PIAR final (30k) por celda — N=1

| estrategia | PF | k=1 | k=3 | k=5 | k=7 | k=15 | pendiente k1→k15 |
|---|---|---|---|---|---|---|---|
| random | 1 | 0.131 | 0.539 | 0.711 | 0.786 | 0.798 | **+0.667** |
| random | 5 | 0.877 | 0.933 | 0.962 | 0.973 | 0.961 | +0.084 |
| income | 1 | 0.0005 | 0.024 | 0.046 | 0.062 | 0.069 | +0.069 |
| income | 5 | 0.108 | 0.242 | 0.289 | 0.295 | 0.334 | +0.226 |
| strategic | 1 | 0.904 | 0.995 | 0.997 | 0.911 | 0.682 | −0.222 (no monótona) |
| strategic | 5 | 0.307 | 0.418 | 0.453 | 0.472 | 0.428 | +0.121 (dip en k15) |

## MRA final (30k)

| estrategia | PF | k=1 → k=15 |
|---|---|---|
| random | 1 | 0.824 → 0.952 (+) |
| random | 5 | 0.988 → 0.999 (+) techo |
| income | 1 | 0.557 → 0.683 (+) |
| income | 5 | 0.743 → 0.822 (+) |
| strategic | 1 | 0.970 → 0.962 (plano) |
| strategic | 5 | 0.930 → 0.961 (+) |

## Detección (`acum_detected/5000` = tasa por tick, ventana 25k–30k)

| estrategia | PF | k1 / k3 / k5 / k7 / k15 por tick |
|---|---|---|
| random | 1 | 6.31 / 8.24 / 8.82 / 9.08 / 8.89 (sube y meseta; régimen viejo: 9.92→3.38 caída) |
| random | 5 | 6.08 / 8.31 / 8.70 / 8.98 / 8.88 |
| income | 1 | 4.34 / 6.96 / 7.46 / 7.43 / 7.81 (sube; viejo: 6.31→2.32 caída) |
| income | 5 | 4.03 / 6.63 / 7.78 / 7.83 / 7.87 |
| strategic | 1 | 8.23 / 6.55 / 6.84 / 7.73 / 7.38 (plano ruidoso) |
| strategic | 5 | 8.76 / 9.18 / 8.47 / 8.74 / 7.45 |

Nota: `detected/perpretated > 1` en k profunda (ej. random PF1 k15: 44453/33116=1.34) es el mecanismo esperado:
la detección tira de historial (agente cumplidor hoy, condenado por fraude pasado), no es bug.

## Anomalías a seguir con N≥30 (no concluir con N=1)

1. **strategic PF1 k15 0.682** (viene de 0.997 en k5): caída −0.315. ¿Mecanismo real (sobre-focalización + fatiga k profunda +
   cobertura 2%) o seed mala? `perpretated` k15=45514 vs k5=35059 acompaña la caída (más fraude, menos reporte).
2. **Detector SS dispara temprano** en varias celdas (SS_PIAR=95, 107, 133 con PIAR aún moviéndose entre 10k y 30k,
   ej. random PF1 k1: PIAR_10000 0.205 → final 0.131). Confirma el sesgo advertido en la lámina: con enforcement bajo
   la convergencia es lenta y el umbral (`delta<1e-6`) marca mesetas transitorias. Revisar ventana de medición (30k–50k).
3. **Piso en income PF1 k1 (PIR 0.0005)**: floor effect simétrico al ceiling anterior — el rango audit-rate {0.01..0.10}
   deberá calibrar para no quedarse pegado al piso en esa celda.

## Lectura vs régimen anterior e hipótesis (direccional, N=1)

- **Techo roto: SÍ.** Base k1: 0.0005–0.904 (nuevo) vs 0.217–0.997 (viejo). Headroom restaurado salvo random PF5/strategic PF1 altos.
- **H1 (`dPIR/dk>0`): pasa de rechazada a sostenida en signo en 5/6 celdas** (todas menos strategic PF1 por anomalía 1).
- **H3 (PF modera):** random: pendiente PF1 (+0.667) ≫ PF5 (+0.084) — con PF larga hay menos que ganar (techo parcial);
  income: PF5 (+0.226) > PF1 (+0.069) en absoluto (pero ×140 en relativo desde 0.0005). Interacción existe, signo depende de estrategia.
- **H4 (ranking):** income siempre peor ✓ (0.0005–0.334 vs resto 0.13–0.997). Pero `strategic>random` SE ROMPE en PF5 k1:
  strategic 0.307 < random 0.877 — con cobertura 2% y memoria social larga, aleatoria supera a estratégica (eco del crossover
  Canessa en PDF, donde random superaba a strategic en detección con PF5). En PF1 k1 se mantiene (0.904 > 0.131).
- **H5 (aleatoria peor con k alta): rechazada otra vez en PIR** (random k15 > k1 en ambas PF). En detección ya no hay colapso:
  la tasa por tick SUBE o meseta con k (contrario al régimen 20%, donde caía −66%). A 2% de cobertura cada auditoría marginal
  vale más y no se satura `audited-periods` igual.
- **MRA–PIR:** ahora se mueven juntos (ambos suben con k) — desaparece la disociación del régimen 20%. Consistente:
  sin techo, el miedo se traduce en reporte.

## Siguiente paso

Subir a N≥30, ticks 30k–50k (revisar ventana por anomalía 2), luego `audit-rate {0.01,0.05,0.10}` y `noise {0.1,0.3,0.5}`.
No tocar rama réplica. Pre-registrar antes de correr.
