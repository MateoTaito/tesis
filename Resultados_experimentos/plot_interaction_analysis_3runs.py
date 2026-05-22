import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Read the new results file with 3 repetitions
with open('/home/MTS/UAI/tesis/Resultados_experimentos/emu_exp_paper_2.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[6]
data_rows = rows[7:]

df = pd.DataFrame(data_rows, columns=header)

# Convert numeric columns
df['period-frauds'] = df['period-frauds'].astype(int)
df['mean [risk-aversion] of tax-payers'] = df['mean [risk-aversion] of tax-payers'].astype(float)
df['mean [pct-income-report] of tax-payers'] = df['mean [pct-income-report] of tax-payers'].astype(float)
df['[run number]'] = df['[run number]'].astype(int)

# Calculate means across runs
summary = df.groupby(['tax-payer-audit-selection', 'period-frauds'])[
    ['mean [risk-aversion] of tax-payers', 'mean [pct-income-report] of tax-payers']
].mean().reset_index()

summary.columns = ['Strategy', 'Period Frauds', 'Mean Risk Aversion', 'Mean Income Report']
summary = summary.sort_values(['Period Frauds', 'Strategy'])

print("SUMMARY - Mean Risk Aversion (3 runs averaged):")
print(summary.to_string(index=False))

# ============================================================================
# PLOT 1: Interaction Plot - Line plot
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

strategies = sorted(summary['Strategy'].unique())
colors = {'random': '#1f77b4', 'income-level': '#ff7f0e', 'strategic': '#2ca02c'}

for strategy in strategies:
    data = summary[summary['Strategy'] == strategy].sort_values('Period Frauds')
    ax.plot(data['Period Frauds'], data['Mean Risk Aversion'], 
            marker='o', linewidth=2.5, markersize=10, 
            label=strategy, color=colors.get(strategy, '#000000'))

ax.set_xlabel('Period Frauds (Social Memory Level)', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Risk Aversion', fontsize=12, fontweight='bold')
ax.set_title('Mean Risk Aversion by Strategy and Social Memory\n(3 runs averaged)', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(title='Audit Selection Strategy', fontsize=11, title_fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xticks(sorted(summary['Period Frauds'].unique()))

plt.tight_layout()
plt.savefig('/home/MTS/UAI/tesis/Resultados_experimentos/interaction_plot_line_3runs.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PLOT 2: Bar Plot - Grouped by Strategy
# ============================================================================
fig, ax = plt.subplots(figsize=(11, 6))

x = np.arange(len(strategies))
width = 0.35

period_values = sorted(summary['Period Frauds'].unique())
for i, period in enumerate(period_values):
    data = summary[summary['Period Frauds'] == period].sort_values('Strategy')
    data = data.set_index('Strategy').reindex(strategies).reset_index()
    offset = (i - len(period_values)/2 + 0.5) * width
    ax.bar(x + offset, data['Mean Risk Aversion'], width, 
           label=f'Period Frauds = {int(period)}', alpha=0.8)

ax.set_xlabel('Audit Selection Strategy', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Risk Aversion', fontsize=12, fontweight='bold')
ax.set_title('Mean Risk Aversion: Strategy vs Social Memory\n(3 runs averaged)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(strategies, fontsize=11)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig('/home/MTS/UAI/tesis/Resultados_experimentos/interaction_plot_grouped_bars_3runs.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PLOT 3: Heatmap
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 5))

pivot_data = summary.pivot(index='Strategy', columns='Period Frauds', values='Mean Risk Aversion')
pivot_data = pivot_data.sort_index()

sns.heatmap(pivot_data, annot=True, fmt='.4f', cmap='RdYlGn_r', 
            cbar_kws={'label': 'Mean Risk Aversion'}, ax=ax, linewidths=0.5)

ax.set_xlabel('Period Frauds (Social Memory Level)', fontsize=12, fontweight='bold')
ax.set_ylabel('Audit Selection Strategy', fontsize=12, fontweight='bold')
ax.set_title('Mean Risk Aversion Heatmap\n(3 runs averaged)', 
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('/home/MTS/UAI/tesis/Resultados_experimentos/interaction_plot_heatmap_3runs.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PLOT 4: Faceted Plot
# ============================================================================
fig, axes = plt.subplots(1, len(period_values), figsize=(14, 5))

if len(period_values) == 1:
    axes = [axes]

for idx, period in enumerate(sorted(period_values)):
    ax = axes[idx]
    data = summary[summary['Period Frauds'] == period].sort_values('Strategy')
    
    bars = ax.bar(range(len(data)), data['Mean Risk Aversion'], color='steelblue', alpha=0.8)
    
    for i, bar in enumerate(bars):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.4f}', ha='center', va='bottom', fontsize=10)
    
    ax.set_xticks(range(len(data)))
    ax.set_xticklabels(data['Strategy'], rotation=45, ha='right')
    ax.set_ylabel('Mean Risk Aversion', fontsize=11, fontweight='bold')
    ax.set_title(f'Period Frauds = {int(period)}', fontsize=12, fontweight='bold')
    ax.set_ylim(0, max(summary['Mean Risk Aversion']) * 1.15)
    ax.grid(True, alpha=0.3, axis='y')

plt.suptitle('Mean Risk Aversion by Strategy\n(3 runs averaged, stratified by Social Memory)', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('/home/MTS/UAI/tesis/Resultados_experimentos/interaction_plot_faceted_3runs.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PLOT 5: Income Report Analysis
# ============================================================================
fig, ax = plt.subplots(figsize=(10, 6))

for strategy in strategies:
    data = summary[summary['Strategy'] == strategy].sort_values('Period Frauds')
    ax.plot(data['Period Frauds'], data['Mean Income Report'], 
            marker='s', linewidth=2.5, markersize=10, 
            label=strategy, color=colors.get(strategy, '#000000'))

ax.set_xlabel('Period Frauds (Social Memory Level)', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Income Reported (%)', fontsize=12, fontweight='bold')
ax.set_title('Mean Income Reported by Strategy and Social Memory\n(3 runs averaged)', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(title='Audit Selection Strategy', fontsize=11, title_fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xticks(sorted(summary['Period Frauds'].unique()))

plt.tight_layout()
plt.savefig('/home/MTS/UAI/tesis/Resultados_experimentos/income_report_plot_3runs.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# SAVE SUMMARY TABLE
# ============================================================================
summary_pivot = summary.pivot(index='Strategy', columns='Period Frauds', values='Mean Risk Aversion')
summary_pivot.to_csv('/home/MTS/UAI/tesis/Resultados_experimentos/summary_3runs_mean_risk_aversion.csv')

income_pivot = summary.pivot(index='Strategy', columns='Period Frauds', values='Mean Income Report')
income_pivot.to_csv('/home/MTS/UAI/tesis/Resultados_experimentos/summary_3runs_mean_income_report.csv')

print("\n✓ All plots generated successfully!")
print("✓ summary_3runs_mean_risk_aversion.csv")
print("✓ summary_3runs_mean_income_report.csv")
