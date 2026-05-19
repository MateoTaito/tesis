globals [max-pop-size  global-audit-perc-eff PIAR_10000 PRA_10000 acum_frauds_detected acum_frauds_perpretated acum_frauds_perpretated_all_ags PIAR_ticks RA_ticks rec_PIAR_ticks rec_RA_ticks
        SS_PIAR SS_RA final_frauds_detected final_frauds_perpretated final_frauds_perpretated_all_ags

  ;otras variables para medir
  acum_prom_PIAR_ags
  acum_prom_RA_ags
  acum_delta_inc_real_inc_report
]
breed [tax-payers tax-payer]
breed [auditors auditor]
tax-payers-own [ pct-income-report income audit? income-reported after-tax-income risk-aversion fraud-detected? fiscal-risk-score fraud-detect-hist under_rep_income income-history audited-periods]
auditors-own [pct-audit-efficiency selected-txp-audit nr-audits cumulative-nr-audits cumulative-nr-audits-OK]

to prueba
 repeat 0
  [show "pase 1 vez"]

end
to startup

set max-pop-size (max-pxcor + 1) * (max-pycor + 1)

end


to go

  if ticks = max-nr-simulated-steps [stop]

  set PIAR_ticks lput mean [pct-income-report] of tax-payers PIAR_ticks

  set RA_ticks lput  mean [risk-aversion] of tax-payers RA_ticks

  if rec_PIAR_ticks and length PIAR_ticks = 2
  [
    let delta last PIAR_ticks - first PIAR_ticks ;show delta
   if  abs delta < .000001 and delta > 0  [show word "PIAR = " ticks set rec_PIAR_ticks false set SS_PIAR ticks ]
   set PIAR_ticks []
  ]

  if rec_RA_ticks and length RA_ticks = 2
  [
    let delta last RA_ticks - first RA_ticks
   if  abs delta < .0005 and delta > 0  [show word "RA = " ticks set rec_RA_ticks false set SS_RA ticks]
   set RA_ticks []
  ]

  if ticks = 10000 [set PIAR_10000 mean [pct-income-report] of tax-payers set PRA_10000 mean [risk-aversion] of tax-payers]
  make-audit

  if ticks >= 25000 [set acum_prom_PIAR_ags acum_prom_PIAR_ags + mean [pct-income-report] of tax-payers
                     set acum_prom_RA_ags acum_prom_RA_ags + mean [risk-aversion] of tax-payers
    set acum_delta_inc_real_inc_report acum_delta_inc_real_inc_report + sum [under_rep_income] of tax-payers


  ]

  ;ask tax-payers [show (word "INC = " income " PIR = " pct-income-report " IN_REP = " income-reported " AUD? = " audit? " ATI = " after-tax-income)]
  auditors-adjust-pct-eff
  tax-payers-adjust-pct-inc-rep

  ; guardar historial de ingresos antes de reasignar (para memoria institucional)
  ask tax-payers [
    set income-history lput (list income income-reported) income-history
    ; mantener solo los últimos institutional-memory registros
    if length income-history > institutional-memory [
      set income-history sublist income-history (length income-history - institutional-memory) (length income-history)
    ]
  ]

  ask tax-payers [set income log-normal-x 16 7] ; podría mantenerse el income inicial en toda la simulacion
  ;ask tax-payers [if risk-aversion > 1 or risk-aversion < 0 [show risk-aversion  show income ]]
  ; ask tax-payers [if pct-income-report > 1 or pct-income-report < 0 [show  pct-income-report]]
  tick
end

to tax-payers-adjust-pct-inc-rep
  ; 1ERA VERSION MULTIPLICATIVA ************************************************************



  ask tax-payers
  [

    let txp-neighbors  tax-payers-on neighbors
    ;show txp-neighbors
    let nr-neighbors-audited count (txp-neighbors with [audit? = true])
    let  nr-neighbors-fraud-detected count (txp-neighbors with [fraud-detected? = true])
    ;show nr-neighbors-audited show nr-neighbors-fraud-detected
  ; debería ajustar el risk-aversion por valor del penalty por income no reportado y por vecinos auditados y vecinos fraude detectado
   let possible-penalty (income - income-reported) * penalty-rate
    ;show risk-aversion
   set risk-aversion txp-adjust-risk-aversion risk-aversion possible-penalty nr-neighbors-audited nr-neighbors-fraud-detected
   ;show risk-aversion
    ;************************* VSERION MULTIPLICATIVA funciona bien y diámica es interenaste **************************
    ifelse audit?
    [ ; got audited
      ifelse fraud-detected?
      [
        set  pct-income-report pct-income-report * 1.005 ^ risk-aversion ; and fraud detected => increment % income reported 1.0005
      ]
      [
        set  pct-income-report pct-income-report * 0.998 ^ (1 - risk-aversion) ; and fraud NOT detected => decrement % income reported 0.9998
      ]

    ]
    [


     set  pct-income-report pct-income-report * 0.999 ^ (1 - risk-aversion) ; didn't get audited => decrement % income reported 0.9999

    ]

    set pct-income-report ifelse-value pct-income-report > 1 [1] [pct-income-report]
    ;set audit? false
    set color color-perc-inc-rep pct-income-report
  ]

  ask tax-payers [set audit? false set fraud-detected? false] ; para reinicializar
;  if ticks mod period-frauds = 0 and ticks > 0
;  [ask tax-payers [set fraud-detect-hist [] ] ]

 ;  2DA VERSION ADITIVA no funciona bien => todos los txps se van a 0% income to report************************************************************************
  ; para que funcione hay que hacer que el incremento en pct-income-report sea muy grande en comparación con su decremento (ordenes de magnitud)
  ;NOTAR: la dinámica del promedio pct-income-report cambia: 1ero crece, luego baja. En cambio en versión multiplicativa es al revés: 1ero baja., luego crece
;  ask tax-payers
;  [
;    let txp-neighbors  tax-payers-on neighbors
;    ;show txp-neighbors
;    let nr-neighbors-audited count (txp-neighbors with [audit? = true])
;    let  nr-neighbors-fraud-detected count (txp-neighbors with [fraud-detected? = true])
;    ;show nr-neighbors-audited show nr-neighbors-fraud-detected
;  ; debería ajustar el risk-aversion por valor del penalty por income no reportado y por vecinos auditados y vecinos fraude detectado
;   let possible-penalty (income - income-reported) * penalty-rate
;   set risk-aversion txp-adjust-risk-aversion risk-aversion possible-penalty nr-neighbors-audited nr-neighbors-fraud-detected
;
;
;
;
;    ifelse audit?
;    [ ; got audited
;      ifelse fraud-detected?
;      [
;        set  pct-income-report pct-income-report + .05 * (1 + risk-aversion / 10); and fraud detected => increment % income reported
;      ]
;      [
;        set  pct-income-report pct-income-report - 0.0007 * (1 - risk-aversion / 10) ; and fraud NOT detected => decrement % income reported
;      ]
;
;    ]
;    [
;
;
;     set  pct-income-report pct-income-report - 0.0005 * (1 - risk-aversion / 10) ; didn't get audited => decrement % income reported
;
;    ]
;
;    set pct-income-report ifelse-value pct-income-report > 1 [1] [pct-income-report]
;    set pct-income-report ifelse-value pct-income-report < 0 [0] [pct-income-report]
;    set audit? false
;    set color color-perc-inc-rep pct-income-report
;  ]
;ask tax-payers [set audit? false set fraud-detected? false] ; para reinicializar

end


; ESTO ES LO MÁS INTERESANTE Y NUEVO EN ESTE MODELO TAX-EVASION_1_1
to-report txp-adjust-risk-aversion [r-av p-penal nna nnfd]

  let tax-p-neigh-8 sort tax-payers-on neighbors
  let weights-income 0
  let weights-sanction 0
  let neighb-influence 0
  let nr-neighbs length tax-p-neigh-8
  let income-own-txp [income] of self
;  show income
;  show income-own-txp
;show tax-p-neigh-8

  foreach tax-p-neigh-8
  [  t ->
    let income-neigh-perceived ([income] of t + random-normal 0 2)
    if income-neigh-perceived < 0 [set income-neigh-perceived 0]
    let ratio-incomes income-neigh-perceived / income-own-txp
    if ratio-incomes >= treshold-influence-income
    [set weights-income  weights-income + 1]

;    if sum [fraud-detect-hist] of t > 0
;    [set weights-sanction  weights-sanction + 1]

      let sum-nr-frauds-detected sum [fraud-detect-hist] of t
      let ignore-next-frauds false
      ;show sum-nr-frauds-detected
    repeat sum-nr-frauds-detected
    [
      if random-float 1 < .7 and not ignore-next-frauds; si al vecino le detectaron un fraude (en la ventana temporal) existe un 70% que el txp lo sepa por cada fraude
      [set weights-sanction  weights-sanction + 1 set ignore-next-frauds true  ]

    ]



    ]




  let total-influence  weights-income +  weights-sanction

  if nr-neighbs > 0
  [set neighb-influence total-influence / nr-neighbs ]

  let delta_r_aver learning-rate * (neighb-influence - risk-aversion)
  let risk-aversion-aux risk-aversion + delta_r_aver

 (ifelse risk-aversion-aux > 1
  [set risk-aversion-aux 1]
  risk-aversion-aux < 0
  [set risk-aversion-aux 0] )

  ;if risk-aversion-aux > 1 [show risk-aversion-aux show risk-aversion show tax-p-neigh-8  show income show weights-income show weights-sanction]
  report risk-aversion-aux ; ****************************************
end

to auditors-adjust-pct-eff
  let to-date-nr-audits sum [cumulative-nr-audits] of auditors
  let to-date-nr-audits-OK sum [cumulative-nr-audits-OK] of auditors
  set global-audit-perc-eff to-date-nr-audits-OK / to-date-nr-audits
;  show to-date-nr-audits
;  show to-date-nr-audits-OK
  ;show global-audit-perc-eff
  ; ******************************** 1ERA VERSION *******************
;  ask auditors
;  [
;    if cumulative-nr-audits >= 10
;    [
;      let pct-audit-eff-to-date cumulative-nr-audits-OK / cumulative-nr-audits
;
;      set pct-audit-efficiency  ifelse-value pct-audit-eff-to-date > global-audit-perc-eff   [ pct-audit-efficiency * 1.001 ] [pct-audit-efficiency * 0.999]
;      ; ARBITRARIO LOS PORCENTAJES INCREMENTO/BAJADA
;      set pct-audit-efficiency  ifelse-value pct-audit-eff-to-date > 1   [ 1 ] [pct-audit-efficiency ]
;    ]
;
;  ]
; ********************************* 2DA VERSION **********************************************
   ask auditors
  [
    if cumulative-nr-audits > 0 and cumulative-nr-audits mod 100 = 0 ;if ticks > 0 and ticks mod 100 = 0;
    [
      let pct-audit-eff-to-date cumulative-nr-audits-OK / cumulative-nr-audits

      set pct-audit-efficiency  ifelse-value (pct-audit-eff-to-date < global-audit-perc-eff * 0.75)  [   0.5 + random-float 0.5] [pct-audit-efficiency ]
      ; ARBITRARIO LOS PORCENTAJES INCREMENTO/BAJADA
      set cumulative-nr-audits 0
      set cumulative-nr-audits-OK 0
    ]

  ]


end

to make-audit
  ask tax-payers [set under_rep_income 0]
  if ticks >= 25000
  [ ask tax-payers [if income-reported < income [set acum_frauds_perpretated_all_ags acum_frauds_perpretated_all_ags + 1 ]] ]
  let txp-sel-audit select-tax-p-audit
  ;let total-nr-audits count txp-sel-audit
  ;show txp-sel-audit
   select-auditors txp-sel-audit
  ;ask auditors [show selected-txp-audit]
  ask auditors with [nr-audits > 0]
  [
    let nr-audits-done 1
    foreach selected-txp-audit
    [  x ->
      ; auditar con memoria institucional: revisar múltiples períodos pasados
      ; period-offset = 0 es el período actual, 1 es el anterior, etc.
      let total-penalty 0  ; acumular penalidades de todos los períodos
      let detected-any-fraud false
      let num-periods-to-audit min list institutional-memory (length [income-history] of x + 1)

      ; loop sobre cada período dentro de la ventana de memoria institucional
      let period-offset 0
      repeat num-periods-to-audit
      [
        ; verificar si este período ya fue auditado
        if not [has-period-been-audited period-offset] of x
        [
          ; aplicar ruido histórico a la eficiencia
          let noise-reduction calculate-historical-noise period-offset
          let effective-efficiency ([pct-audit-efficiency] of self) * nr-audits-done * (1 - noise-reduction)

          ; verificar detección con ruido
          if effective-efficiency > random-float 1
          [
            ; obtener datos históricos del período
            let historical-data [get-income-history-entry period-offset] of x
            let hist-income item 0 historical-data
            let hist-income-reported item 1 historical-data

            ; verificar si hay fraude en este período
            if hist-income-reported < hist-income
            [
              ; fraude detectado en este período
              let period-penalty (hist-income - hist-income-reported) * penalty-rate
              set total-penalty total-penalty + period-penalty
              set detected-any-fraud true
              set cumulative-nr-audits-OK cumulative-nr-audits-OK + 1
            ]
          ]
        ]

        ; fatiga aumenta: 5% por cada período auditar (comentario: quizás revisarse)
        set nr-audits-done nr-audits-done - 0.05
        set period-offset period-offset + 1
      ]

      ; aplicar penalidad acumulada al período actual
      ask x [
        ifelse detected-any-fraud
        [
          let inc-w-penalty ( (1 - tax-rate) * income - total-penalty )
          set after-tax-income ifelse-value inc-w-penalty < 0 [0] [inc-w-penalty]
          set fraud-detected? true
          set fraud-detect-hist sliding-window fraud-detect-hist 1
          ; under_rep_income se calcula como el subreporte del período actual
          set under_rep_income (income - income-reported)
          if ticks >= 25000 [set acum_frauds_detected acum_frauds_detected + 1]
        ]
        [
          ; sin fraude detectado
          set after-tax-income income - tax-rate * income-reported
          set fraud-detect-hist sliding-window fraud-detect-hist 0
        ]

        ; marcar todos los períodos que fueron auditados
        let p-offset 0
        repeat min list institutional-memory (length income-history + 1)
        [
          add-period-to-audited p-offset
          set p-offset p-offset + 1
        ]
      ]

      ; contar fraude perpetrado (si hay subreporte en período actual)
      if [income-reported] of x < [income] of x and ticks >= 25000 [set acum_frauds_perpretated acum_frauds_perpretated + 1]
    ]

  ]

end

to select-auditors [tsa]
  ask auditors [set nr-audits 0 set selected-txp-audit []]
  let count-audits 0

  foreach shuffle sort tsa
  [
    x ->
    let available-auditor one-of auditors with [nr-audits = count-audits]

    ifelse available-auditor != nobody
    [
      ask available-auditor [set  selected-txp-audit lput x selected-txp-audit set nr-audits nr-audits + 1 set cumulative-nr-audits cumulative-nr-audits + 1]
    ]
    [
      set count-audits count-audits + 1
      ask one-of auditors [set  selected-txp-audit lput x selected-txp-audit set nr-audits nr-audits + 1 set cumulative-nr-audits cumulative-nr-audits + 1]
    ]

  ]

end


to-report select-tax-p-audit

  if tax-payer-audit-selection = "random"
  [  let tps n-of (round (actual-audit-rate * nr-tax-payers)) tax-payers
    ask tps [set audit? true ]
    report tps
  ]



  if tax-payer-audit-selection = "income-level"
  [
    let income-rep-median median [income-reported] of tax-payers
    let nr-txp-must-select round (actual-audit-rate * nr-tax-payers)

    let prelim-selected-txp up-to-n-of nr-txp-must-select tax-payers with [income-reported >= income-rep-median]
    ask prelim-selected-txp [set audit? true]
    let nr-txp-prelim-sel count prelim-selected-txp
    if nr-txp-prelim-sel = nr-txp-must-select
    [report  prelim-selected-txp ]

    let next-sel-txp up-to-n-of (nr-txp-must-select - nr-txp-prelim-sel) tax-payers with [audit? = false]
    let tps (turtle-set prelim-selected-txp next-sel-txp)
    ask tps [set audit? true ]
    report tps


  ]

  if tax-payer-audit-selection = "strategic"
  [
    ask tax-payers [set fiscal-risk-score (1 - pct-income-report) * income * (1 - risk-aversion)   ]
    let nr-txp-must-select round (actual-audit-rate * nr-tax-payers)
    let tps sort-on [(- fiscal-risk-score)] tax-payers

    set tps turtle-set sublist tps 0  nr-txp-must-select


    ask tps [set audit? true ]

    report tps


  ]
end

to setup
  clear-all
  set max-pop-size (max-pxcor + 1) * (max-pycor + 1)
  set PIAR_ticks [] set RA_ticks []
  set rec_PIAR_ticks true set rec_RA_ticks true
  setup-tax-payers nr-tax-payers
  setup-auditors nr-auditors
  reset-ticks


end

to setup-tax-payers [ntp]
  ask n-of  ntp patches [ sprout-tax-payers 1
  [
    set  shape "person"
    set pct-income-report  random-float 1
    set income log-normal-x 16 7
    set color color-perc-inc-rep pct-income-report
    set income-reported pct-income-report * income
    set after-tax-income income - income-reported *  tax-rate ;
     ; set risk-aversion initial-risk-aversion ; mejor sería función del pct-income-report: menor pct => menor av. riesgo: set risk-aversion U(.5 * pct-income-report,  pct-income-report)
      set risk-aversion initial-Risk-aversion  ;Uniform_rand pct-income-report (.5 * pct-income-report)
      set fraud-detected? false
      set audit? false
      set fraud-detect-hist []
      ; inicializar historial de ingresos y períodos auditados para memoria institucional
      set income-history []
      set audited-periods []
  ]
  ]


end

to setup-auditors [nau]
  create-auditors nau
  [

    set  shape "person business"
    set pct-audit-efficiency 0.5 + random-float 0.5  ; random-float 0.5
    set color blue
    set nr-audits 0
    set selected-txp-audit []
    hide-turtle
  ]



end

to-report log-normal-x [l-mean l-median]

  let n random-normal 0 1
  let u ln l-median
  let s sqrt ( 2 * (ln l-mean - u) )
  ;show u show s
  report exp (u + n * s)

end

to-report color-perc-inc-rep [pir]

  ifelse pir >= 0.5
  [report -8 * (pir - 1) + 54 ]
  [report 15 + pir * 6]


end

to-report Uniform_rand [up_lim low_lim]


report low_lim + (up_lim - low_lim) * random-float 1


end

to-report sliding-window [list-vals last-val]

  set list-vals lput last-val list-vals

 if length list-vals >  period-frauds
  [set list-vals but-first list-vals]

  report list-vals

end

; FUNCIONES PARA MEMORIA INSTITUCIONAL

to-report get-income-history-entry [period-offset]
  ; Obtiene [income, income-reported] de un período específico
  ; period-offset = 0 es el período actual, 1 es el anterior, etc.
  if period-offset >= length income-history [report [0 0]]
  report item period-offset income-history
end

to-report has-period-been-audited [period-offset]
  ; Verifica si un período específico ya fue auditado
  if period-offset >= length audited-periods [report false]
  report item period-offset audited-periods
end

to add-period-to-audited [period-offset]
  ; Marca un período como auditado
  ; Expande la lista si es necesario
  while [period-offset >= length audited-periods]
  [set audited-periods lput false audited-periods]
  set audited-periods replace-item period-offset audited-periods true
end

to-report calculate-historical-noise [period-offset]
  ; Calcula el ruido aplicable: audit-noise * (ticks_actual - ticks_pasado)
  ; Donde ticks_pasado = ticks - period-offset
  let noise-factor audit-noise * period-offset
  report noise-factor
end
@#$#@#$#@
GRAPHICS-WINDOW
286
11
755
481
-1
-1
15.37
1
10
1
1
1
0
1
1
1
0
29
0
29
1
1
1
ticks
30.0

BUTTON
193
502
260
535
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
40
10
230
43
nr-tax-payers
nr-tax-payers
1
max-pop-size
500.0
1
1
NIL
HORIZONTAL

SLIDER
44
226
216
259
nr-auditors
nr-auditors
1
100
20.0
1
1
NIL
HORIZONTAL

SLIDER
41
270
213
303
actual-audit-rate
actual-audit-rate
0
1
0.2
.01
1
NIL
HORIZONTAL

CHOOSER
42
309
213
354
tax-payer-audit-selection
tax-payer-audit-selection
"random" "income-level" "strategic"
2

BUTTON
195
542
258
575
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
0

SLIDER
43
367
215
400
tax-rate
tax-rate
0
1
0.27
.01
1
NIL
HORIZONTAL

SLIDER
41
409
213
442
penalty-rate
penalty-rate
0
5
1.5
.01
1
NIL
HORIZONTAL

SLIDER
10
542
190
575
max-nr-simulated-steps
max-nr-simulated-steps
1
100000
30000.0
1
1
NIL
HORIZONTAL

PLOT
789
11
1448
297
Histogram:        Percent Income Reported           Risk Aversion
percent
Nr. of tax-payers
0.0
1.0
0.0
1.0
true
true
"set-histogram-num-bars 10\nset-plot-x-range 0 1.01" ""
PENS
"IR" 0.1 1 -16777216 true "set-histogram-num-bars 10\nset-plot-x-range 0 1.01" "histogram [pct-income-report] of tax-payers"
"RA" 0.1 1 -2674135 true "set-histogram-num-bars 10\nset-plot-x-range 0 1.01" "histogram [risk-aversion] of tax-payers"

PLOT
790
301
1448
589
Mean: Percent Income Reported ,  Percent Audit Efficacy , Risk Aversion
time-steps
NIL
0.0
0.5
0.0
0.1
true
true
"" ""
PENS
"MPIR" 1.0 0 -16777216 true "" "plot mean [pct-income-report] of tax-payers"
"MPAE" 1.0 0 -10899396 true "" "plot global-audit-perc-eff"
"MRA" 1.0 0 -2674135 true "" "plot mean [risk-aversion] of tax-payers"

SLIDER
40
50
235
83
treshold-influence-income
treshold-influence-income
0
10
1.65
.05
1
NIL
HORIZONTAL

SLIDER
41
90
229
123
period-frauds
period-frauds
1
10
5.0
1
1
NIL
HORIZONTAL

SLIDER
42
127
230
160
learning-rate
learning-rate
0
1
0.05
.01
1
NIL
HORIZONTAL

SLIDER
43
164
229
197
initial-Risk-aversion
initial-Risk-aversion
0
1
0.5
.01
1
NIL
HORIZONTAL

SLIDER
40
450
229
483
institutional-memory
institutional-memory
1
15
1.0
1
1
NIL
HORIZONTAL

SLIDER
40
485
229
518
audit-noise
audit-noise
0
0.5
0.0
.01
1
NIL
HORIZONTAL

@#$#@#$#@
## WHAT IS IT?

(a general understanding of what the model is trying to show or explain)

## HOW IT WORKS

(what rules the agents use to create the overall behavior of the model)

## HOW TO USE IT

(how to use the model, including a description of each of the items in the Interface tab)

## THINGS TO NOTICE

(suggested things for the user to notice while running the model)

## THINGS TO TRY

(suggested things for the user to try to do (move sliders, switches, etc.) with the model)

## EXTENDING THE MODEL

(suggested things to add or change in the Code tab to make the model more complicated, detailed, accurate, etc.)

## NETLOGO FEATURES

(interesting or unusual features of NetLogo that the model uses, particularly in the Code tab; or where workarounds were needed for missing features)

## RELATED MODELS

(models in the NetLogo Models Library and elsewhere which are of related interest)

## CREDITS AND REFERENCES

(a reference to the model's URL on the web if it has one, as well as any other necessary credits, citations, and links)
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

person business
false
0
Rectangle -1 true false 120 90 180 180
Polygon -13345367 true false 135 90 150 105 135 180 150 195 165 180 150 105 165 90
Polygon -7500403 true true 120 90 105 90 60 195 90 210 116 154 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 183 153 210 210 240 195 195 90 180 90 150 165
Circle -7500403 true true 110 5 80
Rectangle -7500403 true true 127 76 172 91
Line -16777216 false 172 90 161 94
Line -16777216 false 128 90 139 94
Polygon -13345367 true false 195 225 195 300 270 270 270 195
Rectangle -13791810 true false 180 225 195 300
Polygon -14835848 true false 180 226 195 226 270 196 255 196
Polygon -13345367 true false 209 202 209 216 244 202 243 188
Line -16777216 false 180 90 150 165
Line -16777216 false 120 90 150 165

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
15
Circle -1 true true 203 65 88
Circle -1 true true 70 65 162
Circle -1 true true 150 105 120
Polygon -7500403 true false 218 120 240 165 255 165 278 120
Circle -7500403 true false 214 72 67
Rectangle -1 true true 164 223 179 298
Polygon -1 true true 45 285 30 285 30 240 15 195 45 210
Circle -1 true true 3 83 150
Rectangle -1 true true 65 221 80 296
Polygon -1 true true 195 285 210 285 210 240 240 210 195 210
Polygon -7500403 true false 276 85 285 105 302 99 294 83
Polygon -7500403 true false 219 85 210 105 193 99 201 83

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

wolf
false
0
Polygon -16777216 true false 253 133 245 131 245 133
Polygon -7500403 true true 2 194 13 197 30 191 38 193 38 205 20 226 20 257 27 265 38 266 40 260 31 253 31 230 60 206 68 198 75 209 66 228 65 243 82 261 84 268 100 267 103 261 77 239 79 231 100 207 98 196 119 201 143 202 160 195 166 210 172 213 173 238 167 251 160 248 154 265 169 264 178 247 186 240 198 260 200 271 217 271 219 262 207 258 195 230 192 198 210 184 227 164 242 144 259 145 284 151 277 141 293 140 299 134 297 127 273 119 270 105
Polygon -7500403 true true -1 195 14 180 36 166 40 153 53 140 82 131 134 133 159 126 188 115 227 108 236 102 238 98 268 86 269 92 281 87 269 103 269 113

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270
@#$#@#$#@
NetLogo 6.4.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="Exper_1_TE_1_2" repetitions="3" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="30000"/>
    <metric>mean [pct-income-report] of tax-payers</metric>
    <metric>mean [risk-aversion] of tax-payers</metric>
    <metric>PIAR_10000</metric>
    <metric>PRA_10000</metric>
    <metric>acum_frauds_detected</metric>
    <metric>acum_frauds_perpretated</metric>
    <metric>acum_frauds_perpretated_all_ags</metric>
    <metric>SS_PIAR</metric>
    <metric>SS_RA</metric>
    <enumeratedValueSet variable="tax-payer-audit-selection">
      <value value="&quot;random&quot;"/>
      <value value="&quot;income-level&quot;"/>
      <value value="&quot;strategic&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="period-frauds">
      <value value="1"/>
      <value value="5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-Risk-aversion">
      <value value="0.25"/>
      <value value="0.75"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="treshold-influence-income">
      <value value="1.5"/>
      <value value="2"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="Exper_1_TE_1_2_new_2" repetitions="3" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="30000"/>
    <metric>mean [pct-income-report] of tax-payers</metric>
    <metric>mean [risk-aversion] of tax-payers</metric>
    <metric>PIAR_10000</metric>
    <metric>PRA_10000</metric>
    <metric>acum_frauds_detected</metric>
    <metric>acum_frauds_perpretated</metric>
    <metric>acum_frauds_perpretated_all_ags</metric>
    <enumeratedValueSet variable="period-frauds">
      <value value="1"/>
      <value value="5"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="Exper_paper_1" repetitions="5" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="30000"/>
    <metric>acum_prom_PIAR_ags / 5000</metric>
    <metric>acum_prom_RA_ags / 5000</metric>
    <metric>acum_delta_inc_real_inc_report</metric>
    <metric>acum_frauds_perpretated</metric>
    <metric>acum_frauds_detected</metric>
    <metric>acum_frauds_perpretated_all_ags</metric>
    <enumeratedValueSet variable="tax-payer-audit-selection">
      <value value="&quot;strategic&quot;"/>
      <value value="&quot;random&quot;"/>
      <value value="&quot;income-level&quot;"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="Exper_emu_paper" repetitions="1" runMetricsEveryStep="false">
    <setup>setup</setup>
    <go>go</go>
    <timeLimit steps="5000"/>
    <metric>mean [pct-income-report] of tax-payers</metric>
    <metric>mean [risk-aversion] of tax-payers</metric>
    <metric>PIAR_10000</metric>
    <metric>PRA_10000</metric>
    <metric>acum_frauds_detected</metric>
    <metric>acum_frauds_perpretated</metric>
    <metric>acum_frauds_perpretated_all_ags</metric>
    <metric>SS_PIAR</metric>
    <metric>SS_RA</metric>
    <enumeratedValueSet variable="nr-tax-payers">
      <value value="500"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="nr-auditors">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="actual-audit-rate">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="tax-rate">
      <value value="0.27"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="penalty-rate">
      <value value="1.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="learning-rate">
      <value value="0.05"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="initial-Risk-aversion">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="treshold-influence-income">
      <value value="1.65"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="tax-payer-audit-selection">
      <value value="&quot;random&quot;"/>
      <value value="&quot;income-level&quot;"/>
      <value value="&quot;strategic&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="period-frauds">
      <value value="1"/>
      <value value="5"/>
    </enumeratedValueSet>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180
@#$#@#$#@
0
@#$#@#$#@
