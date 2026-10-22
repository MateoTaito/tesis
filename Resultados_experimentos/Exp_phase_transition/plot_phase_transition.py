import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys
import os

SRC = sys.argv[1] if len(sys.argv) > 1 else 'Resultados_experimentos/Exp_phase_transition/phase_transition_50k.csv'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'Resultados_experimentos/Exp_phase_transition/'

os.makedirs(OUT, exist_ok=True)

with open(SRC) as f:
    rows = list(csv.reader(f))
header = rows[6]
data = rows[7:]
df = pd.DataFrame(data, columns=header)

PIR = 'mean [pct-income-report] of tax-payers'
PRA = 'mean [risk-aversion] of tax-payers'
COV = 'count tax-payers with [sum fraud-detect-hist > 0] / count tax-payers'
SCORE = 'mean [fiscal-risk-score] of tax-payers'

df['period-frauds'] = df['period-frauds'].astype(int)
df['actual-audit-rate'] = df['actual-audit-rate'].astype(float)
for c in [PIR, PRA, COV, SCORE, 'PIAR_10000', 'PRA_10000',
          'acum_frauds_detected', 'acum_frauds_perpretated',
          'acum_frauds_perpretated_all_ags']:
    df[c] = df[c].astype(float)
for c in ['SS_PIAR', 'SS_RA']:
    df[c] = df[c].astype(int)

print("=" * 70)
print(f"DATOS: {SRC}")
print("=" * 70)
print(f"  Filas: {len(df)} (esperado 48 = 4 rates x 2 strats x 2 PF x 3 reps)")
print(f"  Estrategias: {sorted(df['tax-payer-audit-selection'].unique())}")
print(f"  Period-frauds: {sorted(df['period-frauds'].unique())}")
print(f"  Audit-rates: {sorted(df['actual-audit-rate'].unique())}")

strategies = sorted(df['tax-payer-audit-selection'].unique())
period_values = sorted(df['period-frauds'].unique())
rate_values = sorted(df['actual-audit-rate'].unique())
colors = {'random': '#1f77b4', 'income-level': '#ff7f0e', 'strategic': '#2ca02c'}

grp = ['tax-payer-audit-selection', 'period-frauds', 'actual-audit-rate']
summary = df.groupby(grp)[PIR].agg(['mean', 'std', 'count']).reset_index()
summary_pra = df.groupby(grp)[PRA].agg(['mean', 'std', 'count']).reset_index()
summary_cov = df.groupby(grp)[COV].agg(['mean', 'std']).reset_index()

print("\n" + "=" * 70)
print("SUMMARY PIR (mean pct-income-reported @ tick 50000)")
print("=" * 70)
print(summary.to_string(index=False))

summary.to_csv(OUT + 'summary_mean_pir.csv', index=False)
summary_pra.to_csv(OUT + 'summary_mean_pra.csv', index=False)
summary_cov.to_csv(OUT + 'summary_signal_coverage.csv', index=False)

# ============================================================================
# PLOT 1: PIR vs audit-rate, faceted by period-frauds (THE phase-change figure)
# ============================================================================
fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
if len(period_values) == 1:
    axes = [axes]
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        d = summary[(summary['tax-payer-audit-selection'] == strategy) &
                    (summary['period-frauds'] == period)].sort_values('actual-audit-rate')
        ax.plot(d['actual-audit-rate'], d['mean'], marker='o', linewidth=2.5,
                markersize=10, label=strategy, color=colors.get(strategy))
        ax.fill_between(d['actual-audit-rate'], d['mean'] - d['std'],
                        d['mean'] + d['std'], alpha=0.2, color=colors.get(strategy))
    ax.axvline(0.04, color='gray', linestyle='--', alpha=0.6, label='umbral hipotético 0.04')
    ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(rate_values)
    ax.set_ylim(-0.05, 1.05)
    if idx == 0:
        ax.set_ylabel('Mean PIR @ tick 50000', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='upper left', fontsize=10, title_fontsize=11)
plt.suptitle('PIR @ tick 50000 vs Audit rate (N=10, 50k steps)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + 'PIR_vs_auditrate_faceted_by_periodfrauds.png', dpi=300, bbox_inches='tight')
print("\nSaved: PIR_vs_auditrate_faceted_by_periodfrauds.png")
plt.close()

# ============================================================================
# PLOT 2: PRA vs audit-rate, faceted by period-frauds
# ============================================================================
fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
if len(period_values) == 1:
    axes = [axes]
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        d = summary_pra[(summary_pra['tax-payer-audit-selection'] == strategy) &
                        (summary_pra['period-frauds'] == period)].sort_values('actual-audit-rate')
        ax.plot(d['actual-audit-rate'], d['mean'], marker='o', linewidth=2.5,
                markersize=10, label=strategy, color=colors.get(strategy))
        ax.fill_between(d['actual-audit-rate'], d['mean'] - d['std'],
                        d['mean'] + d['std'], alpha=0.2, color=colors.get(strategy))
    ax.axvline(0.04, color='gray', linestyle='--', alpha=0.6)
    ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(rate_values)
    ax.set_ylim(-0.05, 1.05)
    if idx == 0:
        ax.set_ylabel('Mean PRA @ tick 50000', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='lower right', fontsize=10, title_fontsize=11)
plt.suptitle('PRA @ tick 50000 vs Audit rate (N=10, 50k steps)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + 'PRA_vs_auditrate_faceted_by_periodfrauds.png', dpi=300, bbox_inches='tight')
print("Saved: PRA_vs_auditrate_faceted_by_periodfrauds.png")
plt.close()

# ============================================================================
# PLOT 3: Heatmaps PIR / PRA (strategy x audit-rate per PF)
# ============================================================================
fig, axes = plt.subplots(2, len(period_values), figsize=(14, 9))
for col, period in enumerate(period_values):
    piv_pir = summary[summary['period-frauds'] == period].pivot(
        index='tax-payer-audit-selection', columns='actual-audit-rate', values='mean')
    piv_pra = summary_pra[summary_pra['period-frauds'] == period].pivot(
        index='tax-payer-audit-selection', columns='actual-audit-rate', values='mean')
    sns.heatmap(piv_pir, annot=True, fmt='.3f', cmap='RdYlGn',
                cbar_kws={'label': 'Mean PIR'}, ax=axes[0, col],
                linewidths=0.5, vmin=0, vmax=1)
    axes[0, col].set_title(f'PIR | Period-Frauds = {period}', fontsize=12, fontweight='bold')
    axes[0, col].set_xlabel('Audit rate')
    axes[0, col].set_ylabel('Estrategia' if col == 0 else '')
    sns.heatmap(piv_pra, annot=True, fmt='.3f', cmap='RdYlGn',
                cbar_kws={'label': 'Mean PRA'}, ax=axes[1, col],
                linewidths=0.5, vmin=0, vmax=1)
    axes[1, col].set_title(f'PRA | Period-Frauds = {period}', fontsize=12, fontweight='bold')
    axes[1, col].set_xlabel('Audit rate')
    axes[1, col].set_ylabel('Estrategia' if col == 0 else '')
plt.suptitle('Heatmaps: Strategy x Audit rate (N=10, 50k steps)',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(OUT + 'heatmaps_PIR_PRA.png', dpi=300, bbox_inches='tight')
print("Saved: heatmaps_PIR_PRA.png")
plt.close()

# ============================================================================
# PLOT 4: Signal coverage vs audit-rate.
# NOTA: fraud-detect-hist solo se actualiza al ser auditado (ventana en
# *auditorías*, no en ticks), luego esto mide "detección en las últimas PF
# auditorías", no influencia actual. Sin línea teórica: la ley ingenua
# rate x eff x grado x PF es inválida bajo esta mecánica.
# ============================================================================
fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
if len(period_values) == 1:
    axes = [axes]
xs = np.array(rate_values)
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        d = summary_cov[(summary_cov['tax-payer-audit-selection'] == strategy) &
                        (summary_cov['period-frauds'] == period)].sort_values('actual-audit-rate')
        ax.plot(d['actual-audit-rate'], d['mean'], marker='s', linewidth=2.5,
                markersize=10, label=strategy, color=colors.get(strategy))
        ax.fill_between(d['actual-audit-rate'], d['mean'] - d['std'],
                        d['mean'] + d['std'], alpha=0.2, color=colors.get(strategy))
    ax.axvline(0.04, color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(rate_values)
    ax.set_ylim(-0.05, 1.15)
    if idx == 0:
        ax.set_ylabel('Frac. con detección en últ. PF auditorías', fontsize=11, fontweight='bold')
        ax.legend(title='Estrategia', loc='upper left', fontsize=10, title_fontsize=11)
plt.suptitle('Detecciones recordadas @ tick 50000 (N=10, 50k steps)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + 'signal_coverage.png', dpi=300, bbox_inches='tight')
print("Saved: signal_coverage.png")
plt.close()

# ============================================================================
# PLOT 5: Detection rate (acum/50000) vs audit-rate
# ============================================================================
# acum_* cuenta desde tick 25000 => ventana de 25000 ticks, no 50000
df['detection_rate_per_tick'] = df['acum_frauds_detected'] / 25000
summary_det = df.groupby(grp)['detection_rate_per_tick'].agg(['mean', 'std']).reset_index()
summary_det.to_csv(OUT + 'summary_detection_rate.csv', index=False)

fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
if len(period_values) == 1:
    axes = [axes]
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        d = summary_det[(summary_det['tax-payer-audit-selection'] == strategy) &
                        (summary_det['period-frauds'] == period)].sort_values('actual-audit-rate')
        ax.plot(d['actual-audit-rate'], d['mean'], marker='D', linewidth=2.5,
                markersize=10, label=strategy, color=colors.get(strategy))
        ax.fill_between(d['actual-audit-rate'], d['mean'] - d['std'],
                        d['mean'] + d['std'], alpha=0.2, color=colors.get(strategy))
    ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(rate_values)
    if idx == 0:
        ax.set_ylabel('Detection rate (frauds/tick)', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='upper left', fontsize=10, title_fontsize=11)
plt.suptitle('Tasa de detección @ tick 50000 (N=10, 50k steps)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + 'detection_rate.png', dpi=300, bbox_inches='tight')
print("Saved: detection_rate.png")
plt.close()

# ============================================================================
# PLOT 6: convergence check (final PIR - PIAR_10000)
# ============================================================================
df['PIR_delta'] = df[PIR] - df['PIAR_10000']
summary_delta = df.groupby(grp)['PIR_delta'].agg(['mean', 'std']).reset_index()

fig, axes = plt.subplots(1, len(period_values), figsize=(14, 6), sharey=True)
if len(period_values) == 1:
    axes = [axes]
for idx, period in enumerate(period_values):
    ax = axes[idx]
    for strategy in strategies:
        d = summary_delta[(summary_delta['tax-payer-audit-selection'] == strategy) &
                          (summary_delta['period-frauds'] == period)].sort_values('actual-audit-rate')
        ax.plot(d['actual-audit-rate'], d['mean'], marker='^', linewidth=2.5,
                markersize=10, label=strategy, color=colors.get(strategy))
        ax.fill_between(d['actual-audit-rate'], d['mean'] - d['std'],
                        d['mean'] + d['std'], alpha=0.2, color=colors.get(strategy))
    ax.axhline(0, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
    ax.set_title(f'Period-Frauds = {period}', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xticks(rate_values)
    if idx == 0:
        ax.set_ylabel('ΔPIR (final − tick 10000)', fontsize=12, fontweight='bold')
        ax.legend(title='Estrategia', loc='best', fontsize=10, title_fontsize=11)
plt.suptitle('Convergencia: cambio de PIR entre t=10000 y t=50000 (N=3)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + 'PIR_delta_convergence.png', dpi=300, bbox_inches='tight')
print("Saved: PIR_delta_convergence.png")
plt.close()

print("\n" + "=" * 70)
print("ALL DONE")
print("=" * 70)
