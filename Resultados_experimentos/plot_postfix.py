import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'Resultados_experimentos/Exp_post_fix/exp_emu_paper_postfix.csv'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'Resultados_experimentos/Exp_post_fix/'

with open(SRC) as f:
    rows = list(csv.reader(f))
header = rows[6]
data = rows[7:]
df = pd.DataFrame(data, columns=header)

df['period-frauds'] = df['period-frauds'].astype(int)
df['mean [pct-income-report] of tax-payers'] = df['mean [pct-income-report] of tax-payers'].astype(float)
df['mean [risk-aversion] of tax-payers'] = df['mean [risk-aversion] of tax-payers'].astype(float)
df['acum_frauds_detected'] = df['acum_frauds_detected'].astype(float)
df['acum_frauds_perpretated'] = df['acum_frauds_perpretated'].astype(float)
df['acum_frauds_perpretated_all_ags'] = df['acum_frauds_perpretated_all_ags'].astype(float)
df['SS_PIAR'] = df['SS_PIAR'].astype(int)
df['SS_RA'] = df['SS_RA'].astype(int)

print("="*70)
print("DATOS POST-FIX — Exper_emu_paper (inst-mem=1, noise=0, 3 reps, 10k steps)")
print("="*70)
print(f"  Filas: {len(df)}")
print(f"  Estrategias: {sorted(df['tax-payer-audit-selection'].unique())}")
print(f"  Period-frauds: {sorted(df['period-frauds'].unique())}")

PIR = 'mean [pct-income-report] of tax-payers'
PRA = 'mean [risk-aversion] of tax-payers'

summary_pir = df.groupby(['tax-payer-audit-selection', 'period-frauds'])[PIR].agg(['mean', 'std', 'count']).reset_index()
summary_pra = df.groupby(['tax-payer-audit-selection', 'period-frauds'])[PRA].agg(['mean', 'std', 'count']).reset_index()

print("\n" + "="*70)
print("SUMMARY: Mean PIR (pct-income-report)")
print("="*70)
print(summary_pir.to_string(index=False))
print("\n" + "="*70)
print("SUMMARY: Mean PRA (risk-aversion)")
print("="*70)
print(summary_pra.to_string(index=False))

strategies = sorted(df['tax-payer-audit-selection'].unique())
colors = {'random': '#1f77b4', 'income-level': '#ff7f0e', 'strategic': '#2ca02c'}
period_values = sorted(df['period-frauds'].unique())

# ============================================================================
# PLOT 1: PIR interaction (line)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for strategy in strategies:
    data = summary_pir[summary_pir['tax-payer-audit-selection'] == strategy].sort_values('period-frauds')
    means = data['mean'].values
    stds = data['std'].values
    periods = data['period-frauds'].values
    ax.plot(periods, means, marker='o', linewidth=2.5, markersize=10,
            label=strategy, color=colors.get(strategy, '#000000'))
    ax.fill_between(periods, means - stds, means + stds, alpha=0.2, color=colors.get(strategy, '#000000'))
ax.set_xlabel('Period Frauds (Social Memory)', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Pct-Income-Reported (PIR)', fontsize=12, fontweight='bold')
ax.set_title('Interaction Plot: PIR by Strategy × Period-Frauds\n(post-fix, inst-mem=1, noise=0)', fontsize=13, fontweight='bold', pad=20)
ax.legend(title='Audit Strategy', fontsize=11, title_fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xticks(period_values)
ax.set_ylim(0, 1.0)
plt.tight_layout()
plt.savefig(OUT + 'interaction_PIR_line.png', dpi=300, bbox_inches='tight')
print("\nSaved: interaction_PIR_line.png")
plt.close()

# ============================================================================
# PLOT 2: PRA interaction (line)
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))
for strategy in strategies:
    data = summary_pra[summary_pra['tax-payer-audit-selection'] == strategy].sort_values('period-frauds')
    means = data['mean'].values
    stds = data['std'].values
    periods = data['period-frauds'].values
    ax.plot(periods, means, marker='o', linewidth=2.5, markersize=10,
            label=strategy, color=colors.get(strategy, '#000000'))
    ax.fill_between(periods, means - stds, means + stds, alpha=0.2, color=colors.get(strategy, '#000000'))
ax.set_xlabel('Period Frauds (Social Memory)', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Risk Aversion (PRA)', fontsize=12, fontweight='bold')
ax.set_title('Interaction Plot: PRA by Strategy × Period-Frauds\n(post-fix, inst-mem=1, noise=0)', fontsize=13, fontweight='bold', pad=20)
ax.legend(title='Audit Strategy', fontsize=11, title_fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xticks(period_values)
ax.set_ylim(0, 1.0)
plt.tight_layout()
plt.savefig(OUT + 'interaction_PRA_line.png', dpi=300, bbox_inches='tight')
print("Saved: interaction_PRA_line.png")
plt.close()

# ============================================================================
# PLOT 3: PIR grouped bars
# ============================================================================
fig, ax = plt.subplots(figsize=(11, 6))
x = np.arange(len(strategies))
width = 0.35
for i, period in enumerate(period_values):
    data = summary_pir[summary_pir['period-frauds'] == period].set_index('tax-payer-audit-selection').reindex(strategies).reset_index()
    offset = (i - len(period_values)/2 + 0.5) * width
    bars = ax.bar(x + offset, data['mean'], width, yerr=data['std'],
                  label=f'Period Frauds = {int(period)}', alpha=0.8, capsize=4)
ax.set_xlabel('Audit Selection Strategy', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Pct-Income-Reported (PIR)', fontsize=12, fontweight='bold')
ax.set_title('PIR by Strategy, grouped by Period-Frauds', fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(strategies, fontsize=11)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 1.0)
plt.tight_layout()
plt.savefig(OUT + 'interaction_PIR_grouped_bars.png', dpi=300, bbox_inches='tight')
print("Saved: interaction_PIR_grouped_bars.png")
plt.close()

# ============================================================================
# PLOT 4: PRA grouped bars
# ============================================================================
fig, ax = plt.subplots(figsize=(11, 6))
x = np.arange(len(strategies))
width = 0.35
for i, period in enumerate(period_values):
    data = summary_pra[summary_pra['period-frauds'] == period].set_index('tax-payer-audit-selection').reindex(strategies).reset_index()
    offset = (i - len(period_values)/2 + 0.5) * width
    bars = ax.bar(x + offset, data['mean'], width, yerr=data['std'],
                  label=f'Period Frauds = {int(period)}', alpha=0.8, capsize=4)
ax.set_xlabel('Audit Selection Strategy', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Risk Aversion (PRA)', fontsize=12, fontweight='bold')
ax.set_title('PRA by Strategy, grouped by Period-Frauds', fontsize=13, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(strategies, fontsize=11)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 1.0)
plt.tight_layout()
plt.savefig(OUT + 'interaction_PRA_grouped_bars.png', dpi=300, bbox_inches='tight')
print("Saved: interaction_PRA_grouped_bars.png")
plt.close()

# ============================================================================
# PLOT 5: Heatmaps (PIR and PRA)
# ============================================================================
fig, axes = plt.subplots(1, 2, figsize=(14, 5))
pivot_pir = summary_pir.pivot(index='tax-payer-audit-selection', columns='period-frauds', values='mean')
pivot_pra = summary_pra.pivot(index='tax-payer-audit-selection', columns='period-frauds', values='mean')
sns.heatmap(pivot_pir, annot=True, fmt='.4f', cmap='RdYlGn',
            cbar_kws={'label': 'Mean PIR'}, ax=axes[0], linewidths=0.5, vmin=0, vmax=1)
axes[0].set_title('Mean PIR', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Period-Frauds')
axes[0].set_ylabel('Strategy')
sns.heatmap(pivot_pra, annot=True, fmt='.4f', cmap='RdYlGn',
            cbar_kws={'label': 'Mean PRA'}, ax=axes[1], linewidths=0.5, vmin=0, vmax=1)
axes[1].set_title('Mean PRA', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Period-Frauds')
axes[1].set_ylabel('')
plt.suptitle('Post-fix: Strategy × Period-Frauds heatmaps (inst-mem=1, noise=0)', fontsize=13, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(OUT + 'interaction_heatmaps.png', dpi=300, bbox_inches='tight')
print("Saved: interaction_heatmaps.png")
plt.close()

# ============================================================================
# PLOT 6: Faceted bars (PIR and PRA, stratified by period-frauds)
# ============================================================================
fig, axes = plt.subplots(2, len(period_values), figsize=(14, 8))
for idx, period in enumerate(period_values):
    data_pir = summary_pir[summary_pir['period-frauds'] == period].sort_values('tax-payer-audit-selection')
    data_pra = summary_pra[summary_pra['period-frauds'] == period].sort_values('tax-payer-audit-selection')
    bars = axes[0, idx].bar(range(len(data_pir)), data_pir['mean'], yerr=data_pir['std'], color='steelblue', alpha=0.8, capsize=4)
    for i, bar in enumerate(bars):
        axes[0, idx].text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                          f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9)
    axes[0, idx].set_xticks(range(len(data_pir)))
    axes[0, idx].set_xticklabels(data_pir['tax-payer-audit-selection'], rotation=45, ha='right')
    axes[0, idx].set_ylabel('Mean PIR', fontsize=10, fontweight='bold')
    axes[0, idx].set_title(f'Period-Frauds = {int(period)}', fontsize=11, fontweight='bold')
    axes[0, idx].set_ylim(0, 1.0)
    axes[0, idx].grid(True, alpha=0.3, axis='y')

    bars = axes[1, idx].bar(range(len(data_pra)), data_pra['mean'], yerr=data_pra['std'], color='coral', alpha=0.8, capsize=4)
    for i, bar in enumerate(bars):
        axes[1, idx].text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                          f'{bar.get_height():.3f}', ha='center', va='bottom', fontsize=9)
    axes[1, idx].set_xticks(range(len(data_pra)))
    axes[1, idx].set_xticklabels(data_pra['tax-payer-audit-selection'], rotation=45, ha='right')
    axes[1, idx].set_ylabel('Mean PRA', fontsize=10, fontweight='bold')
    axes[1, idx].set_ylim(0, 1.0)
    axes[1, idx].grid(True, alpha=0.3, axis='y')

plt.suptitle('Faceted: PIR (top) and PRA (bottom) by Strategy, stratified by Period-Frauds',
             fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig(OUT + 'interaction_faceted.png', dpi=300, bbox_inches='tight')
print("Saved: interaction_faceted.png")
plt.close()

# ============================================================================
# Save summary CSV
# ============================================================================
summary_pir.to_csv(OUT + 'summary_mean_pir.csv', index=False)
summary_pra.to_csv(OUT + 'summary_mean_pra.csv', index=False)
print("Saved: summary_mean_pir.csv, summary_mean_pra.csv")

print("\n" + "="*70)
print("ALL DONE")
print("="*70)
