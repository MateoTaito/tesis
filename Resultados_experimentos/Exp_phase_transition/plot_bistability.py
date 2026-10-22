"""Biestabilidad strategic @ baja cobertura: distribuciones, bandas y cruces (N=10).

Uso: venv/bin/python Resultados_experimentos/Exp_phase_transition/plot_bistability.py
Lee phase_transition_50k_N10.csv, escribe 4 PNG + imprime clasificación y correlaciones.
"""
import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os
from math import sqrt

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'phase_transition_50k_N10.csv')

rows = list(csv.reader(open(SRC)))
df = pd.DataFrame(rows[7:], columns=rows[6])
PIR = 'mean [pct-income-report] of tax-payers'
PRA = 'mean [risk-aversion] of tax-payers'
COV = 'count tax-payers with [sum fraud-detect-hist > 0] / count tax-payers'
SCO = 'mean [fiscal-risk-score] of tax-payers'
for c in [PIR, PRA, COV, SCO, 'PIAR_10000', 'acum_frauds_detected']:
    df[c] = df[c].astype(float)
df['rate'] = df['actual-audit-rate'].astype(float)
df['pf'] = df['period-frauds'].astype(int)
df['strat'] = df['tax-payer-audit-selection']
df['det_rate'] = df['acum_frauds_detected'] / 25000
colors = {'random': '#1f77b4', 'strategic': '#2ca02c'}

print("=" * 70)
print("BIESTABILIDAD: distribuciones por run (N=10 por celda)")
print("=" * 70)

# ---- 1. Clasificación techo / no-techo (umbral 0.9 = lock-in en ceiling) ----
print("\n--- % runs en techo (PIR>=0.9) + IC95 binomial (Wilson) ---")
z = 1.96
for (s, pf, r), g in sorted(df.groupby(['strat', 'pf', 'rate']),
                            key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
    v = g[PIR].values
    k = int((v >= 0.9).sum())
    n = len(v)
    denom = 1 + z * z / n
    c = (k / n + z * z / (2 * n)) / denom
    h = z * sqrt(k * (n - k) / n ** 3 + z * z / (4 * n ** 2)) / denom
    print(f"{s:9s} PF{pf} {r}: {k}/{n} en techo "
          f"(IC95 {max(0, c - h):.2f}-{min(1, c + h):.2f}) "
          f"runs={sorted(round(x, 3) for x in v)}")

# ---- 2. ¿PIAR_10000 predice el destino? (r de Pearson en celdas biestables) ----
print("\n--- r(PIR_10000, PIR_final) por celda strategic ---")
for pf in [1, 5]:
    for r in [0.02, 0.03, 0.04, 0.05]:
        g = df[(df.strat == 'strategic') & (df.pf == pf) & (df.rate == r)]
        if g[PIR].std() > 1e-9 and g['PIAR_10000'].std() > 1e-9:
            rr = g[PIR].corr(g['PIAR_10000'])
            print(f"strategic PF{pf} {r}: r={rr:+.3f}")
        else:
            print(f"strategic PF{pf} {r}: sin varianza (techo)")

# ---- FIG 1: stripplot distribuciones finales por celda ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
for idx, pf in enumerate([1, 5]):
    ax = axes[idx]
    d = df[df.pf == pf]
    sns.stripplot(data=d, x='rate', y=PIR, hue='strat', ax=ax, size=9,
                  palette=colors, dodge=True, alpha=0.9, jitter=0.12)
    ax.axhline(0.9, color='red', linestyle='--', alpha=0.6, label='umbral techo 0.9')
    ax.set_title(f'Period-Frauds = {pf} (1 punto = 1 run, N=10)', fontsize=13, fontweight='bold')
    ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3, axis='y')
    if idx == 0:
        ax.set_ylabel('PIR final @ tick 50000', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', fontsize=10)
    else:
        ax.legend_.remove() if ax.legend_ else None
plt.suptitle('Distribución por run del PIR final: ¿biestabilidad o dispersión?',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'bistability_distributions.png'), dpi=300, bbox_inches='tight')
print("\nSaved: bistability_distributions.png")
plt.close()

# ---- FIG 2: abanico strategic (media±std + min-max) PF1 vs PF5 ----
fig, ax = plt.subplots(figsize=(11, 6))
for pf, ls, mk in [(1, '-', 'o'), (5, '--', 's')]:
    g = df[df.strat == 'strategic'].groupby('rate')[PIR].agg(['mean', 'std', 'min', 'max'])
    ax.plot(g.index, g['mean'], marker=mk, linewidth=2.5, markersize=10,
            linestyle=ls, label=f'strategic PF{pf} (media±std)', color='#2ca02c' if pf == 1 else '#8b1a6e')
    ax.fill_between(g.index, g['mean'] - g['std'], g['mean'] + g['std'], alpha=0.2,
                    color='#2ca02c' if pf == 1 else '#8b1a6e')
    ax.fill_between(g.index, g['min'], g['max'], alpha=0.12,
                    color='#2ca02c' if pf == 1 else '#8b1a6e', label=f'PF{pf} rango min-max')
ax.axvline(0.02, color='gray', linestyle=':', alpha=0.6)
ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
ax.set_ylabel('PIR final @ tick 50000', fontsize=12, fontweight='bold')
ax.set_title('Abanico strategic: rango de resultados según memoria social (N=10)',
             fontsize=14, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10, loc='lower right')
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'bistability_fan_strategic.png'), dpi=300, bbox_inches='tight')
print("Saved: bistability_fan_strategic.png")
plt.close()

# ---- FIG 3: cruces PIR vs (cobertura, detección, PRA, PIAR_10000) ----
fig, axes = plt.subplots(2, 2, figsize=(14, 10))
pairs = [(COV, 'Cobertura: det. en últ. PF auditorías'), ('det_rate', 'Tasa detección (fraudes/tick)'),
         (PRA, 'PRA final'), ('PIAR_10000', 'PIAR en tick 10000')]
for ax, (col, title) in zip(axes.flat, pairs):
    for s in ['random', 'strategic']:
        d = df[df.strat == s]
        ax.scatter(d[col], d[PIR], label=s, color=colors[s], alpha=0.7, s=45)
    r = df[PIR].corr(df[col]) if df[col].std() > 0 else float('nan')
    ax.set_xlabel(title, fontsize=11, fontweight='bold')
    ax.set_ylabel('PIR final', fontsize=11, fontweight='bold')
    ax.set_title(f'{title}  (r={r:+.2f} global)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
plt.suptitle('¿Qué acompaña al PIR final? Cruces por run (160 runs)',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'bistability_crossplots.png'), dpi=300, bbox_inches='tight')
print("Saved: bistability_crossplots.png")
plt.close()

# ---- FIG 4: foco celda biestable strategic PF5 0.02: barras por run ----
d = df[(df.strat == 'strategic') & (df.pf == 5) & (df.rate == 0.02)].sort_values(PIR)
fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(range(len(d)), d[PIR].values, color='#8b1a6e', alpha=0.8)
ax.axhline(d[PIR].mean(), color='black', linestyle='--', label=f"media {d[PIR].mean():.3f}")
for i, v in enumerate(d[PIR].values):
    ax.text(i, v + 0.02, f'{v:.2f}', ha='center', fontsize=10)
ax.set_xticks(range(len(d)))
ax.set_xticklabels([f'run {i + 1}' for i in range(len(d))])
ax.set_ylabel('PIR final', fontsize=12, fontweight='bold')
ax.set_title('Strategic PF5 @ 0.02: 10 runs ordenados — dispersión total, sin clusters',
             fontsize=13, fontweight='bold')
ax.set_ylim(0, 1.15)
ax.legend(fontsize=10)
ax.grid(True, alpha=0.3, axis='y')
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'bistability_PF5_002_runs.png'), dpi=300, bbox_inches='tight')
print("Saved: bistability_PF5_002_runs.png")
plt.close()

print("\nALL DONE")
