import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent

# Read the CSV file manually using csv.reader to handle the format correctly
with open(BASE / 'exp_emu_paper.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Extract header (row 6) and data (rows 7 onwards)
header = rows[6]
data_rows = rows[7:]

# Create DataFrame
df = pd.DataFrame(data_rows, columns=header)

# Convert numeric columns
df['period-frauds'] = df['period-frauds'].astype(int)
df['mean [risk-aversion] of tax-payers'] = df['mean [risk-aversion] of tax-payers'].astype(float)

print("Dataset shape:", df.shape)
print("\nFirst few rows:")
print(df.head())
print("\nUnique strategies:", df['tax-payer-audit-selection'].unique())
print("Unique period-frauds:", sorted(df['period-frauds'].unique()))

# Create a summary table: Mean Risk Aversion by Strategy and Period Frauds
summary = df.groupby(['tax-payer-audit-selection', 'period-frauds'])['mean [risk-aversion] of tax-payers'].mean().reset_index()
summary.columns = ['Strategy', 'Period Frauds', 'Mean Risk Aversion']
summary = summary.sort_values(['Period Frauds', 'Strategy'])

print("\n\nSummary Statistics:")
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
ax.set_title('Interaction Plot: Mean Risk Aversion by Strategy and Period Frauds', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(title='Audit Selection Strategy', fontsize=11, title_fontsize=12)
ax.grid(True, alpha=0.3)
ax.set_xticks(sorted(summary['Period Frauds'].unique()))

plt.tight_layout()
plt.savefig(BASE / 'interaction_plot_line.png', dpi=300, bbox_inches='tight')
print("\n✓ Saved: interaction_plot_line.png")
plt.close()

# ============================================================================
# PLOT 2: Bar Plot - Grouped by Strategy
# ============================================================================
fig, ax = plt.subplots(figsize=(11, 6))

# Prepare data for grouped bar plot
x = np.arange(len(strategies))
width = 0.35

period_values = sorted(summary['Period Frauds'].unique())
for i, period in enumerate(period_values):
    data = summary[summary['Period Frauds'] == period].sort_values('Strategy')
    # Ensure data is in the same order as strategies
    data = data.set_index('Strategy').reindex(strategies).reset_index()
    offset = (i - len(period_values)/2 + 0.5) * width
    ax.bar(x + offset, data['Mean Risk Aversion'], width, 
           label=f'Period Frauds = {int(period)}', alpha=0.8)

ax.set_xlabel('Audit Selection Strategy', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Risk Aversion', fontsize=12, fontweight='bold')
ax.set_title('Mean Risk Aversion: Strategy vs Period Frauds (Grouped)', 
             fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(strategies, fontsize=11)
ax.legend(fontsize=11, loc='best')
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(BASE / 'interaction_plot_grouped_bars.png', dpi=300, bbox_inches='tight')
print("✓ Saved: interaction_plot_grouped_bars.png")
plt.close()

# ============================================================================
# PLOT 3: Heatmap
# ============================================================================
fig, ax = plt.subplots(figsize=(8, 5))

# Create pivot table for heatmap
pivot_data = summary.pivot(index='Strategy', columns='Period Frauds', values='Mean Risk Aversion')

# Sort by strategy for better visualization
pivot_data = pivot_data.sort_index()

sns.heatmap(pivot_data, annot=True, fmt='.4f', cmap='RdYlGn_r', 
            cbar_kws={'label': 'Mean Risk Aversion'}, ax=ax, linewidths=0.5)

ax.set_xlabel('Period Frauds (Social Memory Level)', fontsize=12, fontweight='bold')
ax.set_ylabel('Audit Selection Strategy', fontsize=12, fontweight='bold')
ax.set_title('Mean Risk Aversion Heatmap: Strategy × Period Frauds', 
             fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(BASE / 'interaction_plot_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: interaction_plot_heatmap.png")
plt.close()

# ============================================================================
# PLOT 4: Faceted Plot (separate panels per Period Frauds)
# ============================================================================
fig, axes = plt.subplots(1, len(period_values), figsize=(14, 5))

if len(period_values) == 1:
    axes = [axes]

for idx, period in enumerate(sorted(period_values)):
    ax = axes[idx]
    data = summary[summary['Period Frauds'] == period].sort_values('Strategy')
    
    bars = ax.bar(range(len(data)), data['Mean Risk Aversion'], color='steelblue', alpha=0.8)
    
    # Add value labels on bars
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

plt.suptitle('Mean Risk Aversion by Strategy (Stratified by Period Frauds)', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(BASE / 'interaction_plot_faceted.png', dpi=300, bbox_inches='tight')
print("✓ Saved: interaction_plot_faceted.png")
plt.close()

# ============================================================================
# SUMMARY TABLE TO CSV
# ============================================================================
summary_pivot = summary.pivot(index='Strategy', columns='Period Frauds', values='Mean Risk Aversion')
summary_pivot.to_csv(BASE / 'summary_mean_risk_aversion.csv')
print("✓ Saved: summary_mean_risk_aversion.csv")

print("\n" + "="*70)
print("SUMMARY TABLE: Mean Risk Aversion")
print("="*70)
print(summary_pivot.to_string())
print("\n✓ All plots generated successfully!")
