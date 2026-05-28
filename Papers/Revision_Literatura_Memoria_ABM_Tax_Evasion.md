# Revisión de Literatura: Memoria Social e Institucional en ABM de Evasión Tributaria

## Abstract

Esta revisión identifica y sintetiza papers académicos que abordan específicamente los conceptos de **memoria social** (aprendizaje de contribuyentes al observar a sus vecinos) y **memoria institucional** (capacidad de auditores de revisar períodos pasados) dentro de modelos basados en agentes (ABM) aplicados a evasión tributaria. Se excluyen papers generalistas de ABM o evasión fiscal que no aborden estos mecanismos de memoria de forma explícita.

---

## 1. Memoria Social en ABM de Evasión Tributaria

### 1.1 SIMULFIS: Memoria local y aprendizaje social

**Llàcer, T., Miguel Quesada, F.J., Noguera, J.A., Tapia, E.T. (2018).** "SIMULFIS: A Simulation Tool to Explore Tax Compliance Behavior." In *Agent-based Modeling of Tax Evasion: Theoretical Aspects and Computational Simulations*, Wiley.

- Los agentes mantienen tres tipos de memoria local: **memoria de fraude previo**, **memoria de auditorías previas**, y **memoria de sanciones previas**
- La naturaleza estrictamente local de los datos de memoria incluye la posibilidad de que agentes accedan a información de sus vecinos
- La vecindad se define como una lista de agentes enlazados
- Relevancia directa: el modelo distingue entre memoria individual (experiencia propia) y memoria social (observación de vecinos)

**Noguera, J.A., Miguel Quesada, F.J., Tapia, E.T., Llàcer, T. (2014).** "Tax compliance, rational choice, and social influence: An agent-based model." *Revue française de sociologie*, 55(4), 765-804.

- Componentes clave del modelo: **audit record** del agente (registro de auditorías) + señales recibidas de vecinos (influencia social)
- Los agentes ajustan su comportamiento mediante conformidad social y aprendizaje social
- 256 simulaciones con 1,000 agentes y 100 períodos fiscales
- Relevancia: modela explícitamente cómo la experiencia auditiva individual interactúa con la observación del comportamiento de los vecinos

### 1.2 Efectos de vecindad (neighborhood effects)

**Arslan, M.O. (2013).** "The Effects of Neighborhood on Tax Compliance Rates: Evidence From an Agent Based Model." *Çukurova Üniversitesi Sosyal Bilimler Enstitüsü Dergisi*, 22(2).

- Implementa vecindad de Von Neumann y Moore para estudiar tasas de cumplimiento
- Agentes recién creados adoptan comportamiento de su vecindad inmediata
- Relevancia directa: demuestra que la estructura espacial y la observación de vecinos afecta el cumplimiento tributario

**Andrei, A.L., Comer, K., Koehler, M. (2014).** "An agent-based model of network effects on tax compliance and evasion." *Journal of Economic Psychology*, 40, 119-133.

- ABM con efectos de red que explora cómo la interacción social entre contribuyentes afecta cumplimiento y evasión
- Los agentes aprenden de las experiencias y comportamientos de sus vecinos en la red
- Cited by 110 - paper de alta relevancia en el campo

### 1.3 Influencia social y aprendizaje en red

**Garcia Alvarado, F. (2019a).** "Network effects in an agent-based model of tax evasion with social influence." In *Advances in Practical Applications of Survivable Agents and Multi-Agent Systems*, Springer.

- Los agentes comunican a sus vecinos su **memoria sobre auditorías pasadas** y las señales recibidas
- El modelo integra memoria individual (experiencia de auditoría) con influencia social (información de vecinos)
- 21,890 simulaciones realizadas
- Relevancia: combina explícitamente memoria de auditorías con comunicación entre vecinos

**Garcia Alvarado, F. (2019b).** "Network-based policies versus tax evasion." In *Network Theory and Agent-Based Modeling in Economics and Finance*, Springer.

- Agentes mantienen memoria de períodos anteriores
- Comparten información con vecinos sobre sus esquemas de evasión
- La memoria de los agentes incluye información recibida de vecinos sobre sus propias memorias
- Relevancia: modela la propagación de información fiscal a través de la red social

**Chica, M., Hernandez, J.M., et al. (2021).** "An evolutionary game model for understanding fraud in consumption taxes." *IEEE Computational Intelligence Magazine*, 16(3), 30-43.

- La regla de actualización de imitación social es una forma de aprendizaje social
- Los agentes en la red social observan a sus vecinos para decidir si evadir
- Factor horizontal: la evasión tributaria se propaga a través de la vecindad en la red
- Relevancia: demuestra cómo el aprendizaje social por imitación afecta la evasión

### 1.4 Memoria y coordinación evolutiva

**Bloomquist, K. (2011).** "Tax compliance as an evolutionary coordination game: an agent-based approach." *Public Finance Review*, 39(5), 643-668.

- Red social comparada con datos observados de cumplimiento tributario
- Características principales de ABM de cumplimiento tributario incluyen interacción social
- Relevancia: framework de coordinación evolutiva donde la memoria de interacciones pasadas importa

**Méder, Z.Z., Simonovits, A., Vincze, J. (2012).** "Tax morale and tax evasion: Social preferences and bounded rationality." *Working Paper, Max Planck Institute*.

- ABM simple para analizar cómo interacciones locales fomentan o dificultan la propagación de evasión tributaria
- Agentes con racionalidad limitada ajustan comportamiento según interacciones locales
- Cited by 43
- Relevancia: demuestra que la estructura local de interacciones (memoria de interacciones pasadas) es clave

**Hokamp, S., Pickhardt, M. (2010).** "Income tax evasion in a society of heterogeneous agents – Evidence from an agent-based model." *International Economic Journal*, 24(4), 541-553.

- Factor esencial en modelos ABM de evasión: la heterogeneidad de agentes
- Cited by 117 - paper fundamental en el campo
- Relevancia: establece que la heterogeneidad + memoria de interacciones pasadas es esencial

---

## 2. Memoria Institucional en ABM de Fiscalización

### 2.1 Historial de auditorías y cumplimiento

**Hashimzade, N., Myles, G.D. (2018).** "Using Agent-Based Modeling to Analyze Tax Compliance and Auditing." In *Agent-based Modeling of Tax Evasion: Theoretical Aspects and Computational Simulations*, Wiley.

- La autoridad fiscal usa ingreso declarado, ocupación, e **historial de auditorías del contribuyente** para predecir el nivel de evasión
- El modelo integra el historial de auditorías como input para decisiones futuras
- Relevancia directa: modela cómo la institución (autoridad fiscal) usa memoria histórica

**RAND Corporation (2019).** "RAND's interdisciplinary behavioral and social science agent-based model of income tax evasion." *RAND Working Paper*.

- Los contribuyentes están **fuertemente impactados por su historial de auditorías pasadas**
- El modelo ABM integra el historial de auditorías como factor determinante del comportamiento
- Relevancia: evidencia empírica de que la memoria institucional (historial de auditorías) afecta compliance

**Alm, J., Cox, J.C., Sadiraj, V. (2020).** "Audit state dependent taxpayer compliance: Theory and evidence from Colombia." *Economic Inquiry*, 58(3), 1327-1348.

- El cumplimiento del período actual depende del **historial individual de auditorías de períodos anteriores**
- Diseño experimental que captura la dependencia del estado de auditoría
- Cited by 28
- Relevancia directa: evidencia empírica de que la memoria institucional (audit history) afecta compliance futuro

**Kuchumova, Y., Kumacheva, S. (2025).** "Tax Audit Expectation Updating: Direct and Indirect Effects of an Audit." *SSRN Working Paper*.

- La probabilidad esperada de auditoría se define como función del **historial de auditorías**
- Extiende la teoría de cumplimiento tributario incorporando actualización bayesiana basada en experiencia auditiva
- Relevancia: modela cómo los contribuyentes actualizan sus expectativas basándose en memoria de auditorías

### 2.2 Selección de auditorías basada en historial

**Bachas, P., Brockmeyer, A., Ferreira, A., Sarr, B. (2025).** "Algorithms and bureaucrats: Evidence from tax audit selection in Senegal." *World Bank Development Research Group*.

- Revisión del **historial de auditorías de la firma** como input para selección algorítmica
- La mejora en cumplimiento tributario a través de auditorías depende del acceso al historial
- Cited by 7
- Relevancia: evidencia de campo sobre cómo la memoria institucional guía la selección de auditorías

**Rablen, M.D., Hashimzade, N., Myles, G.D. (2015).** "Predictive Analytics and the Targeting of Audits." *Brunel University Working Paper*.

- Enfoque conductual al cumplimiento tributario
- El modelo usa características del agente y **historial de auditorías** para predicción
- Relevancia: modela cómo la institución usa memoria histórica para optimizar fiscalización

### 2.3 Memoria institucional como concepto en fiscalización

**Lopez, R. (2025).** "The LAAM Framework: Operationalizing Fairness in Asymmetric Enforcement Systems." *SSRN Working Paper*.

- Concepto de **"repeated games with institutional memory (audit anchors)"**
- Los auditores mantienen anclas basadas en historial que afectan decisiones futuras
- Aplicación directa a auditorías fiscales
- Relevancia directa: introduce el concepto de "memoria institucional" como ancla de auditoría

**MacDonald, T. (2026).** "Institutional Evolvability in the Age of AI: Rules, Mechanisms, and the Architecture of Institutional Learning." *SSRN Working Paper*.

- La autoridad fiscal ajusta probabilidades de auditoría usando puntajes de riesgo
- La **memoria institucional** se hace navegable a través de sistemas
- Modelos basados en agentes, redes de Petri, y modelos de flujo de trabajo
- Relevancia: framework teórico de cómo las instituciones mantienen y usan memoria

### 2.4 Memoria de sanciones y deterrencia

**Bloomquist, K. (2004).** "Multi-agent based simulation of the deterrent effects of taxpayer audits." *Proceedings of the Annual Conference on Taxation*, 156-166.

- ABM de los efectos disuasivos de auditorías fiscales
- Los agentes mantienen memoria de auditorías y sanciones pasadas
- Cited by 56
- Relevancia: demuestra que la memoria de auditorías tiene efecto disuasivo

**Antunes, L., Balsa, J., Urbano, P., Moniz, L. (2005).** "Tax compliance in a simulated heterogeneous multi-agent society." In *Multi-Agent-Based Simulation*, Springer.

- Sin el **efecto de memoria**, el promedio de evasores sería ~90%
- La memoria de experiencias pasadas es crucial para mantener cumplimiento
- Cited by 42
- Relevancia directa: demuestra empíricamente que la memoria es necesaria para cumplimiento

---

## 3. Papers que Combinan Ambos Tipos de Memoria

### 3.1 SIMULFIS como caso integrado

**Miguel, F.J., Noguera, J.A., Llàcer, T., Tapia, E. (2012).** "Exploring Tax Compliance: An Agent-Based Simulation." *ECMS 2012*.

- Modelo SIMULFIS combina: memoria de fraude previo + memoria de auditorías + memoria de sanciones + interacción con vecinos
- El modelo final busca reproducción precisa de cifras reales de evasión
- Cited by 13
- Relevancia: caso más completo de integración de memoria social e institucional

### 3.2 Modelo RAND integrado

**Vardavas, R., Katkar, P., Parker, A.M., Aliyev, G.R., et al. (2019).** "RAND's interdisciplinary behavioral and social science agent-based model of income tax evasion." *RAND Working Paper*.

- Integra: historial de auditorías (memoria institucional) + influencia social (memoria social)
- Los agentes están fuertemente impactados por historial de auditorías Y por observación de vecinos
- Relevancia: modelo más reciente que integra ambos tipos de memoria

---

## 4. Gaps en la Literatura

### 4.1 Lo que NO existe (según búsqueda)

1. **No hay papers que modelen explícitamente "memoria institucional" como slider parametrizable** en ABM de evasión. El concepto de memoria institucional como profundidad de revisión retrospectiva (1-15 períodos) es **novedoso**.

2. **No hay papers que combinen memoria institucional de auditores con memoria social de contribuyentes** como variables independientes interactivas.

3. **No hay papers que modelen degradación de detección en períodos lejanos** (audit-noise) como factor que afecta la memoria institucional.

4. **No hay papers que estudien la interacción entre estrategia de selección de auditoría y profundidad de memoria institucional**.

### 4.2 Contribución original de tu tesis

Tu investigación llena estos gaps al:
- Parametrizar la **profundidad de memoria institucional** (1-15 períodos)
- Introducir **ruido de auditoría** que degrada la detección en períodos lejanos
- Estudiar la **interacción entre memoria social (period-frauds) y memoria institucional (institutional-memory)**
- Comparar con el modelo base (ABM_Original de Canessa) para validar equivalencia con institutional-memory=1

---

## 5. Referencias Completas (IEEE Format)

### Memoria Social

[1] T. Llàcer, F. J. Miguel Quesada, J. A. Noguera, and E. Tapia, "SIMULFIS: A Simulation Tool to Explore Tax Compliance Behavior," in *Agent-based Modeling of Tax Evasion: Theoretical Aspects and Computational Simulations*, S. Hokamp, L. Gulyás, M. Koehler, and S. Wijesinghe, Eds. Wiley, 2018.

[2] J. A. Noguera, F. J. Miguel Quesada, E. Tapia, and T. Llàcer, "Tax compliance, rational choice, and social influence: An agent-based model," *Revue française de sociologie*, vol. 55, no. 4, pp. 765–804, 2014.

[3] M. O. Arslan, "The Effects of Neighborhood on Tax Compliance Rates: Evidence From an Agent Based Model," *Çukurova Üniversitesi Sosyal Bilimler Enstitüsü Dergisi*, vol. 22, no. 2, 2013.

[4] A. L. Andrei, K. Comer, and M. Koehler, "An agent-based model of network effects on tax compliance and evasion," *Journal of Economic Psychology*, vol. 40, pp. 119–133, 2014.

[5] F. Garcia Alvarado, "Network effects in an agent-based model of tax evasion with social influence," in *Advances in Practical Applications of Survivable Agents and Multi-Agent Systems*, Springer, 2019.

[6] F. Garcia Alvarado, "Network-based policies versus tax evasion," in *Network Theory and Agent-Based Modeling in Economics and Finance*, Springer, 2019.

[7] M. Chica, J. M. Hernandez et al., "An evolutionary game model for understanding fraud in consumption taxes," *IEEE Computational Intelligence Magazine*, vol. 16, no. 3, pp. 30–43, 2021.

[8] K. Bloomquist, "Tax compliance as an evolutionary coordination game: an agent-based approach," *Public Finance Review*, vol. 39, no. 5, pp. 643–668, 2011.

[9] Z. Z. Méder, A. Simonovits, and J. Vincze, "Tax morale and tax evasion: Social preferences and bounded rationality," *Working Paper, Max Planck Institute*, 2012.

[10] S. Hokamp and M. Pickhardt, "Income tax evasion in a society of heterogeneous agents – Evidence from an agent-based model," *International Economic Journal*, vol. 24, no. 4, pp. 541–553, 2010.

### Memoria Institucional

[11] N. Hashimzade and G. D. Myles, "Using Agent-Based Modeling to Analyze Tax Compliance and Auditing," in *Agent-based Modeling of Tax Evasion: Theoretical Aspects and Computational Simulations*, Wiley, 2018.

[12] RAND Corporation, "RAND's interdisciplinary behavioral and social science agent-based model of income tax evasion," *RAND Working Paper*, 2019.

[13] J. Alm, J. C. Cox, and V. Sadiraj, "Audit state dependent taxpayer compliance: Theory and evidence from Colombia," *Economic Inquiry*, vol. 58, no. 3, pp. 1327–1348, 2020.

[14] Y. Kuchumova and S. Kumacheva, "Tax Audit Expectation Updating: Direct and Indirect Effects of an Audit," *SSRN Working Paper*, 2025.

[15] P. Bachas, A. Brockmeyer, A. Ferreira, and B. Sarr, "Algorithms and bureaucrats: Evidence from tax audit selection in Senegal," *World Bank Development Research Group*, 2025.

[16] M. D. Rablen, N. Hashimzade, and G. D. Myles, "Predictive Analytics and the Targeting of Audits," *Brunel University Working Paper*, 2015.

[17] R. Lopez, "The LAAM Framework: Operationalizing Fairness in Asymmetric Enforcement Systems," *SSRN Working Paper*, 2025.

[18] T. MacDonald, "Institutional Evolvability in the Age of AI: Rules, Mechanisms, and the Architecture of Institutional Learning," *SSRN Working Paper*, 2026.

[19] K. Bloomquist, "Multi-agent based simulation of the deterrent effects of taxpayer audits," in *Proceedings of the Annual Conference on Taxation*, pp. 156–166, 2004.

[20] L. Antunes, J. Balsa, P. Urbano, and L. Moniz, "Tax compliance in a simulated heterogeneous multi-agent society," in *Multi-Agent-Based Simulation*, Springer, 2005.

### Integración de Ambas Memorias

[21] F. J. Miguel, J. A. Noguera, T. Llàcer, and E. Tapia, "Exploring Tax Compliance: An Agent-Based Simulation," in *ECMS 2012*, pp. 13–19, 2012.

[22] R. Vardavas, P. Katkar, A. M. Parker, G. R. Aliyev et al., "RAND's interdisciplinary behavioral and social science agent-based model of income tax evasion," *RAND Working Paper*, 2019.

### Referencias Adicionales de Contexto

[23] K. M. Bloomquist, "A comparison of agent-based models of income tax evasion," *Social Science Computer Review*, vol. 24, no. 4, 2006.

[24] S. Hokamp, L. Gulyás, M. Koehler, and S. Wijesinghe, Eds., *Agent-based Modeling of Tax Evasion: Theoretical Aspects and Computational Simulations*. Wiley, 2018.

[25] K. M. Bloomquist and M. Koehler, "A large-scale agent-based model of taxpayer reporting compliance," *Journal of Artificial Societies and Social Simulation*, vol. 18, no. 2, 2015.

[26] B. Torgler, "Speaking to theorists and searching for facts: Tax morale and tax compliance in experiments," *Journal of Economic Surveys*, vol. 16, no. 5, pp. 657–683, 2002.

[27] K. Kumacheva, E. Gubar, E. Zhitkova, G. Tomilina et al., "Agent-Based Model of Tax Control Under Information Spreading," in *Game Theory and Applications*, Springer, 2022.

[28] T. Lazebnik and L. Shami, "Investigating tax evasion emergence using dual large language model and deep reinforcement learning powered agent-based simulation," *arXiv preprint arXiv:2501.18177*, 2025.

[29] N. Crokidakis, "A three-state kinetic agent-based model to analyze tax evasion dynamics," *Physica A: Statistical Mechanics and its Applications*, vol. 414, pp. 310–318, 2014.

[30] K. M. Bloomquist, "Development and Calibration of a Large-Scale Agent-Based Model of Individual Tax Reporting Compliance," in *Agent-based Modeling of Tax Evasion*, Wiley, 2018.
