import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

SRC = sys.argv[1] if len(sys.argv) > 1 else 'Resultados_experimentos/Exp_chile_calibrado/chile_n30.csv'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'Resultados_experimentos/Exp_chile_calibrado/'
PREFIX = sys.argv[3] if len(sys.argv) > 3 else 'n30_'

os.makedirs(OUT, exist_ok=True)

with open(SRC) as f:
    rows = list(csv.reader(f))
header = rows[6]
data = rows[7:]
df = pd.DataFrame(data, columns=header)

df['period-frauds'] = df['period-frauds'].astype(int)
df['institutional-memory'] = df['institutional-memory'].astype(int)
df['actual-audit-rate'] = df['actual-audit-rate'].astype(float)
PIR = 'mean [pct-income-report] of tax-payers'
PRA = 'mean [risk-aversion] of tax-payers'
df[PIR] = df[PIR].astype(float)
df[PRA] = df[PRA].astype(float)
df['acum_frauds_detected'] = df['acum_frauds_detected'].astype(float)
df['acum_frauds_perpretated'] = df['acum_frauds_perpretated'].astype(float)
df['acum_frauds_perpretated_all_ags'] = df['acum_frauds_perpretated_all_ags'].astype(float)
df['PIAR_10000'] = df['PIAR_10000'].astype(float)
df['PRA_10000'] = df['PRA_10000'].astype(float)
df['SS_PIAR'] = df['SS_PIAR'].astype(int)
df['SS_RA'] = df['SS_RA'].astype(int)

TAG = 'Exper_chile_calibrado (N=30/celda, audit-rate 0.02, 30k steps)'

print("="*70)
print(f"DATOS: {SRC}  [{TAG}]")
print("="*70)
print(f"  Filas: {len(df)}")
print(f"  audit-rate: {sorted(df['actual-audit-rate'].unique())}")
print(f"  Estrategias: {sorted(df['tax-payer-audit-selection'].unique())}")
print(f"  Period-frauds: {sorted(df['period-frauds'].unique())}")
print(f"  Institutional-memory: {sorted(df['institutional-memory'].unique())}")

strategies = sorted(df['tax-payer-audit-selection'].unique())
period_values = sorted(df['period-frauds'].unique())
mem_values = sorted(df['institutional-memory'].unique())
colors = {'random': '#1f77b4', 'income-level': '#ff7f0e', 'strategic': '#2ca02c'}

summary = df.groupby(['tax-payer-audit-selection', 'period-frauds', 'institutional-memory'])[PIR].agg(['mean', 'std', 'count']).reset_index()
summary_pra = df.groupby(['tax-payer-audit-selection', 'period-frauds', 'institutional-memory'])[PRA].agg(['mean', 'std', 'count']).reset_index()

print("\n" + "="*70)
print("SUMMARY PIR (pct-income-reported @ tick 30000, N=30)")
print("="*70)
print(summary.to_string(index=False))
print("\n" + "="*70)
print("SUMMARY PRA (risk-aversion @ tick 30000, N=30)")
print("="*70)
print(summary_pra.to_string(index=False))

summary.to_csv(OUT + PREFIX + 'summary_mean_pir.csv', index=False)
summary_pra.to_csv(OUT + PREFIX + 'summary_mean_pra.csv', index=False)

# ============================================================================
# PLOT 1: PIR vs inst-mem, líneas por estrategia, facetas por period-frauds
# ============================================================================
fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        data = summary[(summary['tax-payer-audit-selection'] == strategy) & (summary['period-frauds'] == period)].sort_values('institutional-memory')
        ax.plot(data['institutional-memory'], data['mean'],
                marker='o', linewidth=2.5, markersize=10,
                label=strategy, color=colors.get(strategy))
        ax.fill_between(data['institutional-memory'],
                        data['mean'] - data['std'],
                        data['mean'] + data['std'],
                        alpha=0.2, color=colors.get(strategy))
    ax.set_xlabel('Memoria Institucional (períodos)', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(mem_values)
    ax.set_ylim(0, 1.05)
    if idx == 0:
        ax.set_ylabel('Mean PIR (Pct-Income-Reported)', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='lower right', fontsize=10, title_fontsize=11)
plt.suptitle(f'PIR @ tick 30000 vs Memoria Institucional (mean±std, N=30)\n{TAG}', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + PREFIX + 'PIR_vs_instmem_faceted_by_periodfrauds.png', dpi=300, bbox_inches='tight')
print("\nSaved: " + PREFIX + "PIR_vs_instmem_faceted_by_periodfrauds.png")
plt.close()

# ============================================================================
# PLOT 2: PRA vs inst-mem
# ============================================================================
fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        data = summary_pra[(summary_pra['tax-payer-audit-selection'] == strategy) & (summary_pra['period-frauds'] == period)].sort_values('institutional-memory')
        ax.plot(data['institutional-memory'], data['mean'],
                marker='o', linewidth=2.5, markersize=10,
                label=strategy, color=colors.get(strategy))
        ax.fill_between(data['institutional-memory'],
                        data['mean'] - data['std'],
                        data['mean'] + data['std'],
                        alpha=0.2, color=colors.get(strategy))
    ax.set_xlabel('Memoria Institucional (períodos)', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(mem_values)
    ax.set_ylim(0, 1.05)
    if idx == 0:
        ax.set_ylabel('Mean PRA (Risk-Aversion)', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='lower right', fontsize=10, title_fontsize=11)
plt.suptitle(f'PRA @ tick 30000 vs Memoria Institucional (mean±std, N=30)\n{TAG}', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + PREFIX + 'PRA_vs_instmem_faceted_by_periodfrauds.png', dpi=300, bbox_inches='tight')
print("Saved: " + PREFIX + "PRA_vs_instmem_faceted_by_periodfrauds.png")
plt.close()

# ============================================================================
# PLOT 3: Heatmaps PIR/PRA (estrategia × inst-mem, por period-frauds)
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
for col, period in enumerate(period_values):
    pivot_pir = summary[(summary['period-frauds'] == period)].pivot(
        index='tax-payer-audit-selection', columns='institutional-memory', values='mean')
    pivot_pra = summary_pra[(summary_pra['period-frauds'] == period)].pivot(
        index='tax-payer-audit-selection', columns='institutional-memory', values='mean')
    sns.heatmap(pivot_pir, annot=True, fmt='.3f', cmap='RdYlGn',
                cbar_kws={'label': 'Mean PIR'}, ax=axes[0, col],
                linewidths=0.5, vmin=0, vmax=1)
    axes[0, col].set_title(f'PIR | Period-Frauds = {period}', fontsize=12, fontweight='bold')
    axes[0, col].set_xlabel('Memoria Institucional')
    axes[0, col].set_ylabel('Estrategia' if col == 0 else '')
    sns.heatmap(pivot_pra, annot=True, fmt='.3f', cmap='RdYlGn',
                cbar_kws={'label': 'Mean PRA'}, ax=axes[1, col],
                linewidths=0.5, vmin=0, vmax=1)
    axes[1, col].set_title(f'PRA | Period-Frauds = {period}', fontsize=12, fontweight='bold')
    axes[1, col].set_xlabel('Memoria Institucional')
    axes[1, col].set_ylabel('Estrategia' if col == 0 else '')
plt.suptitle(f'Heatmaps: Strategy × Memoria Institucional, N=30 (split by Period-Frauds)\n{TAG}',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(OUT + PREFIX + 'heatmaps_PIR_PRA.png', dpi=300, bbox_inches='tight')
print("Saved: " + PREFIX + "heatmaps_PIR_PRA.png")
plt.close()

# ============================================================================
# PLOT 4: Barras facetadas PIR/PRA × period-frauds (con yerr=std, N=30)
# ============================================================================
fig, axes = plt.subplots(2, len(period_values), figsize=(16, 9), sharey=True)
for col, period in enumerate(period_values):
    for row, (metric_name, summ) in enumerate([('PIR', summary), ('PRA', summary_pra)]):
        ax = axes[row, col]
        data = summ[summ['period-frauds'] == period].sort_values(['tax-payer-audit-selection', 'institutional-memory'])
        strategies_sorted = sorted(data['tax-payer-audit-selection'].unique())
        mems_sorted = sorted(data['institutional-memory'].unique())
        x = np.arange(len(strategies_sorted))
        width = 0.15
        for i, mem in enumerate(mems_sorted):
            vals = []
            errs = []
            for s in strategies_sorted:
                row_data = data[(data['tax-payer-audit-selection'] == s) & (data['institutional-memory'] == mem)]
                vals.append(row_data['mean'].values[0])
                errs.append(row_data['std'].values[0])
            offset = (i - len(mems_sorted)/2 + 0.5) * width
            ax.bar(x + offset, vals, width, yerr=errs,
                   label=f'inst-mem={mem}', alpha=0.85, capsize=3)
        ax.set_xticks(x)
        ax.set_xticklabels(strategies_sorted, fontsize=10)
        ax.set_ylabel(f'Mean {metric_name}', fontsize=11, fontweight='bold')
        ax.set_title(f'{metric_name} | Period-Frauds = {period}', fontsize=12, fontweight='bold')
        ax.set_ylim(0, 1.1)
        ax.grid(True, alpha=0.3, axis='y')
        if row == 0 and col == len(period_values) - 1:
            ax.legend(title='Memoria Inst.', loc='upper left', fontsize=9, title_fontsize=10)
plt.suptitle(f'Faceted bars: PIR/PRA × Period-Frauds, grouped by Memoria Institucional (N=30)\n{TAG}',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(OUT + PREFIX + 'faceted_bars_PIR_PRA.png', dpi=300, bbox_inches='tight')
print("Saved: " + PREFIX + "faceted_bars_PIR_PRA.png")
plt.close()

# ============================================================================
# PLOT 5: Tasa de detección (misma convención que Exp_full_inst_mem: acum/30000)
# ============================================================================
df['detection_rate_per_tick'] = df['acum_frauds_detected'] / 30000
summary_det = df.groupby(['tax-payer-audit-selection', 'period-frauds', 'institutional-memory'])['detection_rate_per_tick'].agg(['mean', 'std']).reset_index()
summary_det.to_csv(OUT + PREFIX + 'summary_detection_rate.csv', index=False)

fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        data = summary_det[(summary_det['tax-payer-audit-selection'] == strategy) & (summary_det['period-frauds'] == period)].sort_values('institutional-memory')
        ax.plot(data['institutional-memory'], data['mean'],
                marker='s', linewidth=2.5, markersize=10,
                label=strategy, color=colors.get(strategy))
        ax.fill_between(data['institutional-memory'],
                        data['mean'] - data['std'],
                        data['mean'] + data['std'],
                        alpha=0.2, color=colors.get(strategy))
    ax.set_xlabel('Memoria Institucional (períodos)', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(mem_values)
    if idx == 0:
        ax.set_ylabel('Detection Rate (frauds/tick)', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='best', fontsize=10, title_fontsize=11)
plt.suptitle(f'Tasa de detección de fraudes @ tick 30000 (mean±std, N=30)\n{TAG}', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + PREFIX + 'detection_rate.png', dpi=300, bbox_inches='tight')
print("Saved: " + PREFIX + "detection_rate.png")
plt.close()

# ============================================================================
# PLOT 6: ΔPIR final − tick 10000 (convergencia)
# ============================================================================
df['PIR_delta'] = df[PIR] - df['PIAR_10000']
summary_delta = df.groupby(['tax-payer-audit-selection', 'period-frauds', 'institutional-memory'])['PIR_delta'].agg(['mean', 'std']).reset_index()

fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        data = summary_delta[(summary_delta['tax-payer-audit-selection'] == strategy) & (summary_delta['period-frauds'] == period)].sort_values('institutional-memory')
        ax.plot(data['institutional-memory'], data['mean'],
                marker='D', linewidth=2.5, markersize=10,
                label=strategy, color=colors.get(strategy))
        ax.fill_between(data['institutional-memory'],
                        data['mean'] - data['std'],
                        data['mean'] + data['std'],
                        alpha=0.2, color=colors.get(strategy))
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Memoria Institucional (períodos)', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(mem_values)
    if idx == 0:
        ax.set_ylabel('ΔPIR (final − tick 10000)', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='best', fontsize=10, title_fontsize=11)
plt.suptitle(f'Cambio de PIR entre t=10000 y t=30000, N=30 (convergencia)\n{TAG}', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + PREFIX + 'PIR_delta_transient.png', dpi=300, bbox_inches='tight')
print("Saved: " + PREFIX + "PIR_delta_transient.png")
plt.close()

print("\n" + "="*70)
print("ALL DONE")
print("="*70)
