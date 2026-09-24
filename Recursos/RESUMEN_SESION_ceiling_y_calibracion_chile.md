# Recordatorio de sesión — Ceiling effect y calibración a Chile

**Fecha:** 2026-09-24
**Tema:** ¿Por qué H1 no se ve con el experimento actual y cómo alejar el base del techo calibrando a Chile sin caer en p-hacking?

## 1. Diagnóstico (con números literales)

- Base actual (`k=1, noise=0, audit-rate 0.20, 20 auditores/500 contribuyentes`) está en techo:
  - `random PF5 k=1: PIR 0.994±0.003`, `strategic PF5 k=1: 0.997±0.0003`, `MRA ~0.99`.
  - Headroom: `1.000-0.994 = 0.006`. MDE con N=3 ≈ `0.005`. Un H1 de "+0.01" es indetectable por construcción.
- Lo único observable con ese base son caídas (asimetría de rango restringido):
  - `income PF1 0.217→0.052 (−76%, p<0.001)`, `detection_rate random PF1 9.92→3.38/tick (−66%, p<0.001)`.
- Réplica Canessa: **SÍ reproduce**.
  - Bit-a-bit bajo misma seed (Validation 1000 steps, seeds 42/7/100): ej. seed 42 random `0.5978588931629338/0.8378434305378016` idéntico 16 decimales.
  - Patrón 3×2: PF1 `strategic−random PIR +0.110 (p<.0001)` vs Canessa `+0.0957 (p<.0001)`; PF5 `−0.018 (ns, p≈0.07)` vs Canessa `+0.0034 (p=0.063 ns)` — mismo veredicto.
- Régimen actual ≈ 20–80× la presión SII real:
  - Modelo: `20/500 = 4%`, `audit-rate 0.20` = 100 auditorías/tick = 20% auditado cada período.
  - SII PGCT 2026: dotación 4.913, fiscalizadores 2.103, 5.891 auditorías + 14.491 RC vs millones de RUTs (<1% cobertura), 67% horas al 2.8% de contribuyentes.

## 2. Veredicto H1–H5 con datos actuales (`FullInstMem`, N=3, 30k, noise=0)

- **H1** (`dPIR/dk>0`, mayor con PF alta): RECHAZADA. Pendientes ≤0 en 6/6 celdas. Único tramo positivo (random PF1 1→5, +0.068, p<0.01) se revierte 5→15 (−0.036, p<0.01).
- **H2** (ruido modera): NO TESTEABLE — `audit-noise` siempre 0.0 en los 90 runs.
- **H3** (PF corta refuerza focalizadas; PF larga atenúa): RECHAZADA en signo, parcial en magnitud. Con PF1, k profunda debilita (income −76%); con PF5 el daño se atenúa (−16%). Atenuación sí, refuerzo no.
- **H4** (profunda→estratégica>aleatoria; superficial→equivalentes; ingreso peor): PARCIAL. Ranking `strategic≈random≫income` holds siempre (income 0.05–0.38 vs resto 0.93–0.99, p<0.001). Pero "superficial→equivalentes" solo vale PF5 (diff 0.002 ns); PF1 k=1 diff +0.089 (p<0.01). Brecha se achica con k, no se agranda.
- **H5** (k alta→aleatoria peor que k nula): RECHAZADA en PIR (random PF1 k15 0.929 vs k1 0.897, mejor; PF5 plano ns), CONFIRMADA en mecanismo (detección 9.9→3.4/tick, p<0.001). Más miedo (MRA 0.85→0.94) sostiene cumplimiento pese a menos cobertura.
- Disociación clave: `dMRA/dk>0` mientras `dPIR/dk≤0`.

## 3. Criterio científico: recalibración sí, tuning no

- Mantener rama réplica Canessa intacta (validez interna).
- Justificar escenario Chile ex-ante con PGCT/SII/INE/Ley 21.713, no con los CSV.
- Pre-registrar ventana de observabilidad ("H1 no testeable bajo audit-rate 0.20 por techo; se testea en régimen calibrado PIR~0.5-0.6").
- Reportar ambos (el nulo Canessa es resultado).
- Sensibilidad en rango, no punto único. N≥30, 30k–50k ticks, semillas dispersas, ANOVA `PIR ~ k×PF×estrategia`.
- Ojo código: `nr-auditors` vs `actual-audit-rate` NO intercambiables. `audit-rate` = cobertura horizontal; `nr-auditors` = reparto + fatiga intra-tick (`nr-done −=0.05` por período y por asignado). Mover cobertura; fijar dotación para carga constante.

## 4. Experimentos pendientes (estado 2026-09-24)

- `k∈{1,3,5,7,15}`: faltan 3,7; sobra 10. `ruido∈{0,0.1,0.3,0.5}`: falta todo.
- N=3 → N≥30/100. 10k-final vs 25k–30k-promedio: unificar a 25k–30k (o 30k–50k si baja enforcement).
- Experimento `memoria_institucional_x_social` no existe en el .nlogo.
- Preguntas abiertas al tesista: ¿dos ramas o migración total? ¿mover audit-rate, nr-auditors o ambos? ¿tasa objetivo 2%/5%/rango 2–10%?

## 5. Archivos fuente de estos números

- `Resultados_experimentos/Exp_post_fix/exp_emu_paper_postfix.csv` (18 runs, 10k) + `summary_mean_pir/pra.csv`
- `Resultados_experimentos/Exp_full_inst_mem/full_inst_mem_30k.csv` (72 runs, 30k) + `summary_mean_pir/pra/detection_rate.csv`
- `Resultados_experimentos/Comparacion_ABM_vs_TaxEvation/ANALISIS_COMPARATIVO.md` (equivalencia bit-a-bit)
- `Resultados_experimentos/Original_exp.csv` (ABM_Original)
- `Papers/(291225) Paper_Tax Compliance...Canessa...pdf` Sec. 5 (MRA/PIAR/PDF/CDI + ANOVAs)
- `Recursos/templateLatex/templateLatex/Chapters/Hipotesis.tex` (H1–H5, VI/VD)
- `Recursos/SII_PGCT_2026.pdf`, `Recursos/respuesta_scibot.txt`
