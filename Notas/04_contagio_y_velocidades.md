# 04 — Contagio, espacio y velocidades (14 oct 2026)

## Tesis central: el fraude no se transmite en este modelo

Los vecinos **no observan evasión exitosa**. Los únicos canales sociales
(`ABM_TESIS_CHANGES.nlogo:182-237`, vecindad de Moore vía `tax-payers-on neighbors`) son:

1. `weights-income`: compara ingresos **brutos** de lotería, no evasión.
2. `weights-sanction`: +1 si un vecino fue **detectado** (70% de enterarse).

Un evasor no detectado es invisible; si lo detectan, **disuade** a sus vecinos
(lo opuesto a la cascada). La "cascada" observable es deriva global por ausencia de
disuasión, no contagio vecino-a-vecino. El experimento `seed-fraud?` lo confirmó:
un paciente cero solo deja un punto rojo estático.

## Qué interacciones dependen del espacio

**Solo una**: la influencia social en `risk-aversion` (hasta 8 vecinos de Moore).
Todo lo demás es mean-field: auditores sin posición (`hide-turtle`, reparto round-robin
global), ingresos sin correlación espacial, detección/penalidad/historiales por agente.
Segundo orden: la densidad (`nr-tax-payers` vs 900 parches) regula el n° de vecinos
(señal más ruidosa a baja densidad; la influencia se promedia, no se sesga).
Código muerto con potencial: `nr-neighbors-audited` / `nr-neighbors-fraud-detected`
(`:98-101`) se calculan por vecindario pero el reporter los ignora — gancho natural
si se quiere que "ver auditar al vecino" disuada directamente.

## Velocidades: qué sirve y qué no

- **"Velocidad de expansión del fraude": NO aplicable.** Sin mecanismo de transmisión,
  hablar de frente de contagio inventa un mecanismo. Requiere extensión teórica
  (canal de imitación, p. ej. switch `imitate-evaders?`): decisión pendiente, es cambio
  de modelo para la tesis, no parámetro.
- **"Velocidad de la influencia auditora": SÍ, redefinida como tasa de refresco.**
  La disuasión tiene alcance (1 salto), persistencia (PF auditorías ≈ PF/audit-rate ticks)
  e intensidad (auditorías/tick × eficiencia). Formalización útil: balance deriva vs
  detección `p_eff ≈ (1-ra)/(5·ra)` — de ahí sale el feedback desestabilizante
  (menos ra → deriva más rápida → se necesita más fiscalización → colapso global).
  Es un tipping mean-field, no una ola.
- **Encuadre alternativo**: explore-exploit con presupuesto (strategic = explotación
  codiciosa de estimación ruidosa; con poco presupuesto gana la exploración/random).
  Literatura de bandits, sin velocidades inexistentes.

## Origen de la biestabilidad strategic × cobertura escasa (19 oct, N=10)

Disección con 160 runs (`Exp_phase_transition/plot_bistability.py`):

- Random es determinista en las 8 celdas (bandas apretadas, PF1 abajo / PF5 arriba).
- Strategic PF1 0.02: 9/10 en techo + 1 escape (0.747). Lock-in malo raro (~10%).
- Strategic PF5 0.02: 1/10 en techo; valores **continuos 0.27–0.94 sin clusters**:
  indeterminación, no dos atractores. El umbral "techo" (PIR≥0.9) es convencional.
- Lock-in temprano: r(PIAR_10000, PIR_final) +0.65…+0.86 en strategic — el destino
  se decide antes del tick 10k.
- Cobertura acompaña (r=+0.95) pero **no determina** (a cobertura 0.65–0.72 el PIR va
  de 0.07 a 0.53; es en parte consecuencia). Detección ortogonal al PIR (r=+0.28):
  escala con volumen (6→16/tick), no con cumplimiento.
- Evidencia de concentración vs dispersión: random PF5 0.02 detecta 6.2/tick → PIR
  0.925; strategic detecta 8.5/tick → PIR 0.598. Mismo orden de volumen, resultado
  opuesto: importa **dónde** caen las señales (cobertura recordada 0.921 vs 0.823).
- PRA y PIR acoplados a 50k (r=+0.93): colapsan juntos.

Síntesis: targeting codicioso sobre scores ruidosos al inicio → rotación virtuosa
(lock-in alto) o caza-fantasmas con señales redundantes (lock-in bajo); PF5 alarga la
memoria de esas señales redundantes. Exclusivo de strategic × cobertura escasa.

## Receta de régimen pro-colapso global (no ola; vigente)

`start-all-honest?` ON + `visual-fraud-spread?` ON, initRA 0–0.1, learning-rate 0.5–1.0,
PF=1, threshold 10, audit-rate 0.01, pocos auditores, `random`, k=1/noise=0, 500 txps.
