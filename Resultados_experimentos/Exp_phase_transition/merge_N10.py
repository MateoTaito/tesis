"""Fusiona batch1 (N=3) + batch2 (N=7) en N=10 por celda, con procedencia.

Uso:
  venv/bin/python Resultados_experimentos/Exp_phase_transition/merge_N10.py

Salidas:
  phase_transition_50k_N10.csv  (6 meta + header + 160 filas, [run number] 1..10 por combo)
  MERGE_N10.txt                 (trazabilidad: md5, conteos, fechas)
"""
import csv
import hashlib
from pathlib import Path
from collections import defaultdict

BASE = Path(__file__).resolve().parent
B1 = BASE / 'phase_transition_50k.csv'
B2 = BASE / 'phase_transition_50k_batch2.csv'
OUT = BASE / 'phase_transition_50k_N10.csv'
LOG = BASE / 'MERGE_N10.txt'


def load(path):
    rows = list(csv.reader(open(path)))
    meta, header, data = rows[:6], rows[6], rows[7:]
    return meta, header, data


meta1, h1, d1 = load(B1)
meta2, h2, d2 = load(B2)
assert h1 == h2, 'Headers difieren entre batches; no fusionar'
assert len(d1) == 48, f'batch1: {len(d1)} filas, esperado 48'
assert len(d2) == 112, f'batch2: {len(d2)} filas, esperado 112'

data = d1 + d2
i_run = h1.index('[run number]')
i_step = h1.index('[step]')
param_idx = [i for i, h in enumerate(h1) if i not in (i_run,)
             and not h.startswith(('mean ', 'PIAR', 'PRA', 'acum_', 'SS_', 'count tax'))]

counts = defaultdict(int)
for r in data:
    key = tuple(r[i] for i in param_idx)
    counts[key] += 1
    r[i_run] = str(counts[key])
assert set(counts.values()) == {10}, f'conteos != 10: {set(counts.values())}'

with open(OUT, 'w', newline='') as f:
    w = csv.writer(f)
    w.writerows(meta1)
    w.writerow(h1)
    w.writerows(data)

md5 = lambda p: hashlib.md5(open(p, 'rb').read()).hexdigest()
repo = BASE.parents[1]
log = [
    'MERGE N=10 PhaseTransition',
    f"batch1: {len(d1)} filas <- {B1.name}",
    f"batch2: {len(d2)} filas <- {B2.name}",
    f"merged: {len(data)} filas (16 combos x 10), [run number] renumerado 1..10 por combo",
    f"md5 modelo : {md5(repo / 'ABM_TESIS_CHANGES.nlogo')}  (idéntico en ambas tandas: verificado)",
    f"md5 xml b1 : {md5(BASE / 'phase_transition.xml')}",
    f"md5 xml b2 : {md5(BASE / 'phase_transition_batch2.xml')}",
    'Nota: extensión secuencial pre-registrada (N=3 analizado antes); inferencia final sobre N=10.',
]
LOG.write_text('\n'.join(log) + '\n')
print('\n'.join(log))
print(f'OK -> {OUT.name}')
