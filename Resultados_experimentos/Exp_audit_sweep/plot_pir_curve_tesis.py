"""Curva PIR vs audit_rate solo modelo tesis (k=1, noise=0).

X: audit_rate 0.01-0.10 | Y: mean PIR final | lineas por estrategia, facetas por period-frauds.
Seed 42, 10k ticks, N=1.
"""
import csv
import os
import sys

import pandas as pd
import matplotlib.pyplot as plt

SRC = sys.argv[1] if len(sys.argv) > 1 else 'Resultados_experimentos/Exp_audit_sweep/tesis_curve_001_010.csv'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'Resultados_experimentos/Exp_audit_sweep/'

os.makedirs(OUT, exist_ok=True)
PIR = 'mean [pct-income-report] of tax-payers'

with open(SRC) as f:
    rows = list(csv.reader(f))
df = pd.DataFrame(rows[7:], columns=rows[6])
df['actual-audit-rate'] = df['actual-audit-rate'].astype(float)
df['period-frauds'] = df['period-frauds'].astype(int)
df[PIR] = df[PIR].astype(float)

rates = sorted(df['actual-audit-rate'].unique())
pfs = sorted(df['period-frauds'].unique())
strategies = ['random', 'income-level', 'strategic']
print(f'rates: {rates} | PF: {pfs} | filas: {len(df)}')

df.to_csv(OUT + 'summary_pir_curve_tesis.csv', index=False)

colors = {'random': '#1f77b4', 'income-level': '#ff7f0e', 'strategic': '#2ca02c'}
markers = {'random': 'o', 'income-level': 's', 'strategic': 'D'}

fig, axes = plt.subplots(1, len(pfs), figsize=(15, 6), sharey=True)
for idx, pf in enumerate(pfs):
    ax = axes[idx] if len(pfs) > 1 else axes
    for s in strategies:
        sub = df[(df['period-frauds'] == pf) & (df['tax-payer-audit-selection'] == s)].sort_values('actual-audit-rate')
        ax.plot(sub['actual-audit-rate'], sub[PIR], marker=markers[s],
                linewidth=2.5, markersize=9, label=s, color=colors[s])
        for x, y in zip(sub['actual-audit-rate'], sub[PIR]):
            ax.annotate(f'{y:.2f}', (x, y), textcoords='offset points',
                        xytext=(0, 8), ha='center', fontsize=7, alpha=0.8)
    ax.set_xlabel('audit-rate (actual-audit-rate)', fontweight='bold')
    ax.set_title(f'period-frauds = {pf}', fontweight='bold')
    ax.set_xticks(rates)
    ax.set_xticklabels([f'{r:g}' for r in rates], rotation=45)
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3)
    if idx == 0:
        ax.set_ylabel('Mean PIR (pct-income-reported final)', fontweight='bold')
        ax.legend(title='Estrategia', fontsize=10, title_fontsize=11)

plt.suptitle('Evolución de Mean PIR vs audit-rate — solo tesis (k=1, noise=0)\n'
             'Seed 42, 10k ticks, N=1, sin IC', fontweight='bold', y=1.02)
plt.tight_layout()
fname = OUT + 'pir_curve_tesis_audit_rate.png'
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('Saved:', fname)
plt.close()
print('ALL DONE')
