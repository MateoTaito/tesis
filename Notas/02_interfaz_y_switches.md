# 02 — Interfaz y switches nuevos (14 oct 2026)

## Solapamientos de la UI (corregido, sin commitear al 15 oct)

El commit `53c4a42` ("Enhancing visualization") agregó 4 widgets en y 520–700,
zona ocupada por `setup`, `go` y `max-nr-simulated-steps`. Chequeo por script:
**6 solapamientos** en 22 widgets. Reordenamiento (columna x 40–229):

- `setup` + `go` lado a lado en una fila (y 525–558),
- `max-nr-simulated-steps` debajo a ancho completo (565–598),
- `visual-fraud-spread?` (605–638), leyenda (640–710),
  `start-all-honest?` (717–750), su textbox (752–790).

Post-fix: 24 widgets, 0 solapamientos; smoke headless idéntico al bit
(`PIR 0.5215...`), archivo íntegro. Script de chequeo en `/tmp/opencode/check_overlap.py`
(no está en el repo; rescatar si se vuelve a tocar la UI).

## Switch `seed-fraud?` (nuevo, default OFF)

Paciente cero para observar contagio: con ON, al inicio del 2do tick (`ticks = 1`,
antes de captura de historial y de `make-audit`) un contribuyente al azar pasa a
evasión total (`pct-income-report = 0`, `income-reported = 0`). El 0 es absorbente
(multiplicativo), el paciente cero nunca se reforma solo. Con OFF no ejecuta nada
(ni RNG): equivalencia con el original intacta (verificado: OFF reproduce el smoke).
Combinación sugerida para demo visual: `start-all-honest?` ON + `visual-fraud-spread?` ON.
Documentado en `Docu/Especificación...memoria_institucional.md` §4.2.
Verificación headless (métrica `count ... [pct-income-report = 0]`): OFF → 0, ON → 1.

## Advertencia: defaults que heredan los experimentos

Ningún XML BehaviorSpace embebido fija los switches: las corridas heredan la interfaz
(`visual-fraud-spread?` OFF, `start-all-honest?` **ON**, `seed-fraud?` OFF).
`start-all-honest?` ON implica partir de honestidad total, distinto del setup aleatorio
del original y de los experimentos pre-Oct-2026. Fijarlo explícito en cada XML nuevo.
(UI sin cambios desde el fix del 14 oct; validada con 0 solapamientos por script.)
