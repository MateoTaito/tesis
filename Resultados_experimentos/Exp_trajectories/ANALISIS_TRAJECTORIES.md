# Trayectorias a tasa 0.02 — análisis (40 runs × 50k ticks, N=10 por celda)

**Diseño:** `Exp_trajectories/trajectory.xml` — solo `audit-rate 0.02`,
{random, strategic} × PF {1,5} × 10 reps, 50k ticks, `runMetricsEveryStep=true`
(PIR, PRA, cobertura). CSV: `trajectory_50k.csv` (2.000.040 filas + header, 321MB).
Figuras: `traj_*.png` (4). Script: `plot_trajectories.py`. Corrida: 25m13s, 9 threads.

## 1. Espaguetis PIR (todas las réplicas)

- **random PF1**: las 10 caen juntas al piso ~0.1. Colapso determinista.
- **random PF5**: las 10 suben juntas a ~0.9. Recuperación determinista.
- **strategic PF1**: las 10 caen a ~0.4 (tick 3–5k) y **todas despegan** en tiempos
  dispersos (~8k–25k); 9/10 en techo a ~35k, 1 rezagada subiendo (0.85 a 50k).
- **strategic PF5**: caen a ~0.35–0.45; despegues dispersos ~20k–45k+; a 50k hay
  2–3 planas abajo (~0.24–0.32) y el resto subiendo a ritmos distintos.

## 2. Dispersión entre réplicas std(t): ¿cuándo se separan?

| celda | std cruza 0.10 (sostenida) | std final | forma |
|---|---|---|---|
| random PF1/PF5 | nunca | 0.01–0.02 | plana |
| strategic PF1 | ~21.700 | 0.04 | sube a pico ~0.13 (25k) y **baja**: convergencia en curso |
| strategic PF5 | ~25.200 | 0.29 | **sube monótona, sin cerrar** |

Primeros 3000 ticks: indistinguibles (todas cayendo). La divergencia es **tardía**,
pero el ranking a 10k predice el destino (r=+0.65…+0.86): diferencias pequeñas
tempranas que se amplifican. Semilla fija el orden, no el destino visible.

## 3. Pendientes en últimos 5k ticks (por 1000 ticks)

random PF1 ≈ 0 (piso convergido); random PF5 +0.0013 (sube lento);
strategic PF1 una rezagada +0.0139 (llegaría al techo con ~15k ticks más);
strategic PF5 hasta +0.0392, una plana-negativa (−0.001): varias a mitad de subida.

## 4. Interpretación (revisión de la "biestabilidad")

- **PF1 = un atractor + tiempos de despegue dispersos**: la dispersión es
  transitoria y se está cerrando (std en baja). El run 0.747 no es otra cuenca,
  es el más lento.
- **PF5 = despegues tan dispersos que a 50k coexisten regímenes**: con estos datos
  **indistinguible** entre biestabilidad genuina y transitorio ultra-lento.
  Se necesitan 100k+ ticks o test de pendiente por run (hecho: mixto).
- La "distribución uniforme" 0.27–0.94 es compatible con una distribución ancha de
  tiempos de despegue, no exige dos cuencas. Cuidado con sobre-interpretar el N=10.
- Mecanismo del despegue = la rotación del targeting completa cobertura suficiente;
  por qué PF5 lo retrasa/dispersa más sigue abierto (caza-fantasmas con señales
  redundantes vs rotación lenta). Requiere historiales de auditoría por agente
  (exportación a nivel agente, trabajo futuro).

## 5. Cruce con el experimento de medias

Las trayectorias reconcilian todo: el barrido 10k fotografió la caída común (~0.4);
a 50k strategic PF1 ya despegó (medias altas) y strategic PF5 está a mitad de un
proceso con tiempos de despegue de 20k–45k+. El "umbral 0.04" del barrido era el
punto donde, a 10k, la rotación ya había completado a tasas altas pero no a bajas.
