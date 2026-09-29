"""Comparacion base vs tesis por audit_rate: X=period-frauds, Y=mean PIR, estratificado por estrategia.

Entradas:
  Resultados_experimentos/Exp_audit_sweep/base_audit_sweep.csv   (36 runs, ABM_Original)
  Resultados_experimentos/Exp_audit_sweep/tesis_audit_sweep.csv  (36 runs, ABM_TESIS_CHANGES k=1 noise=0)
Seed 42, 10k ticks, 1 rep/celda. CSVs BehaviorSpace con 6 filas de metadata.

Salidas (en OUT):
  audit_sweep_combined.csv, summary_mean_pir.csv
  pir_comparison_audit_0.01/0.02/0.03/0.05/0.1/0.2.png  (6 figuras, una por audit_rate)
  pir_comparison_all_rates.png  (resumen 2x3 facetado por audit_rate)
"""
import csv
import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

BASE = sys.argv[1] if len(sys.argv) > 1 else 'Resultados_experimentos/Exp_audit_sweep/base_audit_sweep.csv'
TESIS = sys.argv[2] if len(sys.argv) > 2 else 'Resultados_experimentos/Exp_audit_sweep/tesis_audit_sweep.csv'
OUT = sys.argv[3] if len(sys.argv) > 3 else 'Resultados_experimentos/Exp_audit_sweep/'

os.makedirs(OUT, exist_ok=True)

PIR = 'mean [pct-income-report] of tax-payers'


def load(path, modelo):
    with open(path) as f:
        rows = list(csv.reader(f))
    header = rows[6]
    df = pd.DataFrame(rows[7:], columns=header)
    df['modelo'] = modelo
    # columnas comunes a ambos modelos
    df['period-frauds'] = df['period-frauds'].astype(int)
    df['actual-audit-rate'] = df['actual-audit-rate'].astype(float)
    df[PIR] = df[PIR].astype(float)
    return df


base = load(BASE, 'base')
tesis = load(TESIS, 'tesis')
df = pd.concat([base, tesis], ignore_index=True)

rates = sorted(df['actual-audit-rate'].unique())
strategies = ['random', 'income-level', 'strategic']
pfs = sorted(df['period-frauds'].unique())
modelos = ['base', 'tesis']

print('=' * 70)
print(f'Filas: {len(df)} | rates: {rates} | PF: {pfs}')
print('=' * 70)

df.to_csv(OUT + 'audit_sweep_combined.csv', index=False)
summary = df.groupby(['actual-audit-rate', 'period-frauds',
                      'tax-payer-audit-selection', 'modelo'])[PIR].agg(['mean', 'count']).reset_index()
summary.to_csv(OUT + 'summary_mean_pir.csv', index=False)
print(summary.to_string(index=False))

# ---- equivalencia base vs tesis (k=1 debe ser ~identico) ----
piv = summary.pivot_table(index=['actual-audit-rate', 'period-frauds', 'tax-payer-audit-selection'],
                          columns='modelo', values='mean')
piv['abs_diff'] = (piv['base'] - piv['tesis']).abs()
print('\n' + '=' * 70)
print('MAX abs diff base-tesis por celda:')
print(piv['abs_diff'].max())
print(piv.sort_values('abs_diff', ascending=False).head(10).to_string())

# ---- estilo: estrategia=color, modelo=solido vs achurado ----
colors = {'random': '#1f77b4', 'income-level': '#ff7f0e', 'strategic': '#2ca02c'}
hatches = {'base': '', 'tesis': '///'}
alphas = {'base': 1.0, 'tesis': 0.55}
combo_order = [(s, m) for s in strategies for m in modelos]  # 6 barras por PF
width = 0.12


def plot_one_rate(ax, rate):
    sub = summary[summary['actual-audit-rate'] == rate]
    x = np.arange(len(pfs))
    for i, (s, m) in enumerate(combo_order):
        vals = []
        for pf in pfs:
            r = sub[(sub['period-frauds'] == pf)
                    & (sub['tax-payer-audit-selection'] == s)
                    & (sub['modelo'] == m)]
            vals.append(r['mean'].values[0] if len(r) else np.nan)
        offset = (i - len(combo_order) / 2 + 0.5) * width
        ax.bar(x + offset, vals, width, color=colors[s], alpha=alphas[m],
               hatch=hatches[m], edgecolor='black', linewidth=0.6,
               label=f'{s}/{m}')
    ax.set_xticks(x)
    ax.set_xticklabels([str(p) for p in pfs])
    ax.set_xlabel('period-frauds', fontweight='bold')
    ax.set_ylim(0, 1.1)
    ax.grid(True, alpha=0.3, axis='y')
    ax.set_title(f'audit-rate = {rate:g}', fontweight='bold')


TAG = 'AuditSweep seed 42, 10k ticks, N=1 (base vs tesis k=1)'

# ---- 6 figuras, una por audit_rate ----
for rate in rates:
    fig, ax = plt.subplots(figsize=(11, 6))
    plot_one_rate(ax, rate)
    ax.set_ylabel('Mean PIR (pct-income-reported final)', fontweight='bold')
    ax.legend(title='estrategia/modelo', fontsize=8, title_fontsize=9,
              loc='upper left', ncol=2)
    plt.suptitle(f'Mean PIR vs period-frauds por estrategia — base vs tesis\n{TAG} | audit-rate={rate:g}',
                 fontweight='bold')
    plt.tight_layout()
    fname = OUT + f'pir_comparison_audit_{rate:g}.png'
    plt.savefig(fname, dpi=300, bbox_inches='tight')
    print('Saved:', fname)
    plt.close()

# ---- 1 figura resumen 2x3 ----
fig, axes = plt.subplots(2, 3, figsize=(18, 10), sharey=True, sharex=True)
for ax, rate in zip(axes.flat, rates):
    plot_one_rate(ax, rate)
    if ax in (axes[1, 0], axes[1, 1], axes[1, 2]):
        pass
axes[1, 0].set_ylabel('Mean PIR', fontweight='bold')
axes[1, 1].set_ylabel('Mean PIR', fontweight='bold')
handles, labels = axes[0, 0].get_legend_handles_labels()
fig.legend(handles, labels, title='estrategia/modelo', loc='outside right',
           fontsize=9, title_fontsize=10)
plt.suptitle(f'Mean PIR vs period-frauds — todos los audit-rates side by side\n{TAG} — N=1, sin IC',
             fontweight='bold')
plt.tight_layout()
fname = OUT + 'pir_comparison_all_rates.png'
plt.savefig(fname, dpi=300, bbox_inches='tight')
print('Saved:', fname)
plt.close()

print('ALL DONE')
