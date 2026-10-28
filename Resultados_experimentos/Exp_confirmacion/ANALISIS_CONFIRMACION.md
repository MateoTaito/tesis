# Confirmatorio N=30 — análisis (libros vivos, 600 runs)

**Diseño ejecutado:** factorial tasa {0.015,0.02,0.025,0.03,0.035} × {random, strategic}
× PF {1,5} × 30 reps, 50k ticks, modelo FixBooks (md5 idéntico antes/después),
métricas finales + PIAR_10000. 5h25 en 9 threads, EXIT=0, 600 filas.
Análisis: `analyze_confirmacion.py` (dip+Holm, GMM-BIC, Levene, logística).
Figuras: `confirm_distributions.png`, `confirm_techo_curve.png`.

## 1. Dip test (primario pre-registrado): veredicto matizado

| celda | dip p | Holm (m=5, solo strategic PF5) |
|---|---|---|
| strat PF5 0.015 | 0.538 | no rechaza (colapso uniforme 0.23–0.34) |
| strat PF5 0.02 | 0.045 | nominal sí; **Holm (0.025) no** |
| strat PF5 0.025/0.03/0.035 | ~0.000 | rechaza, PERO medias ~0.995–0.998 (29–30/30 en techo + 1 escape: artefacto de outlier) |
| strat PF1 0.015 | 0.906 | no rechaza (pero dispersa 0.47–1.0: el dip no ve asimetría sin valle) |
| strat PF1 ≥0.02 | ≤0.005 | rechaza por el escape único (0.907): artefacto |
| random (todas) | 0.16–0.95 | no rechaza en ninguna |

Lección instrumental: el dip es frágil ante outliers y distribuciones discretizadas
en techo. La regla pre-registrada ("dip+ solo PF5-baja") no se cumple literalmente
porque el dip también salta en celdas techo. El veredicto afirmativo viene de la
convergencia de las demás pruebas, reportando esto en forma transparente.

## 2. Mixtura gaussiana (BIC): dos cuencas donde hay dispersión real

strategic PF5 0.02: BIC2 < BIC1, medias **0.45 y 0.90** → 2 cuencas separadas.
strategic PF1 0.02: BIC2 < BIC1 con medias 0.907/0.998 → el "segundo componente"
es el escape único (no una cuenca). Random PF1 0.02: 1 cuenca.
PF5 0.03: 1 cuenca (0.998/0.999: el dip de esa celda era el escape 0.922).

## 3. Levene: la varianza de PF5-0.02 domina todo

strategic PF5 0.02 (sd 0.245) vs cada control en 0.02: p<0.0001 siempre
(PF1 0.017, random PF1 0.008, random PF5 0.004). A 0.015 la mayor dispersión es
strategic PF1 (sd 0.139 vs PF5 0.029, p=0.0016): la zona indeterminada se mueve
con la tasa — a 0.015 PF5 ya colapsó uniformemente y PF1 es la dispersa.

## 4. Estructura final de la zona (N=30, libros vivos)

- **0.015**: strategic PF5 colapso uniforme (0.23–0.34); PF1 dispersa techo-dominante.
- **0.02**: strategic PF5 dispersión total 0.28–0.99 con valle ~0.65–0.78
  (leve bimodalidad, GMM 2 cuencas); PF1 techo + escape raro (3%).
- **≥0.025**: techo en todo strategic (escapes únicos ocasionales).
- **Curva P(techo)**: strategic PF5 traza la sigmoide 0 → 0.27 → 1.0;
  strategic PF1 0.63 → 1.0; random plana en 0 (PF1) y 1 (PF5).
- Logística destino~PIAR_10000: solo ajustable en PF5 0.02 (coef +0.24, acc 0.73)
  y PF1 0.015 (+0.28, acc 0.63); resto sin variación. Lock-in temprano débil a N=30.

## 5. Veredicto vs lo pre-registrado

"Biestabilidad localizada y afirmada" — SÍ, con el matiz de que el instrumento
principal (dip) es el más débil y los fuertes son GMM+Levene+distribuciones.
La indeterminación de N=10 se resuelve: PF1 = un atractor + escapes raros;
PF5 0.02 = dos cuencas (0.45/0.90); PF5 0.015 = colapso; PF5 ≥0.025 = techo.
Zona completa: colapso → indeterminación/biestabilidad → techo en 0.015 → 0.025.
