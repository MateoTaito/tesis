# `Exper_chile_calibrado` N=30 — análisis y conclusiones

**Diseño:** `audit-rate 0.02`, `k∈{1,3,5,7,15}`, `noise 0`, `PF∈{1,5}`, 3 estrategias × 30 reps = 900 runs, 30k ticks.
**CSV:** `chile_n30.csv` (900 filas, 30 combos × 30, todo a step 30000). **Gráficos:** `n30_*.png` (6, 300 dpi, mean±std).
**Estadística:** Welch t por celda (n=30, gl≈58; |t|>2.0 ⇒ p<0.05, |t|>3.5 ⇒ p<0.001). Sin ANOVA factorial aún (pendiente para la tesis).

## 1. PIAR final (mean±std, N=30)

| estrategia | PF | k1 | k3 | k5 | k7 | k15 |
|---|---|---|---|---|---|---|
| income | 1 | 0.0002±0.0001 | 0.023±0.009 | 0.051±0.013 | 0.065±0.016 | 0.068±0.013 |
| income | 5 | 0.114±0.017 | 0.257±0.022 | 0.288±0.020 | 0.300±0.017 | 0.311±0.013 |
| random | 1 | 0.116±0.018 | 0.523±0.033 | 0.692±0.030 | 0.770±0.027 | 0.821±0.020 |
| random | 5 | 0.868±0.015 | 0.952±0.007 | 0.963±0.006 | 0.965±0.006 | 0.964±0.009 |
| strategic | 1 | 0.970±0.053 | 0.921±0.107 | 0.908±0.110 | 0.903±0.109 | 0.653±0.077 |
| strategic | 5 | 0.399±0.082 | 0.585±0.176 | 0.567±0.176 | 0.527±0.170 | 0.459±0.123 |

## 2. Contrastes k15 vs k1 (PIR)

| celda | diff | SE | t | veredicto |
|---|---|---|---|---|
| income PF1 | +0.068 | 0.0023 | +29.0 | *** + (×340 en relativo, piso→bajo) |
| income PF5 | +0.198 | 0.0038 | +51.8 | *** + |
| random PF1 | +0.705 | 0.0049 | +144 | *** + (el efecto más grande del estudio) |
| random PF5 | +0.096 | 0.0032 | +30.2 | *** + (luego meseta k5→k15: 0.963→0.964, ns) |
| strategic PF1 | −0.317 | 0.0171 | −18.5 | *** NEGATIVO (colapso k7→k15: 0.903→0.653) |
| strategic PF5 | +0.060 | 0.0270 | +2.2 | * + marginal, pero joroba: k3 0.585 → k15 0.459 (−0.126, p<0.01) |

## 3. MRA final — sube con k en 5/6 (el miedo responde; el reporte solo a veces)

income PF1 0.545→0.679 ***; income PF5 0.749→0.818 ***; random PF1 0.840→0.957 ***;
random PF5 0.989→0.998 *** (techo); strategic PF1 0.974→0.962 (baja leve pero *** por SE tiny);
strategic PF5 0.950→0.961 **. Desaparece la disociación MRA–PIR del régimen 20%.

## 4. Detección (tasa/tick, convención acum/30000 como en Exp_full_inst_mem)

income 0.68→1.13→1.27→1.32→1.29 (sube y satura, ambas PF); random 1.04→1.38→1.46→1.50→1.49
(sube y meseta k7); strategic PF1 1.18→1.28→1.22→1.25→1.16 (plano, std 0.07–0.16);
strategic PF5 1.42→1.45→1.45→1.41→1.21 (dip k15). Contraste con régimen 20% (caída −63..−71%):
a 2% de cobertura cada auditoría marginal vale más y la ventana no se satura igual.

## 5. Convergencia — ΔPIR medio (final − tick 10000)

income: −0.03..−0.05 (sigue cayendo lento a 30k); random PF1 k1 −0.096 (base aún colapsando),
k15 +0.166 (aún subiendo); random PF5 +0.18..+0.21 (AÚN SUBIENDO a 30k, no convergido);
strategic PF1 k1 +0.505 (subió medio punto desde 10k). **Conclusión metodológica:**
varias celdas no están en estado estacionario a 30k → la corrida definitiva debe ir a 50k con
ventana de medición 30k–50k, y el detector SS (umbral delta<1e-6) dispara en mesetas transitorias.

## 6. Veredicto H1–H5 (N=30)

- **H1** (`dPIR/dk>0`): **SOSTENIDA para random (ambas PF) e income (ambas PF), todas p<0.0001.
  RECHAZADA para strategic PF1 (negativa, p<0.0001) y matizada en strategic PF5 (joroba).**
  La memoria institucional sí eleva el cumplimiento — salvo bajo focalización estratégica con
  cobertura escasa, donde la memoria profunda es contraproducente. Esa es la interacción central.
- **H2** (ruido): **NO TESTEADA** (noise=0 en los 900 runs). Siguiente barrido.
- **H3** (PF modera): **CONFIRMADA, con signo dependiente de estrategia.** random: pendiente
  PF1 (+0.705) ≫ PF5 (+0.096) — memoria social larga deja menos que ganar (atenuación tal cual H3).
  income: PF5 (+0.198) > PF1 (+0.068) en absoluto — con base en piso, la memoria social larga
  potencia el rescate (matiz a registrar contra H3). strategic: PF1 colapso, PF5 joroba.
- **H4** (profunda→estratégica>aleatoria; superficial→equivalentes; ingreso peor):
  **PARCIAL.** "Ingreso siempre peor" ✓ en las 10 celdas k (0.0002–0.311 vs resto 0.116–0.970).
  El resto SE INVIERTE a cobertura 2%: k1 PF1 strategic 0.970 > random 0.116 ✓ pero
  k15 PF1 strategic 0.653 < random 0.821 ✗; PF5 strategic < random en TODO k
  (k1: 0.399<0.868; k15: 0.459<0.964). Con enforcement escaso, la focalización estratégica
  rinde peor que lo aleatorio — generaliza el crossover Canessa (que solo lo veía en PDF con PF5).
- **H5** (aleatoria peor con k alta): **RECHAZADA por segunda vez** (random k15>k1 en ambas PF,
  p<0.0001; detección también sube). Se archiva.

## 7. Hallazgo adicional — strategic a cobertura escasa es inestable

std PIR strategic 0.05–0.18 vs 0.003–0.03 en el resto (×10–30). Distribuciones:
PF1 k15 min 0.460–max 0.789 (colapso SISTEMÁTICO, mediana 0.656, no outliers);
PF5 k3 min 0.345–max 0.893 (dispersión total). La focalización por riesgo con pocos
audits es path-dependent: si los primeros audits aciertan, converge alto; si no, el score
persigue fantasmas y la ventana profunda amplifica el error. Esto merece su propia
subsección en la tesis (implicancia de política: targeting sofisticado exige piso de cobertura).

## 8. Qué falta (orden)

1. 50k ticks + ventana 30k–50k (convergencia, §5). 2. `noise {0.1,0.3,0.5}` (H2).
3. `audit-rate {0.01,0.05,0.10}` (sensibilidad). 4. ANOVA factorial `PIR ~ k×PF×estrategia`.
5. No tocar rama réplica. Pre-registrar 1–4 antes de correr.
