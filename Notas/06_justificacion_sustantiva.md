# 06 — Justificación sustantiva del cambio de fase / biestabilidad (21 oct 2026)

Fenómeno: bajo cobertura escasa (~0.02), la estrategia focalizada (`strategic`,
score = (1−pir)·income·(1−ra)) colapsa o se vuelve indeterminada (PF5 0.27–0.94),
mientras `random` degrada linealmente; sobre ~0.04 strategic domina. Pregunta: ¿qué
parte de esto es economía real y qué parte artefacto del modelo?

## 1. Mapeo institucional: Chile fiscaliza "strategic" con cobertura bajo el umbral

- **El SII real es strategic.** PGCT 2026 p. 21: 67% de las horas de fiscalización al
  2.8% de contribuyentes (riesgos complejos/alto impacto). Eso es selección por
  riesgo, el análogo directo del `fiscal-risk-score`.
- **Opera bajo la zona de colapso del modelo.** Cobertura real: 0.097% auditorías
  puras, 0.34% +RC (JUSTIFICACION §a). El modelo dice que bajo ~2–4% el targeting
  ingenuo deja de funcionar. Chile está un orden de magnitud bajo ese piso.
- **Ley 21.713 (oct-2024) mueve tres piezas del mecanismo:**
  (i) horizonte de revisión 3 años → ancla legal de k=3 (prescripción general),
  6 años casos calificados → k=7 (ya en JUSTIFICACION §g);
  (ii) **denunciante anónimo con 10% de la multa** → canal social real de
  observación vecinal, análogo empírico de `weights-sanction` (la detección ajena
  que disuade);
  (iii) **fiscalización unificada de grupos empresariales** → enforcement sobre la
  red, análogo de targetear hubs (Andrei); más NGA antielusión y certificación de
  sostenibilidad tributaria (cumplimiento cooperativo OCDE).
- **Transparencia de la selección** (gobernanza SII, UCM 2024): si el score es
  público/predecible, se puede *gamear* — el correlato de Canessa ("evitar patrones
  predecibles", income-level colapsa por señalización).

## 2. Literatura: el resultado extiende, no contradice

- **Canessa (draft dic-2025, este repo): strategic≈random con PF5, strategic>random
  con PF1; explica por "over-focusing"** (el muestreo neutral cubre lo que el foco
  pierde). Nuestro resultado lo extiende a la dimensión cobertura: el over-focusing
  se vuelve catastrófico cuando el presupuesto es escaso. La interacción
  selección×memoria (p<.0001 en sus ANOVAs) gana un tercer eje.
- **Hashimzade–Myles–Rablen 2016: targeting domina a random — pero al 5% de
  cobertura y con predictores calibrados.** Nuestro umbral (~2–4%) y su 5% son
  consistentes: el targeting necesita piso de cobertura + calibración. No hay
  contradicción; hay condición de borde. Citar así en la tesis.
- **Bachas et al. 2025 (Senegal, experimento de campo): el análogo real directo.**
  Score de riesgo ingenuo (lógica económica sin entrenar) vs inspectores: los
  audits del algoritmo detectan **89% menos evasión**; el score predice evasión
  solo *dentro* de los casos elegidos por inspectores, no en los del algoritmo;
  ni el ML posterior mejora más que moderadamente. Es exactamente nuestro
  confounding del ingreso: targeting sobre observables ingenuos falla, y falla
  *aunque el score correlacione en submuestras*. La lección "los algoritmos no
  superan burócratas expertos en tareas complejas con datos pobres" es la versión
  de campo de "strategic necesita piso de cobertura y calibración".
- **Andrei et al. 2014: auditar hubs interconectados propaga honestidad por
  imitación** (MGTR menor, p≈1.6e-9). Micro-mecanismo del lado concentración:
  señales concentradas donde la red las retransmite. Nuestro modelo lo tiene a
  medio camino (alcance 1 salto, sin imitación del éxito) — por eso la
  concentración ayuda arriba del umbral y daña abajo (regiones sin cobertura).
- **Di Mauro et al. 2019: template de tipping** (crítico ~55% cumplidores iniciales
  con IF=CF=1; siempre >50%). Analogía **estructural, no mecanicista**: transición
  crítica genuina, pero gobernada por share de cumplidores e imitación — canales
  que nuestro modelo no tiene. Citar como familia de fenómenos, no como respaldo
  del mecanismo. (Nuestro umbral vive en cobertura×memoria, el suyo en
  composición inicial.)
- **Alm et al. 2017 (peer effects):** informar auditorías de vecinos mueve
  cumplimiento en ambas direcciones → respalda el canal de señales y PF como
  persistencia del spillover. **DeBacker 2018 / Beer et al. 2020:** decaimiento
  (+14.2%→1/3 a 5 años; +64%→+44% a 3 años) → ya ancla `audit-noise` (JUSTIFICACION §h).
  **Antunes et al. 2005:** sin memoria, evasores ~90% → la memoria (PF) es
  load-bearing, consistente con PF1→colapso / PF5→sostén a 2%.

## 3. Mecanismo causal propuesto (tesis)

Bajo presupuesto de auditoría, `strategic` es **explotación codiciosa de una
estimación ruidosa** (score dominado por lotería de ingresos σ=7, verificación
código + distribuciones): concentra un flujo de señales ya escaso en blancos
muchas veces equivocados, dejando regiones enteras sin disuasión que derivan a
cero; `random` reparte el mismo flujo uniformemente (degradación lineal).
Con memoria larga, las señales redundantes persisten (PF/audit-rate ticks) y el
error se fosiliza → indeterminación máxima en strategic PF5 0.02. Predicción
falsable en el propio modelo: un híbrido (base aleatoria + top-up por riesgo)
debería dominar a strategic puro a baja cobertura.

## 4. Límites honestos (no negociables en la tesis)

1. Sin canal de imitación, nada sobre difusión del fraude (nota 04).
2. Libros congelados: la "detección" es en parte lotería contable; la disuasión
   opera por flujo de señales, no por precisión. Cuantificar falsos positivos
   antes de afirmar precisión del targeting (pendiente).
3. El que falla es el targeting **ingenuo** (score sin calibrar, Bachas dixit);
   no refuta el targeting calibrado con buenos datos (SII tiene RCV/DTE/facturación
   electrónica: Chile está mejor datado que Senegal 2018).
4. Tick ≠ año; cobertura 2% es estilización al alza (JUSTIFICACION §a).
5. N=10 en la zona biestable; el N≥30 va en 0.015–0.035. Trayectorias: PF1 converge
   (un atractor), PF5 indistinguible entre biestabilidad y transitorio ultra-lento.

## 5. Fraseo para la tesis (implicancia de política)

*La focalización por riesgo exige un piso de cobertura: bajo él, un score ingenuo
concentra la fiscalización donde no rinde y deja sin disuadir al resto, de modo
que aleatorizar —o hibridar— domina. La cobertura efectiva chilena (<1%) está bajo
la zona donde el targeting ingenuo funciona; la Ley 21.713 amplía facultades y
horizonte (3 años) pero no eleva por sí sola la cobertura efectiva: el riesgo es
sofisticar la puntería sin el presupuesto que la hace rendir.*

Refs clave: Canessa–Peña–Quezada draft dic-2025 (este repo); Hashimzade et al. 2016
doi:10.1016/j.jebo.2015.11.009; Bachas et al. 2025 CEPR DP20608; Andrei et al. 2014
doi:10.1016/j.joep.2013.01.002; Di Mauro et al. 2019 doi:10.1140/epjb/e2019-90722-9;
Alm et al. 2017 doi:10.1111/1475-5890.12111; DeBacker et al. 2018 doi:10.1086/697683;
Beer et al. 2020 doi:10.1093/cesifo/ifz018; SII PGCT 2026; Ley 21.713 (D.O. 24-10-2024).
