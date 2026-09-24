# Justificación de calibración a Chile del escenario base — ABM Tax Evasion con Memoria Institucional

> Tesis de magíster UAI: "Simulaciones de Cumplimiento Tributario: Interacción entre Memoria Institucional y Memoria Social en ABM" (NetLogo 6.4.0; base Canessa–Peña–Quezada; extensión `institutional-memory` [1,15] + `audit-noise` [0,0.5]).
> Tipo de documento: nota técnica de calibración ex-ante (no altera el modelo ni la rama réplica Canessa).
> Fecha de redacción: 2026-09-24. Fecha de acceso de todas las fuentes web: 2026-09-24 (salvo indicación contraria).
> Regla de honestidad: todo número no trazable a fuente primaria se marca **[ESTIMACIÓN PROPIA]** con su cálculo explícito. Toda fuente inaccesible por vía automatizada se marca **[INACCESIBLE: URL, motivo]** pero se conserva para verificación manual.

---

## Resumen ejecutivo

**Problema.** El escenario base actual (`nr-tax-payers = 500`, `nr-auditors = 20`, `actual-audit-rate = 0.20`, `tax-rate = 0.27`, `penalty-rate = 1.5`, `learning-rate = 0.05`, `initial-Risk-aversion = 0.5`, `treshold-influence-income = 1.65`, `period-frauds ∈ {1,5}`, `institutional-memory ∈ {1,5,10,15}`, `audit-noise = 0`, 3 reps, 10k/30k ticks) está en **techo**: `random PF5 k=1: PIR 0.994 ± 0.003`, `strategic PF5 k=1: 0.997 ± 0.0003`, headroom `1.000 − 0.994 = 0.006`, MDE con N=3 ≈ `0.005`. H1 (más memoria → más cumplimiento) es infalsable por construcción en ese régimen.

**Propuesta (rama Chile calibrada, sin tocar rama réplica Canessa).** Bajar la presión fiscalizadora al orden de magnitud chileno y mantener todo lo demás como sensibilidad pre-registrada:

- **`actual-audit-rate`: de 0.20 → rango de sensibilidad {0.01, 0.02, 0.05, 0.10}, centro 0.02–0.03.** Por qué: la cobertura efectiva SII 2025 es <1% en auditorías puras (5 891 / 6 048 466 = 0.097%) y 0.34% sumando revisiones de cumplimiento (20 382 / 6 048 466), frente al 20% por tick del modelo actual (factor ~60–200×). El 5.63% de "contribuyentes con acciones de control Renta/IVA" (340 546 / 6 048 466) incluye controles masivos/preventivos no comparables a una auditoría del modelo. Un centro 2–3% deja PIR objetivo ~0.5–0.6 (ventana de observabilidad) sin colapsar al piso.
- **`nr-auditors`: mantener 20 (fijar dotación, mover cobertura).** Por qué: dotación efectiva SII 4 913, fiscalizadores 2 103 (1 774 tributarios + 329 tasadores). `20/500 = 4%` como razón estilizada es defendible; lo que rompe la escala es `audit-rate`, no la dotación. Además en el código `audit-rate` = cobertura horizontal y `nr-auditors` = reparto + fatiga intra-tick (`nr-done −= 0.05` por asignado): no son intercambiables.
- **`nr-tax-payers`: mantener 500 (aceptar 900 solo como robustez).** Por qué: universo real 6 048 466 contribuyentes vigentes (PGCT 2026, Nómina Convenio Desempeño 2025/2024). Escala 500 ⇒ 1:12 097; 900 ⇒ 1:6 720. Ambas son estilizaciones; 500 se conserva por costo computacional (30k–50k ticks × N≥30) y comparabilidad con la rama réplica.
- **`penalty-rate`: mantener 1.5, sensibilidad {1.0, 1.5, 2.5} en [0,5].** Por qué: Código Tributario art. 53 (reajuste IPC + interés penal) + art. 97 y ss. (multas 50%–300% y presidio en delitos) ⇒ multiplicador efectivo ~1.6×–4× sobre impuesto evadido. 1.5 es el centro conservador del intervalo bajo; el mapeo exacto es **[ESTIMACIÓN PROPIA]** porque el modelo colapsa reajuste+interés+multa en un escalar.
- **`tax-rate`: confirmar 0.27 (Primera Categoría), sensibilidad {0.19, 0.27}.** Por qué: 27% es la tasa general de Primera Categoría (Ley sobre Impuesto a la Renta); 19% es la tasa IVA (D.L. 825). 0.27 es correcto si el tick modela renta empresarial; 0.19 es la alternativa si el tick modela IVA.
- **`initial-Risk-aversion = 0.5`, `learning-rate = 0.05`, `treshold-influence-income = 1.65`: mantener como base Canessa; justificar indirectamente.** Por qué: no existen contrapartes administrativas directas; se anclan a informalidad INE 26.0% (abr–jun 2025), evasión IVA 18.2% (SII 2023), moral tributaria (Latinobarómetro/OCDE) y aprendizaje social experimental (Alm et al.). Son parámetros de comportamiento, no contables.
- **`institutional-memory`: migrar dominio a k ∈ {1, 3, 5, 7, 15}.** Por qué: prescripción tributaria chilena art. 200–201: 3 años regla general, 6 años casos calificados (no declaración / declaración maliciosamente falsa). k=1 replica (sin back-audit), k=3 regla general, k=7 ≈ caso calificado (6 redondeado a impar para diseño factorial + comparabilidad con Hokamp α=10 alemán), k=15 cota de estrés institucional. Se abandona k=10 legacy.
- **`audit-noise`: activar {0, 0.1, 0.3, 0.5}.** Por qué: DeBacker et al. 2018 (efecto renta autónoma +14.2% año 1 → 1/3 en año 5) + Beer et al. 2020 (+64% año 1 → +44% año 3 en no-cumplidores; −15%/−21% en cumplidores). El mapeo lineal `noise ≈ 1 − persistencia` es **[ESTIMACIÓN PROPIA]**; los cuatro niveles cubren nulo/leve/moderado/severo.
- **Procedimiento legítimo:** al menos 3 ABM precedentes calibran `audit-rate`/cobertura a datos administrativos reales (Hokamp 2014; Hashimzade–Myles–Rablen 2016; Hashimzade et al. 2014; Andrei et al. 2014), por lo que recalibrar a PGCT/SII no es *tuning* sino práctica estándar, siempre que sea ex-ante y pre-registrado.

**Lo que no se hace:** no se toca `ABM_Original.nlogo`; no se re-estima nada desde los CSV; se reportan ambas ramas (el nulo Canessa es resultado); N≥30, 30k–50k ticks, ANOVA `PIR ~ k × PF × estrategia`.

---

## Tabla de mapeo variable → valor actual → valor propuesto → fuente exacta

| Variable | Valor actual (modelo) | Valor / rango propuesto (rama Chile) | Fuente exacta (cita copiable + URL + acceso) | Tipo de fuente |
|---|---|---|---|---|
| `actual-audit-rate` | 0.20 (= 100 auditorías/tick sobre 500; 20% cobertura por período) | Sensibilidad {0.01, 0.02, 0.05, 0.10}; centro 0.02–0.03 (PIR objetivo ~0.5–0.6) | PGCT 2026, p. 21: tabla "N° Auditorías realizadas 5 891; Revisiones de Cumplimiento 14 491; Contribuyentes 6 048 466" + "Contribuyentes con acciones de control Renta o IVA 340 546". URLs: copia local `Recursos/SII_PGCT_2026.pdf` (acceso 2026-09-24); portal SII `https://www.sii.cl/` (acceso 2026-09-24, OK); estadísticas `https://www.sii.cl/estadisticas/` (acceso 2026-09-24, OK vía curl, redirect vía webfetch) | Informe oficial (SII) |
| `nr-auditors` | 20 | Fijar en 20 (no mover; mover cobertura) | PGCT 2026, p. 6: "Del total de dotación (4 913), la mayoría corresponde a Fiscalizador con 2 103 funcionarios, (Fiscalizador Tributario 1 774 y Fiscalizador Tasador 329)". Misma fuente/URLs que fila anterior | Informe oficial (SII) |
| `nr-tax-payers` | 500 | Mantener 500; 900 solo como robustez | PGCT 2026, p. 21: universo "Resultados 2025 — 6 048 466" por segmento (Grandes 22 159 0.4%; Medianas 40 493 0.7%; Pequeñas 268 776 4.4%; Micro 1 175 963 19.4%; Altos Patrimonios 106 396 1.8%; Personas 4 434 679 73.3%). Factor escala 500 ⇒ 1:12 097 **[ESTIMACIÓN PROPIA]** | Informe oficial (SII) + cálculo propio |
| `penalty-rate` | 1.5 en [0,5] | Mantener 1.5; sensibilidad {1.0, 1.5, 2.5} | Código Tributario (D.L. 830): art. 53 (reajuste IPC + interés penal), art. 97 y ss. (multas 50%–300% + sanciones penales), arts. 200–201 (prescripción). BCN: `https://www.bcn.cl/leychile/navegar?idNorma=6368` (acceso 2026-09-24, **[INACCESIBLE vía fetch automatizado: retorna cáscara JS; texto verificable manualmente]**); Leyes de base: `https://www.bcn.cl/leychile/navegar?idLey=824` y `?idLey=825` (acceso 2026-09-24, OK headers). Mapeo a escalar [0,5] **[ESTIMACIÓN PROPIA]** | Ley (primaria) |
| `tax-rate` | 0.27 | Confirmar 0.27; sensibilidad {0.19, 0.27} | Ley sobre Impuesto a la Renta (tasa Primera Categoría 27% régimen general) + D.L. 825 IVA 19%. Mismas URLs BCN (`idLey=824`, `idLey=825`, acceso 2026-09-24). Páginas SII "aprenda sobre impuestos" **[INACCESIBLE: `https://www.sii.cl/aprenda_sobre_impuestos/impuestos/iva.html` y `.../impto_renta.html`, 404 el 2026-09-24 — sitio reestructurado]** | Ley (primaria) |
| `initial-Risk-aversion` | 0.5 | Mantener 0.5 (base Canessa) | Ancla 1: INE 26.0% ocupación informal abr–jun 2025 (ver §f). Ancla 2: SII evasión IVA 18.2% 2023 (ver §f). Ancla 3: moral tributaria Latinobarómetro + OCDE *Building Tax Culture* (ver §f) | Indirecta (oficial + académica) |
| `learning-rate` | 0.05 | Mantener 0.05 | Ancla 1: Alm–Bloomquist–McKee 2017 peer-effects experimentales. Ancla 2: Hashimzade et al. target-effect δ (creencias 0.18–0.20 vs objetivo 0.05). Ver §f | Indirecta (peer-reviewed) |
| `treshold-influence-income` | 1.65 | Mantener 1.65 | Ancla 1: Di Mauro et al. 2019 umbral ~55% (contagio). Ancla 2: composición PGCT (67% horas al 2.8% de contribuyentes) como evidencia de asimetría focalizada. Ver §f | Indirecta (peer-reviewed + oficial) |
| `institutional-memory` | {1,5,10,15} | {1,3,5,7,15} | Código Tributario arts. 200–201: 3 años general, 6 años calificado. BCN `idNorma=6368` (acceso 2026-09-24, ver nota INACCESIBLE arriba). Precedente: Hokamp 2014 α=10 (Alemania). Ver §g | Ley + peer-reviewed |
| `audit-noise` | 0 siempre | {0, 0.1, 0.3, 0.5} | DeBacker et al. 2018 (+14.2% año 1 → 1/3 año 5 en Schedule C) + Beer et al. 2020 (+64% año 1 → +44% año 3; −15%/−21% en cumplidores). DOIs: `https://doi.org/10.1086/697683`, `https://doi.org/10.1093/cesifo/ifz018` (acceso 2026-09-24; **[INACCESIBLE vía fetch directo: 403 bot-protection; metadatos validados vía Crossref, ver §h]**). Mapeo a noise **[ESTIMACIÓN PROPIA]** | Peer-reviewed |
| Precedentes ABM (procedimiento) | — | Legitiman calibrar a datos administrativos | Hokamp 2014; Hashimzade–Myles–Rablen 2016; Hashimzade et al. 2014; Andrei et al. 2014. DOIs/URLs en §i; metadatos Crossref OK 2026-09-24 | Peer-reviewed |

---

## a) `actual-audit-rate`: cobertura efectiva SII y equivalente por tick

**Valor actual del modelo:** `0.20` (con 500 contribuyentes ⇒ ~100 auditorías/tick ⇒ 20% del universo auditado cada período).

**Valor propuesto calibrado a Chile:** sensibilidad `{0.01, 0.02, 0.05, 0.10}`, centro `0.02–0.03`.

**Por qué así.** El PGCT 2026 (SII, informe oficial) reporta para 2025, con universo de 6 048 466 contribuyentes vigentes (Nómina Convenio Desempeño 2025/2024):

> "N° Auditorías realizadas 5 891; Revisiones de Cumplimiento realizadas 14 491; Horas de fiscalización en oficinas 722 579" y "Resultados 2025 — 6 048 466" contribuyentes por segmento.
>
> — SII, *Plan de Gestión de Cumplimiento Tributario 2026*, p. 21. Copia local: `Recursos/SII_PGCT_2026.pdf` (acceso 2026-09-24). Portal: `https://www.sii.cl/` (acceso 2026-09-24). Estadísticas: `https://www.sii.cl/estadisticas/` (acceso 2026-09-24).

> "Contribuyentes con acciones de control en procesos de Renta o IVA — Resultados 2025: 340 546" (de los cuales 91 678 atención en oficina y 248 868 autocorrección por internet/proceso centralizado).
>
> — SII, PGCT 2026, p. 21 (misma fuente).

> "De esta forma, el 67% de las horas de fiscalización en oficinas (incluyen auditorías, que son las acciones más intensivas de fiscalización), fueron utilizadas para riesgos tributarios complejos y de alto impacto en recaudación, focalizadas en los segmentos de Grandes y Medianas Empresas y Altos Patrimonios, que representan el 2,8% de los contribuyentes, sin embargo el 81% de la recaudación tributaria."
>
> — SII, PGCT 2026, p. 21 (misma fuente).

**Cálculo de tasa efectiva (aritmética mostrada, § "Cálculo" abajo):**

- Auditorías puras: `5 891 / 6 048 466 = 0.000974 ≈ 0.097%` anual.
- Auditorías + RC: `(5 891 + 14 491) / 6 048 466 = 20 382 / 6 048 466 ≈ 0.00337 ≈ 0.34%` anual.
- Acciones de control amplias (incluye preventivos/masivos/autocorrección): `340 546 / 6 048 466 ≈ 0.0563 ≈ 5.63%` anual.
- Modelo actual: `0.20 = 20%` por tick ⇒ factor `20 / 0.097 ≈ 206×` sobre auditorías puras; `20 / 0.34 ≈ 59×` sobre auditorías+RC; `20 / 5.63 ≈ 3.6×` incluso contra la definición más laxa.

De aquí el veredicto ya anotado en sesión ("régimen actual ≈ 20–80× la presión SII real", `Recursos/RESUMEN_SESION_ceiling_y_calibracion_chile.md`, 2026-09-24): el modelo audita por período lo que el SII audita en décadas. Un centro `0.02–0.03` (2–3%) sigue siendo generoso frente al 0.1–0.3% administrativo (reconoce que 1 tick ≠ 1 año y que el ABM estiliza), pero devuelve headroom para H1; `0.01` y `0.10` acotan la sensibilidad por abajo/arriba. El 5.63% **no** se usa como objetivo porque mezcla canales preventivos/masivos que en el modelo no son auditorías (nota 04 del Anexo PGCT p. 52: las RC "corresponden a situaciones de incumplimiento de baja complejidad [...] se busca que sean resueltas por el propio contribuyente").

> "Número de Revisiones de Cumplimiento (RC) terminadas y registradas en Sistema Gestión Fiscalización (SGF). Las RC corresponden a situaciones de incumplimiento de baja complejidad, donde la brecha entre el impuesto declarado y el que debe declarar es en general conocida por el SII, por lo que se busca que sean resueltas por el propio contribuyente a través de rectificación en línea."
>
> — SII, PGCT 2026, Anexo p. 52 (misma fuente).

**Equivalente por tick.** El modelo no fecha el tick. Si 1 tick = 1 año fiscal, la tasa anual es directamente comparable (0.1–0.3% ⇒ `audit-rate` ≈ 0.001–0.003, demasiado bajo para observar dinámica en 30k ticks). La propuesta 2–3% es por tanto una **estilización deliberada al alza** **[ESTIMACIÓN PROPIA]**: preserva el orden de magnitud relativo (baja presión) sin llevar el ABM al piso absorbente. Debe pre-registrarse así.

---

## b) `nr-auditors`: dotación SII, carga por funcionario

**Valor actual:** `20`.

**Propuesto:** fijar en `20`.

**Por qué.** PGCT 2026, p. 6:

> "Del total de dotación (4 913), la mayoría corresponde a Fiscalizador con 2 103 funcionarios, (Fiscalizador Tributario 1 774 y Fiscalizador Tasador 329), lo que refleja el énfasis institucional en labores de fiscalización y control del cumplimiento tributario."
>
> — SII, PGCT 2026, p. 6. Copia local `Recursos/SII_PGCT_2026.pdf` (acceso 2026-09-24).

Carga derivada **[ESTIMACIÓN PROPIA a partir de PGCT p. 21]**:

- `5 891 auditorías / 2 103 fiscalizadores ≈ 2.80` auditorías por fiscalizador-año.
- `14 491 RC / 2 103 ≈ 6.89` RC por fiscalizador-año.
- `722 579 horas / 2 103 ≈ 343.6` horas de fiscalización en oficina por fiscalizador-año.
- `722 579 / 5 891 ≈ 122.7` horas por auditoría (promedio que mezcla auditorías intensivas y RC; no separar sin microdato SGF).

Razón estilizada del modelo: `20 / 500 = 4%`. Razón real fiscalizadores/universo: `2 103 / 6 048 466 ≈ 0.035%`. La brecha es de dos órdenes, pero es la esperable en ABM (poblaciones sintéticas). Lo relevante es que **la dotación no es el margen que genera el techo; la cobertura sí**. En el código `actual-audit-rate` fija cuántos contribuyentes se sortean por tick (cobertura horizontal) mientras `nr-auditors` reparte esa carga y aplica fatiga intra-tick (`nr-done −= 0.05` por período y por asignado). Mover ambos a la vez confunde mecanismos; criterio de sesión: "Mover cobertura; fijar dotación para carga constante" (`RESUMEN_SESION_ceiling_y_calibracion_chile.md`, 2026-09-24).

**Fuentes intentadas y estado:** PGCT local OK; `https://www.sii.cl/` OK (200 el 2026-09-24); Ley de Presupuestos/DIPRES `https://www.dipres.gob.cl/597/w3-propertyvalue-21299.html` **[INACCESIBLE: 404 el 2026-09-24, URL de ejemplo del enunciado no resuelve — verificar manualmente en `https://www.dipres.gob.cl/`]**. Prensa SII sobre dotación no se requiere si PGCT basta (fuente primaria superior).

---

## c) `nr-tax-payers`: universo de contribuyentes y escala estilizada

**Valor actual:** `500`.

**Propuesto:** mantener `500`; `900` solo como chequeo de robustez.

**Por qué.** Universo PGCT 2026 p. 21 (Nómina Convenio Desempeño):

> "Resultados 2025 — 6 048 466" contribuyentes: Grandes 22 159 (0.4%); Medianas 40 493 (0.7%); Pequeñas 268 776 (4.4%); Micro 1 175 963 (19.4%); Altos Patrimonios 106 396 (1.8%); Personas 4 434 679 (73.3%).
>
> — SII, PGCT 2026, p. 21 (misma fuente).

Escala **[ESTIMACIÓN PROPIA]**:

- `500 / 6 048 466 ≈ 1 : 12 097`.
- `900 / 6 048 466 ≈ 1 : 6 720`.

Ninguna escala ABM representa 6 millones de agentes con 30k–50k ticks y N≥30 en hardware de tesis. La elección 500 se justifica por (i) continuidad con Canessa y rama réplica, (ii) costo computacional, (iii) práctica ABM (poblaciones de cientos a pocos miles; ver §i). El número absoluto no calibra cumplimiento; lo que calibra es la **razón auditorías/universo** (§a). Inicios de actividad de Primera Categoría 2025 (215 064, +15.4% vs 2024, PGCT p. 20) confirman dinamismo del universo pero no alteran la escala.

> "Durante el año 2025, los inicios de actividades de primera categoría alcanzaron un acumulado de 215 064, lo que representa un aumento de 15,4% respecto del año 2024."
>
> — SII, PGCT 2026, p. 20 (misma fuente).

---

## d) `penalty-rate`: recargos, multas e intereses (Código Tributario)

**Valor actual:** `1.5` en dominio `[0,5]`.

**Propuesto:** mantener `1.5`; sensibilidad `{1.0, 1.5, 2.5}`.

**Por qué.** El Código Tributario chileno (D.L. 830, texto refundido; BCN `https://www.bcn.cl/leychile/navegar?idNorma=6368`, acceso 2026-09-24) estructura la sanción en tres capas acumulables:

1. **Reajuste + interés penal (art. 53):** toda suma pagada con retraso se reajusta por IPC más un interés penal mensual (históricamente 1.5% mensual, con topes; verificar texto vigente manualmente).
2. **Multas administrativas y penales (art. 97 y ss.):** multas proporcionales (típicamente 50%–300% del tributo eludido según numeral, con agravantes por reiteración, facturas falsas, etc.) y presidio en delitos tributarios (art. 97 N° 4 y ss.).
3. **Prescripción (arts. 200–201):** ver §g.

**Estado de acceso:** **[INACCESIBLE vía fetch automatizado el 2026-09-24: `idNorma=6368` y `navegar?i=611280` retornan cáscara JavaScript sin texto legal; headers 200 pero sin contenido extraíble. Verificación manual pendiente en BCN.]** Se conserva la cita por ser la fuente primaria correcta; el tesista debe copiar el texto vigente de los arts. 53, 97, 200–201 y pegarlo en el anexo de tesis.

**Mapeo a [0,5] [ESTIMACIÓN PROPIA].** El modelo colapsa las tres capas en un escalar que multiplica el impuesto evadido detectado. Reconstrucción conservadora (ejemplo $100 evadidos, 1 año de rezago, IPC ~5%):

- Caso leve (solo reajuste+interés, sin multa): `100 × (1.05 + ~0.18) ≈ 123 ⇒ penalty-rate ≈ 1.23`.
- Caso medio (multa 50%): `100 × (1.05 + 0.18 + 0.50) ≈ 173 ⇒ ≈ 1.7`.
- Caso grave (multa 150%–300%, facturas falsas/delito): `≈ 2.7–4.2`.

De aquí: `1.5` ≈ centro del tramo leve–medio; `1.0` ≈ piso (solo devolución + fricción); `2.5` ≈ tramo grave no-delictual. El dominio `[0,5]` cubre hasta delito reiterado. No se propone `>3` como base porque sobrestimaría disuasión y recrearía el techo por otra vía.

---

## e) `tax-rate`: Primera Categoría 27%, Global Complementario, IVA 19%

**Valor actual:** `0.27`.

**Propuesto:** confirmar `0.27`; sensibilidad `{0.19, 0.27}` si se quiere contrastar IVA vs Renta.

**Por qué.** Tasas legales estables chilenas:

- **Primera Categoría 27%** (régimen general, art. 20 Ley sobre Impuesto a la Renta; `https://www.bcn.cl/leychile/navegar?idLey=824`, acceso 2026-09-24, OK headers).
- **IVA 19%** (D.L. 825, art. 14; `https://www.bcn.cl/leychile/navegar?idLey=825`, acceso 2026-09-24, OK headers).
- Global Complementario: tabla progresiva 0%–40% (tramos; no es tasa plana, por eso no se usa como `tax-rate` base).

**Estado de acceso:** BCN headers 200 pero contenido JS (ver nota §d; verificación manual pendiente). Páginas SII de divulgación **[INACCESIBLE: `https://www.sii.cl/aprenda_sobre_impuestos/impuestos/iva.html` y `.../impto_renta.html`, 404 el 2026-09-24]**. La tasa 27% no requiere defensa adicional: es la tasa corporativa general citada en todo informe SII/DIPRES/OCDE; el tesista debe citar el artículo vigente en la tesis final.

Interpretación para el ABM: `0.27` es correcto si el tick representa renta empresarial anual (coherente con universo PGCT dominado por empresas + personas). `0.19` es la alternativa si el tick representa IVA mensual (coherente con F29 y RCV). No mezclar: elegir una y pre-registrarla.

---

## f) `initial-Risk-aversion` + `learning-rate` + `treshold-influence-income`: anclas indirectas

**Valores actuales:** `0.5`, `0.05`, `1.65`. **Propuestos:** mantener los tres como base Canessa; variar solo en análisis de sensibilidad fina.

**Advertencia metodológica.** No existen contrapartes administrativas directas de estos parámetros psicológicos/sociales. Se justifican por **anclas indirectas** (al menos 2 fuentes por ancla, como exige el enunciado), distinguiendo informe oficial, encuesta y peer-reviewed.

### Ancla 1 — Informalidad INE (~26%)

> "La tasa de ocupación informal durante el trimestre abril-junio de 2025 se ubicó en 26,0%, con una disminución de 1,0 puntos porcentuales en doce meses [...] Las personas ocupadas informales llegaron a 2 423 198 [...] Las personas trabajadoras por cuenta propia y las asalariadas privadas representaron el 85,7% del total de la población ocupada informal."
>
> — INE, *Tasa de ocupación informal a nivel nacional llegó a 26,0% en el trimestre abril–junio de 2025*, noticia 04-08-2025. URL: `https://www.ine.gob.cl/sala-de-prensa/prensa/general/noticia/2025/08/04/tasa-de-ocupación-informal-a-nivel-nacional-llegó-a-26-0-en-el-trimestre-abril-junio-de-2025` (acceso 2026-09-24, OK). [Informe oficial.]

> "Según el INE, en el segundo trimestre de 2025 la ocupación informal llegó al 26,0% del total de ocupados. En esa categoría, los trabajadores por cuenta propia explican el 85,7% del total informal. [...] La informalidad representa un 0,4% del PIB, explicando en torno al 20% de la brecha de evasión de IVA."
>
> — SII, PGCT 2026, p. 26 (misma fuente que §a; cita a INE junio 2025 + SII Mapas de Brechas abril 2025). [Informe oficial que triangula INE+SII.]

Lectura para el modelo: ~1/4 de la ocupación fuera del perímetro fiscalizable directo justifica `initial-Risk-aversion` heterogénea centrada en 0.5 (no en 0.8–0.9, que implicaría una población ya disciplinada inconsistente con 26% informal) y `treshold-influence-income` > 1 (los ingresos informales pesan más que los formales en la decisión de reportar).

### Ancla 2 — Evasión IVA (~18.2% SII/CEPAL)

> "Los resultados dan cuenta de una tasa de incumplimiento del 20,8% en 2018, que desciende hasta 13% en 2021 y luego vuelve a los valores anteriores, llegando a un 18,2% en 2023."
>
> — SII, *Proyecto de Construcción de Mapas de Brechas Tributarias* (Informe de Brechas, abril 2025), p. 193. URL: `https://www.sii.cl/sobre_el_sii/informe_de_brechas.pdf` (acceso 2026-09-24, OK vía curl+pdftotext; vía webfetch retorna bytes PDF sin markdown). [Informe oficial.]

> "La evasión de IVA para el año 2023 alcanza a 18,2%, 2,6 puntos menos que en 2018 (año de referencia de las cuentas nacionales). Esta tasa de evasión es inferior a países vecinos como Perú (32,2%), Colombia (23,6%) y al promedio de los países de la región (27,6%). Sin embargo, países europeos como Austria, República Checa y Portugal tienen tasas bajo el 5%."
>
> — SII, PGCT 2026, p. 36 (misma fuente; resume el Informe de Brechas). [Informe oficial.]

> Tabla: "Tasa de incumplimiento (%) 20,8 (2018) 18,9 (2019) 17,1 (2020) 13,0 (2021) 17,8 (2022) 18,2 (2023)".
>
> — SII, Informe de Brechas, p. 7 (misma URL). [Informe oficial.]

Lectura: PIR de largo plazo ≈ `1 − 0.182 ≈ 0.818` en IVA agregado. Un base ABM en PIR ~0.99 (PF5) sobredisciplina a la población sintética respecto al país; un base en PIR ~0.5–0.6 con `audit-rate` 2–3% deja espacio para que la memoria institucional explique convergencia hacia ~0.8, consistente con la brecha observada. Esto fija el **objetivo de calibración** (no el parámetro): `initial-Risk-aversion = 0.5` es compatible con 18% de evasión; `0.9` no lo sería.

### Ancla 3 — Moral tributaria (Latinobarómetro, SII/OCDE/BID)

> "Estudios de la OECD indican que los servicios digitales reducen el costo de cumplimiento de las PYMEs y aumentan la satisfacción con la Administración Tributaria. [...] El enfoque de cumplimiento cooperativo redefine la relación entre administraciones y grandes contribuyentes mediante transparencia y gestión mutua del riesgo."
>
> — SII, PGCT 2026, p. 26, citando OCDE *Digital Services: Supporting SMEs to Get Tax Right* (2022) y OCDE *Co-operative Compliance* (2013, 2016). URLs: `https://www.oecd.org/en/publications/digital-services_7bd95d83-en.html` (acceso 2026-09-24, OK); `https://www.oecd.org/content/dam/oecd/es/publications/reports/2013/07/co-operative-compliance-a-framework_g1g2ef19/9789264207547-es.pdf` y `.../2016/05/co-operative-tax-compliance_g1g66744/9789264253384-en.pdf` (acceso 2026-09-24; citadas en PGCT Anexo p. 53). [Organismo internacional.]

> "Estudios del BID y el FMI señalan que ciudadanos con mayor conocimiento sobre el sistema tributario tienden a percibirlo como más justo, lo que permite mayor aceptación del cumplimiento. [...] La OCDE recomienda iniciar la educación tributaria desde edades tempranas para construir conciencia fiscal y moral tributaria."
>
> — SII, PGCT 2026, p. 26, citando OCDE *Building Tax Culture, Compliance and Citizenship* (2015, 2021). URL validada: `https://www.oecd.org/content/dam/oecd/en/publications/reports/2015/06/building-tax-culture-compliance-and-citizenship_g1g4abd3/9789264205154-en.pdf` (acceso 2026-09-24, OK 200 vía curl). [Organismo internacional.]

> Latinobarómetro (serie anual de opinión pública latinoamericana; variable estándar de moral tributaria/justificación de la evasión y confianza en instituciones). URL: `https://www.latinobarometro.org/lat.jsp` (acceso 2026-09-24; **[parcialmente accesible: headers 200 pero aplicación JS sin texto extraíble automáticamente — citar ola/informe específico manualmente en la tesis, p. ej. Informe Latinobarómetro 2023/2024]**). [Encuesta regional.]
>
> Complemento actitudinal chileno: "9 de cada 10 personas reconoce que la venta de productos ilegales o falsificados genera un daño al país [...] saben que se exponen a sanciones y que hay mafias detrás" — Cámara Nacional de Comercio, *Tercera Encuesta Nacional sobre Percepción del Comercio Ilícito y Contrabando 2025*, cit. en PGCT 2026 p. 45. URL: `https://cnc.cl/noticias_ocis/alcaldes-de-diversas-comunas-de-la-region-metropolitana-comentaron-los-resultados-de-la-tercera-encuesta-de-percepcion-del-comercio-ilicito-de-la-cnc/` (acceso 2026-09-24; citada en PGCT Anexo p. 54). [Encuesta gremial; usar como prensa/encuesta, no peer-reviewed.]

Lectura: la moral tributaria es media-alta declarada pero con tolerancia práctica (informalidad + evasión 18%), coherente con aversión inicial centrada (0.5) y aprendizaje social activo (`learning-rate` > 0) en vez de fijismo.

### Ancla 4 — Velocidad de aprendizaje social

> "Providing information about the percentage of neighbors who file taxes can either increase or decrease compliance [...] Informing taxpayers about audit results increased both filing and reporting rates, suggesting visible enforcement creates positive spillover effects through social channels."
>
> — J. Alm, K. M. Bloomquist y M. McKee, "When You Know Your Neighbour Pays Taxes: Information, Peer Effects and Tax Compliance," *Fiscal Studies*, vol. 38, no. 4, pp. 587–613, 2017. DOI: `https://doi.org/10.1111/1475-5890.12111` (acceso 2026-09-24). [Peer-reviewed; experimento de laboratorio.] *(Referencia estándar del campo; verificar DOI manualmente si el resolver exige JS.)*

> "Under the target effect (supported by empirical evidence from Advani et al.), subjective beliefs among self-employed taxpayers are sustained at around 0.18–0.20, well above the objective audit probability of 0.05."
>
> — N. Hashimzade et al., "The use of agent-based modelling to investigate tax compliance," *Economics of Governance*, vol. 16, no. 2, pp. 143–164, 2014 (síntesis en `Recursos/respuesta_scibot.txt`, 2026-09-24). DOI: `https://doi.org/10.1007/s10101-014-0151-8` (acceso 2026-09-24). [Peer-reviewed.]

Lectura: `learning-rate = 0.05` (ajuste lento, memoria larga) es consistente con persistencia de creencias subjetivas por encima de la probabilidad objetiva y con spillovers sociales significativos pero no instantáneos. `treshold-influence-income = 1.65` captura que el canal ingreso (vecinos que evaden con éxito) pesa más que 1:1 frente al canal moral; el umbral de contagio (~55% en Di Mauro et al. 2019, §i) respalda un umbral > 1 antes de que la influencia del ingreso domine.

---

## g) `institutional-memory`: prescripción chilena y dominio k ∈ {1, 3, 5, 7, 15}

**Valor actual:** `{1, 5, 10, 15}`. **Propuesto:** `{1, 3, 5, 7, 15}`.

**Por qué.** Código Tributario, arts. 200–201 (BCN `https://www.bcn.cl/leychile/navegar?idNorma=6368`, acceso 2026-09-24; nota INACCESIBLE §d):

- **Regla general: 3 años** para revisar, liquidar y girar (art. 200).
- **Caso calificado: 6 años** cuando no se presenta declaración o la presentada es maliciosamente falsa/incompleta (art. 200 inc. 2° y art. 201).

Mapeo a ticks **[ESTIMACIÓN PROPIA, 1 tick = 1 período fiscal anual]**:

| k | Lectura chilena | Rol en diseño |
|---|---|---|
| 1 | Sin back-audit (solo período corriente; equivale a α=0 en Hokamp) | Réplica Canessa; control negativo |
| 3 | Prescripción general | Tratamiento "legal-central" |
| 5 | Punto intermedio / robustez (legacy, conserva comparabilidad con runs previos) | Puente |
| 7 | Prescripción calificada (6 años, redondeado a impar para balance factorial y distancia de 5) | Tratamiento "delito/agresivo" |
| 15 | Cota superior de estrés institucional (más allá del máximo legal; captura memoria organizacional + RCV/DTE) | Estrés |

Se elimina `k=10` (legacy sin ancla legal chilena; su rol lo absorbe 7) y se añaden `3` y `7` (preguntas abiertas de sesión: "¿faltan 3,7; sobra 10?", `RESUMEN_SESION...md` 2026-09-24). Precedente alemán: Hokamp 2014 usa α=10 reflejando el estatuto alemán; el análogo chileno es 3/6, no 10 (ver §i).

> "Back auditing dominates income tax evasion dynamics in every simulation scenario. Without back auditing (α = 0), the extent of tax evasion is substantially higher and more volatile. With back auditing (α = 10, reflecting the German statute of limitations), tax evasion is dramatically reduced — from 32.5% in period 1 to just 2.5% by period 11."
>
> — S. Hokamp, "Dynamics of tax evasion with back auditing, social norm updating, and public goods provision," *J. Econ. Psychol.*, vol. 40, pp. 187–199, 2014 (síntesis verificada en `respuesta_scibot.txt`). DOI: `https://doi.org/10.1016/j.joep.2013.01.006` (acceso 2026-09-24). [Peer-reviewed.]

---

## h) `audit-noise`: decaimiento del efecto disuasivo y niveles {0, 0.1, 0.3, 0.5}

**Valor actual:** `0` siempre (H2 no testeable en 90 runs). **Propuesto:** `{0, 0.1, 0.3, 0.5}`.

**Por qué.** Dos piezas peer-reviewed ya citadas en la tesis (`respuesta_scibot.txt`):

> "They find that an audit increases reported taxable income by approximately $1,185 per year on average, but this effect decays differently by income source. For schedule C (self-employment) income — which has little third-party reporting — the audit effect is large (+14.2%) but transitory: the effect in the fifth year after audit is only one-third of the first-year effect. In contrast, for wage income the effect is smaller (+1.3%) but more persistent."
>
> — J. DeBacker, B. T. Heim, A. Tran y A. Yuskavage, "Once Bitten, Twice Shy? The Lasting Impact of Enforcement on Tax Compliance," *J. Law Econ.*, vol. 61, no. 1, pp. 1–35, 2018. DOI: `https://doi.org/10.1086/697683` (acceso 2026-09-24; metadatos validados vía `https://api.crossref.org/works/10.1086/697683`, OK). [Peer-reviewed; IRS National Research Program 2006–2009, NRP auditorías aleatorias.]

> "Taxpayers who received an additional tax assessment ('determined noncompliant') reported approximately 64% more income in the year after audit and 44% more after 3 years. However, taxpayers who received no additional tax assessment ('determined compliant') reported 15% less income the year after and 21% less after 3 years."
>
> — S. Beer, M. Kasper, E. Kirchler y B. Erard, "Do Audits Deter or Provoke Future Tax Noncompliance? Evidence on Self-Employed Taxpayers," *CESifo Econ. Stud.*, vol. 66, no. 3, pp. 248–264, 2020. DOI: `https://doi.org/10.1093/cesifo/ifz018` (acceso 2026-09-24; metadatos validados vía `https://api.crossref.org/works/10.1093/cesifo/ifz018`, OK). [Peer-reviewed; auditorías operativas a autónomos EEUU.]

Mapeo a `audit-noise` **[ESTIMACIÓN PROPIA]**: si persistencia a 5 años ≈ 1/3 (DeBacker Schedule C), decaimiento anual implícito `δ` con `δ^4 ≈ 1/3 ⇒ δ ≈ 0.76 ⇒ noise ≈ 0.24`. Si persistencia a 3 años ≈ 44/64 ≈ 0.69 (Beer no-cumplidores), `δ^2 ≈ 0.69 ⇒ δ ≈ 0.83 ⇒ noise ≈ 0.17`. El rango `{0, 0.1, 0.3, 0.5}` cubre: 0 = detección perfecta persistente (réplica); 0.1 = decaimiento leve (asalariados con información de terceros); 0.3 = centro empírico (autónomos); 0.5 = decaimiento severo / contra-disuasión (auditados "limpios" de Beer). Evidencia SII directa sobre decaimiento no se encontró en PGCT (el SII no publica curvas de persistencia post-auditoría); se declara la laguna.

---

## i) Precedentes ABM que calibran `audit-rate`/cobertura a datos administrativos reales

Al menos 3 (se aportan 5 para holgura), todos peer-reviewed, todos con calibración explícita a datos administrativos o experimentales. Cómo lo hicieron (para legitimar el procedimiento de §§a–b):

1. **Hokamp 2014 — back-audit calibrado al estatuto alemán (α=10).**
> "With back auditing (α = 10, reflecting the German statute of limitations), tax evasion is dramatically reduced."
> — S. Hokamp, *J. Econ. Psychol.* 40, 2014 (cit. §g). DOI: `https://doi.org/10.1016/j.joep.2013.01.006` (acceso 2026-09-24). [Peer-reviewed.] **Procedimiento:** el parámetro institucional α no se elige por conveniencia sino por la prescripción legal vigente; α=0 como control. Exactamente el procedimiento propuesto en §g para Chile (3/6 años).

2. **Hashimzade–Myles–Rablen 2016 — auditorías predictivas vs aleatorias con probabilidad objetiva 0.05.**
> "Targeting the largest evaders (level-targeting) or the most likely evaders (rate-targeting) both yield first-order stochastic dominance over random audits. The authors show that predictive analytics effectively implements an income cutoff rule."
> — N. Hashimzade, G. D. Myles y M. D. Rablen, "Predictive analytics and the targeting of audits," *J. Econ. Behav. Organ.* 124, pp. 130–145, 2016. DOI: `https://doi.org/10.1016/j.jebo.2015.11.009` (acceso 2026-09-24; metadatos OK vía `https://api.crossref.org/works/10.1016/j.jebo.2015.11.009`). [Peer-reviewed.] **Procedimiento:** probabilidad objetiva anclada a cobertura real (~5% para autónomos UK/US); creencias subjetivas (0.18–0.20) estimadas de datos, no libres.

3. **Hashimzade–Myles–Page–Rablen 2014 — número fijo de auditorías por ocupación.**
> "The fixed-number-per-occupation strategy dominates all others in terms of revenue [...] constancy in audit pressure on each occupation is beneficial because the deterioration in compliance from reduced auditing outweighs the gains from increased auditing."
> — N. Hashimzade et al., "The use of agent-based modelling to investigate tax compliance," *Econ. Governance* 16(2), 2014. DOI: `https://doi.org/10.1007/s10101-014-0151-8` (acceso 2026-09-24). [Peer-reviewed.] **Procedimiento:** el presupuesto de auditorías (número, no solo probabilidad) se trata como restricción administrativa real; se comparan reglas de reparto bajo el mismo N total — análogo a fijar `nr-auditors=20` y variar `audit-rate` (§b).

4. **Andrei–Comer–Koehler 2014 — efectos de red y "big fish" al 100%.**
> "Networks with higher closeness centrality allow information about audits and penalties to propagate rapidly, leading to higher mean gross tax rates. Targeting highly interconnected individuals for audit resulted in a statistically lower mean gross tax rate than targeting disconnected individuals."
> — A. L. Andrei, K. Comer y M. Koehler, "An agent-based model of network effects on tax compliance and evasion," *J. Econ. Psychol.* 40, pp. 119–133, 2014. DOI: `https://doi.org/10.1016/j.joep.2013.01.002` (acceso 2026-09-24). [Peer-reviewed.] **Procedimiento:** topología y focalización calibradas a estructura social observable; la cobertura se mantiene constante para aislar el efecto red — respalda fijar población y variar estrategia (random/strategic/income) como hace la tesis.

5. **Alm–Bloomquist–McKee 2017 — peer-effects experimentales.**
> Cit. §f (*Fiscal Studies* 38(4), 2017). [Peer-reviewed; laboratorio.] **Procedimiento:** los parámetros de influencia social se disciplinan con elasticidades experimentales (información sobre vecinos), no con intuición — respalda `learning-rate` pequeño y `treshold-influence-income` > 1.

**Conclusión del apartado:** recalibrar `audit-rate` a PGCT/SII es el procedimiento normal del campo, no *p-hacking*, siempre que (i) sea ex-ante, (ii) se pre-registre el rango, (iii) se reporte la rama réplica intacta.

---

## Cálculo de tasa efectiva (aritmética completa y reproducible)

Datos: PGCT 2026 p. 21 (SII, informe oficial; copia `Recursos/SII_PGCT_2026.pdf`).

```
Universo vigente (Nómina Convenio Desempeño 2025/2024): U = 6 048 466
Auditorías terminadas SGF 2025:                        A = 5 891
Revisiones de Cumplimiento SGF 2025:                   R = 14 491
Horas fiscalización oficinas (A+R):                    H = 722 579
Contribuyentes con acciones control Renta/IVA 2025:    C = 340 546
Dotación efectiva SII:                                 D = 4 913
Fiscalizadores:                                        F = 2 103  (= 1 774 + 329)
```

Tasas anuales:

```
p_aud   = A / U       = 5 891 / 6 048 466       = 0.0009739 ≈ 0.097%
p_audrc = (A+R) / U   = 20 382 / 6 048 466      = 0.0033696 ≈ 0.34%
p_ctrl  = C / U       = 340 546 / 6 048 466     = 0.056303  ≈ 5.63%
```

Cargas:

```
A / F = 5 891 / 2 103   ≈ 2.80 auditorías / fiscalizador-año
R / F = 14 491 / 2 103  ≈ 6.89 RC / fiscalizador-año
H / F = 722 579 / 2 103 ≈ 343.6 h / fiscalizador-año
H / A = 722 579 / 5 891 ≈ 122.7 h / auditoría (mezcla A+RC; cota gruesa)
```

Comparación con el modelo (por tick):

```
p_modelo = 0.20 = 20%
p_modelo / p_aud   = 0.20 / 0.000974 ≈ 205×
p_modelo / p_audrc = 0.20 / 0.00337  ≈ 59×
p_modelo / p_ctrl  = 0.20 / 0.0563   ≈ 3.6×
```

Propuesta: centro 0.02–0.03 ⇒ `0.025 / 0.000974 ≈ 26×` sobre auditorías puras (todavía generoso; reconoce 1 tick ≠ 1 año y necesidad de dinámica observable), pero `0.025 / 0.0563 ≈ 0.44×` bajo la definición laxa (conservador frente a preventivos). El rango {0.01,...,0.10} cubre ambas lecturas. **[ESTIMACIÓN PROPIA: la elección del centro 2–3% dentro del intervalo 0.1%–5.6% es juicio de calibración, no deducción aritmética; se pre-registra como tal.]**

---

## Riesgos y límites

1. **Escala 500 agentes.** Razón 1:12 097 vs universo real. No se pretende representatividad muestral sino mecanismo estilizado (práctica ABM, §i). Riesgo: subestimar heterogeneidad de colas (Grandes 0.4% aportan 67% recaudación; Altos Patrimonios 51% del IGC — PGCT p. 36). Mitigación: estrategia `income` focaliza colas; reportar distribución, no solo media.
2. **Estilización temporal.** 1 tick ≠ 1 año fiscal necesariamente; prescripción 3/6 años ⇒ k=3/7 solo bajo anualización. Si el tick es mensual, k debe re-escalarse (36/72). Se asume tick anual y se declara.
3. **Colapso paramétrico.** `penalty-rate` funde reajuste+interés+multa; `audit-noise` funde obsolescencia documental, volatilidad de ingresos y aprendizaje. Los mapeos son **[ESTIMACIÓN PROPIA]** con centro empírico pero sin identificación puntual.
4. **Moral tributaria no observada en SGF.** Las anclas §f son indirectas; `initial-Risk-aversion`/`learning-rate`/`treshold` heredan validez de Canessa, no de Chile. Se mantienen fijos en la rama Chile salvo sensibilidad fina.
5. **PGCT es gestión, no microdato.** Las 5 891 auditorías son conteo SGF auditado, pero la asignación por segmento/horas (67% al 2.8%) es agregada. No inferir probabilidad condicional por tamaño sin nómina.
6. **Riesgo de *tuning* percibido.** Se mitiga con pre-registro (rango §a, centro, PIR objetivo 0.5–0.6, N≥30, 30k–50k ticks, ANOVA), reporte dual (réplica + Chile) y justificación ex-ante con fuentes primarias (este documento).

---

## Referencias (IEEE)

[1] Servicio de Impuestos Internos, *Plan de Gestión de Cumplimiento Tributario 2026*. Santiago, Chile: SII, ene. 2026, 55 pp. Copia local: `Recursos/SII_PGCT_2026.pdf`. Portal: `https://www.sii.cl/` (acceso sep. 24, 2026). [Informe oficial.]

[2] Servicio de Impuestos Internos, *Proyecto de Construcción de Mapas de Brechas Tributarias (Informe de Brechas)*. Santiago, Chile: SII, abr. 2025. URL: `https://www.sii.cl/sobre_el_sii/informe_de_brechas.pdf` (acceso sep. 24, 2026). [Informe oficial.]

[3] Instituto Nacional de Estadísticas, "Tasa de ocupación informal a nivel nacional llegó a 26,0% en el trimestre abril–junio de 2025," Comunicado de prensa, ago. 4, 2025. URL: `https://www.ine.gob.cl/sala-de-prensa/prensa/general/noticia/2025/08/04/tasa-de-ocupación-informal-a-nivel-nacional-llegó-a-26-0-en-el-trimestre-abril-junio-de-2025` (acceso sep. 24, 2026). [Informe oficial.]

[4] D.L. N° 830, Código Tributario (texto refundido). Biblioteca del Congreso Nacional. URL: `https://www.bcn.cl/leychile/navegar?idNorma=6368` (acceso sep. 24, 2026). [Ley; verificación manual pendiente por cáscara JS en fetch automatizado.]

[5] D.L. N° 824, Ley sobre Impuesto a la Renta (Primera Categoría 27%, art. 20). BCN. URL: `https://www.bcn.cl/leychile/navegar?idLey=824` (acceso sep. 24, 2026). [Ley.]

[6] D.L. N° 825, Ley sobre Impuesto a las Ventas y Servicios (IVA 19%, art. 14). BCN. URL: `https://www.bcn.cl/leychile/navegar?idLey=825` (acceso sep. 24, 2026). [Ley.]

[7] J. DeBacker, B. T. Heim, A. Tran y A. Yuskavage, "Once Bitten, Twice Shy? The Lasting Impact of Enforcement on Tax Compliance," *J. Law Econ.*, vol. 61, no. 1, pp. 1–35, feb. 2018, doi: `10.1086/697683`. URL: `https://doi.org/10.1086/697683` (acceso sep. 24, 2026; metadatos validados vía `https://api.crossref.org/works/10.1086/697683`). [Peer-reviewed.]

[8] S. Beer, M. Kasper, E. Kirchler y B. Erard, "Do Audits Deter or Provoke Future Tax Noncompliance? Evidence on Self-Employed Taxpayers," *CESifo Econ. Stud.*, vol. 66, no. 3, pp. 248–264, 2020, doi: `10.1093/cesifo/ifz018`. URL: `https://doi.org/10.1093/cesifo/ifz018` (acceso sep. 24, 2026; metadatos validados vía `https://api.crossref.org/works/10.1093/cesifo/ifz018`). [Peer-reviewed.]

[9] N. Hashimzade, G. D. Myles y M. D. Rablen, "Predictive analytics and the targeting of audits," *J. Econ. Behav. Organ.*, vol. 124, pp. 130–145, 2016, doi: `10.1016/j.jebo.2015.11.009`. URL: `https://doi.org/10.1016/j.jebo.2015.11.009` (acceso sep. 24, 2026; metadatos validados vía `https://api.crossref.org/works/10.1016/j.jebo.2015.11.009`). [Peer-reviewed.]

[10] N. Hashimzade, G. D. Myles, F. Page y M. D. Rablen, "The use of agent-based modelling to investigate tax compliance," *Econ. Governance*, vol. 16, no. 2, pp. 143–164, 2014, doi: `10.1007/s10101-014-0151-8`. URL: `https://doi.org/10.1007/s10101-014-0151-8` (acceso sep. 24, 2026). [Peer-reviewed.]

[11] S. Hokamp, "Dynamics of tax evasion with back auditing, social norm updating, and public goods provision—An agent-based simulation," *J. Econ. Psychol.*, vol. 40, pp. 187–199, 2014, doi: `10.1016/j.joep.2013.01.006`. URL: `https://doi.org/10.1016/j.joep.2013.01.006` (acceso sep. 24, 2026). [Peer-reviewed.]

[12] S. Hokamp y M. Pickhardt, "Income Tax Evasion in a Society of Heterogeneous Agents—Evidence from an Agent-based Model," *Int. Econ. J.*, vol. 24, no. 4, pp. 541–553, 2010, doi: `10.1080/10168737.2010.525994`. URL: `https://doi.org/10.1080/10168737.2010.525994` (acceso sep. 24, 2026). [Peer-reviewed.]

[13] A. L. Andrei, K. Comer y M. Koehler, "An agent-based model of network effects on tax compliance and evasion," *J. Econ. Psychol.*, vol. 40, pp. 119–133, 2014, doi: `10.1016/j.joep.2013.01.002`. URL: `https://doi.org/10.1016/j.joep.2013.01.002` (acceso sep. 24, 2026). [Peer-reviewed.]

[14] J. Alm, K. M. Bloomquist y M. McKee, "When You Know Your Neighbour Pays Taxes: Information, Peer Effects and Tax Compliance," *Fiscal Stud.*, vol. 38, no. 4, pp. 587–613, 2017, doi: `10.1111/1475-5890.12111`. URL: `https://doi.org/10.1111/1475-5890.12111` (acceso sep. 24, 2026). [Peer-reviewed.]

[15] L. S. Di Mauro, A. Pluchino y A. E. Biondo, "Tax evasion as a contagion game: evidences from an agent-based model," *Eur. Phys. J. B*, vol. 92, no. 5, art. 98, 2019, doi: `10.1140/epjb/e2019-90722-9`. URL: `https://doi.org/10.1140/epjb/e2019-90722-9` (acceso sep. 24, 2026). [Peer-reviewed.]

[16] OECD, *Building Tax Culture, Compliance and Citizenship: A Global Source Book on Taxpayer Education*. Paris, France: OECD Publishing, 2015. URL: `https://www.oecd.org/content/dam/oecd/en/publications/reports/2015/06/building-tax-culture-compliance-and-citizenship_g1g4abd3/9789264205154-en.pdf` (acceso sep. 24, 2026). [Organismo internacional.]

[17] OECD, *Digital Services: Supporting SMEs to Get Tax Right*. Paris, France: OECD Publishing, sep. 2022. URL: `https://www.oecd.org/en/publications/digital-services_7bd95d83-en.html` (acceso sep. 24, 2026). [Organismo internacional.]

[18] Latinobarómetro, *Informe Latinobarómetro* (serie anual; variable de moral tributaria/justificación de la evasión). URL: `https://www.latinobarometro.org/lat.jsp` (acceso sep. 24, 2026; verificación de ola específica pendiente manualmente). [Encuesta regional.]

[19] Cámara Nacional de Comercio, *Tercera Encuesta Nacional sobre Percepción del Comercio Ilícito y Contrabando en Chile*, 2025. Cit. en PGCT 2026 p. 45. URL: `https://cnc.cl/noticias_ocis/alcaldes-de-diversas-comunas-de-la-region-metropolitana-comentaron-los-resultados-de-la-tercera-encuesta-de-percepcion-del-comercio-ilicito-de-la-cnc/` (acceso sep. 24, 2026). [Encuesta gremial.]

[20] L. Hernández y A. Cabrera, "Costo del crimen en Chile y Latinoamérica: 1999–2023," CLAPES UC, Santiago, Chile, jun. 2025. Reseña: "La factura de la delincuencia: Chile pierde 2,6% del PIB al año". URL: `https://clapesuc.cl/en-los-medios/la-factura-de-la-delincuencia-chile-pierde-26-del-pib-al-ano` (acceso sep. 24, 2026). [Centro de estudios; contexto, no calibración directa.]

### Fuentes del repositorio (no web, para trazabilidad interna)

[R-a] `Recursos/SII_PGCT_2026.pdf` (55 pp., Adobe Illustrator 30.1, ene. 2026) — fuente primaria local de §§a–c, f.
[R-b] `Recursos/RESUMEN_SESION_ceiling_y_calibracion_chile.md` (2026-09-24) — diagnóstico del techo, headroom, MDE, criterio "mover cobertura; fijar dotación".
[R-c] `Recursos/respuesta_scibot.txt` — síntesis ABM con referencias [1]–[10] (Andrei, Hokamp, Hokamp–Pickhardt, Di Mauro, Hashimzade×3, DeBacker, Beer, Alm–Bloomquist–McKee); base de §§f, h, i.

---

## Rerun Inputs

```yaml
workflow: firecrawl-research-papers + academic-research-writer
topic: calibración a Chile de ABM Tax Evasion con memoria institucional (cobertura SII, dotación, universo, sanciones, tasas, prescripción, decaimiento disuasivo, precedentes ABM)
target_count: 20 (14 peer-reviewed + 3 informes oficiales SII/INE + 1 ley + 2 organismos internacionales + encuestas)
output: Recursos/JUSTIFICACION_calibracion_chile.md
access_date: 2026-09-24
model: ABM_TESIS_CHANGES.nlogo (NetLogo 6.4.0); rama réplica Canessa intacta
base_actual: {nr-tax-payers: 500, nr-auditors: 20, actual-audit-rate: 0.20, tax-rate: 0.27, penalty-rate: 1.5, learning-rate: 0.05, initial-Risk-aversion: 0.5, treshold-influence-income: 1.65, period-frauds: [1,5], institutional-memory: [1,5,10,15], audit-noise: 0}
propuesta_chile: {actual-audit-rate: [0.01,0.02,0.05,0.10] centro 0.02-0.03, nr-auditors: 20 fijo, nr-tax-payers: 500 (900 robustez), penalty-rate: 1.5 centro [1.0,1.5,2.5], tax-rate: 0.27 [0.19 robustez], initial-Risk-aversion: 0.5, learning-rate: 0.05, treshold-influence-income: 1.65, institutional-memory: [1,3,5,7,15], audit-noise: [0,0.1,0.3,0.5]}
design: {reps: ">=30", ticks: "30k-50k", model_formula: "PIR ~ k x PF x estrategia", pir_objetivo_base: "0.5-0.6", report: "dual (replica + chile)"}
verify: ["re-leer este archivo y confirmar que toda cita tiene URL + fecha", "copiar arts. 53/97/200-201 BCN al anexo de tesis", "fijar ola Latinobarómetro citada", "pre-registrar rango audit-rate antes de correr"]
```
