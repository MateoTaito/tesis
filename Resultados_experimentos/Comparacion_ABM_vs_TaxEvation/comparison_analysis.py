import csv
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

BASE = Path(__file__).resolve().parent
PARENT = BASE.parent

# ============================================================================
# READ ABM_Original (Spreadsheet format - complex)
# ============================================================================

with open(PARENT / 'Original_exp.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

# Find the actual data row (after [final value])
header_idx = None
for i, row in enumerate(rows):
    if row and row[0] == '[final value]':
        header_idx = i
        break

# Extract headers and data
if header_idx:
    headers = rows[header_idx]
    # Parse the complex header structure
    data_row = rows[header_idx + 1]
    
    # Extract parameters and values from the nested structure
    abm_data = []
    run_num = 1
    
    # This CSV has a complex structure with repeated parameters
    # We need to parse it carefully
    i = 1  # Start after [final value]
    while i < len(headers):
        if '[step]' in headers[i]:
            # Found a run, extract all metrics for this run
            step_val = data_row[i] if i < len(data_row) else 0
            pir = data_row[i+1] if i+1 < len(data_row) else 0
            pra = data_row[i+2] if i+2 < len(data_row) else 0
            
            # Look back for strategy and period-frauds
            # These are in the fixed columns at the beginning
            strategy_idx = None
            period_idx = None
            
            for j in range(1, i):
                if 'tax-payer-audit-selection' in headers[j]:
                    strategy_idx = j
                if 'period-frauds' in headers[j]:
                    period_idx = j
            
            strategy = data_row[strategy_idx] if strategy_idx and strategy_idx < len(data_row) else 'unknown'
            period = data_row[period_idx] if period_idx and period_idx < len(data_row) else 'unknown'
            
            abm_data.append({
                'run': run_num,
                'strategy': strategy,
                'period': period,
                'risk_aversion': float(pra) if pra else 0
            })
            
            i += 10  # Skip ahead
            run_num += 1
        else:
            i += 1

# Simpler approach: manually parse the data structure
# The file has repeating blocks of (step, PIR, PRA, etc.) for each run
# Let's extract more carefully

abm_df = pd.DataFrame()

# Re-read and use a different approach
# Column pattern: empty, [step], PIR, PRA, PIAR_10000, PRA_10000, acum_detected, acum_perpetrated, acum_all, SS_PIAR, SS_RA (10 cols per run)

data_row_idx = header_idx + 1
if data_row_idx < len(rows):
    data = rows[data_row_idx]
    
    # Extract strategy and period from fixed columns
    all_strategies = []
    all_periods = []
    
    # Find strategy and period rows
    for row_idx, row in enumerate(rows):
        if row and 'tax-payer-audit-selection' in row[0]:
            # This row has all the strategies
            all_strategies = [x for x in row[1:] if x]
        if row and 'period-frauds' in row[0]:
            # This row has all the periods
            all_periods = [x for x in row[1:] if x]
    
    # Now extract data for each run
    # Data starts after [final value] row
    # We have 18 runs (6 combinations × 3 repetitions)
    
    pra_values = []
    run_configs = []
    
    # The data row has empty first value, then repeats pattern
    col_idx = 1
    run_num = 0
    
    while col_idx < len(data) and run_num < 18:
        # Each run has: [step], PIR, PRA, ... (11 columns)
        if col_idx + 2 < len(data):
            try:
                pra = float(data[col_idx + 2])  # PRA is 3rd column in each block
                pra_values.append(pra)
                run_num += 1
                col_idx += 11  # Move to next run
            except:
                col_idx += 1
        else:
            break
    
    # Match runs with their configs (6 configs × 3 reps each)
    configs = [
        ('random', 1),
        ('random', 1),
        ('random', 1),
        ('random', 5),
        ('random', 5),
        ('random', 5),
        ('income-level', 1),
        ('income-level', 1),
        ('income-level', 1),
        ('income-level', 5),
        ('income-level', 5),
        ('income-level', 5),
        ('strategic', 1),
        ('strategic', 1),
        ('strategic', 1),
        ('strategic', 5),
        ('strategic', 5),
        ('strategic', 5),
    ]
    
    abm_data_list = []
    for i, (strategy, period) in enumerate(configs):
        if i < len(pra_values):
            abm_data_list.append({
                'model': 'ABM_Original',
                'strategy': strategy,
                'period': period,
                'risk_aversion': pra_values[i]
            })
    
    abm_df = pd.DataFrame(abm_data_list)

print("ABM_Original Data:")
print(abm_df.head(10))
print(f"Shape: {abm_df.shape}")

# ============================================================================
# READ Tax-Evation (3 runs)
# ============================================================================

with open(BASE / 'emu_exp_paper_2.csv', 'r') as f:
    reader = csv.reader(f)
    rows = list(reader)

header = rows[6]
data_rows = rows[7:]

tax_df = pd.DataFrame(data_rows, columns=header)
tax_df['period-frauds'] = tax_df['period-frauds'].astype(int)
tax_df['mean [risk-aversion] of tax-payers'] = tax_df['mean [risk-aversion] of tax-payers'].astype(float)

tax_df['model'] = 'Tax-Evation (inst_mem=1)'
tax_df_renamed = tax_df[[
    'model',
    'tax-payer-audit-selection',
    'period-frauds',
    'mean [risk-aversion] of tax-payers'
]].copy()
tax_df_renamed.columns = ['model', 'strategy', 'period', 'risk_aversion']
tax_df_renamed['strategy'] = tax_df_renamed['strategy'].astype(str)
tax_df_renamed['period'] = tax_df_renamed['period'].astype(int)
tax_df_renamed['risk_aversion'] = pd.to_numeric(tax_df_renamed['risk_aversion'])

print("\nTax-Evation Data:")
print(tax_df_renamed.head(10))
print(f"Shape: {tax_df_renamed.shape}")

# ============================================================================
# CALCULATE MEANS FOR EACH MODEL
# ============================================================================

abm_summary = abm_df.groupby(['strategy', 'period'])['risk_aversion'].agg(['mean', 'std', 'count']).reset_index()
abm_summary['model'] = 'ABM_Original'

tax_summary = tax_df_renamed.groupby(['strategy', 'period'])['risk_aversion'].agg(['mean', 'std', 'count']).reset_index()
tax_summary['model'] = 'Tax-Evation (inst_mem=1)'

print("\nABM Summary:")
print(abm_summary)
print("\nTax-Evation Summary:")
print(tax_summary)

# ============================================================================
# PLOT 1: Comparison Line Plot
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 7))

strategies = sorted(set(abm_summary['strategy'].unique()) | set(tax_summary['strategy'].unique()))
colors_model = {'ABM_Original': '#1f77b4', 'Tax-Evation (inst_mem=1)': '#d62728'}
markers_strategy = {'random': 'o', 'income-level': 's', 'strategic': '^'}

for model in ['ABM_Original', 'Tax-Evation (inst_mem=1)']:
    for strategy in strategies:
        if model == 'ABM_Original':
            data = abm_summary[(abm_summary['strategy'] == strategy)].sort_values('period')
        else:
            data = tax_summary[(tax_summary['strategy'] == strategy)].sort_values('period')
        
        if len(data) > 0:
            ax.errorbar(data['period'], data['mean'], yerr=data['std'], 
                       marker=markers_strategy[strategy], 
                       linestyle='-' if model == 'ABM_Original' else '--',
                       linewidth=2.5, markersize=10,
                       label=f'{model} - {strategy}',
                       color=colors_model[model], capsize=5, capthick=2, alpha=0.8)

ax.set_xlabel('Period Frauds (Social Memory)', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Risk Aversion', fontsize=12, fontweight='bold')
ax.set_title('ABM_Original vs Tax-Evation (institutional-memory=1)\nMean Risk Aversion by Strategy', 
             fontsize=14, fontweight='bold', pad=20)
ax.legend(fontsize=10, loc='best', ncol=2)
ax.grid(True, alpha=0.3)
ax.set_xticks(sorted(set(abm_summary['period'].unique()) | set(tax_summary['period'].unique())))

plt.tight_layout()
plt.savefig(BASE / 'comparison_line_plot.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PLOT 2: Grouped Bar Comparison
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

periods = sorted(set(abm_summary['period'].unique()) | set(tax_summary['period'].unique()))

for plot_idx, period in enumerate(periods):
    ax = axes[plot_idx]
    
    abm_data = abm_summary[abm_summary['period'] == period].sort_values('strategy')
    tax_data = tax_summary[tax_summary['period'] == period].sort_values('strategy')
    
    x = np.arange(len(strategies))
    width = 0.35
    
    # ABM bars
    abm_means = [abm_data[abm_data['strategy'] == s]['mean'].values[0] if len(abm_data[abm_data['strategy'] == s]) > 0 else 0 for s in strategies]
    abm_stds = [abm_data[abm_data['strategy'] == s]['std'].values[0] if len(abm_data[abm_data['strategy'] == s]) > 0 else 0 for s in strategies]
    
    ax.bar(x - width/2, abm_means, width, label='ABM_Original', 
           yerr=abm_stds, capsize=5, alpha=0.8, color='#1f77b4')
    
    # Tax-Evation bars
    tax_means = [tax_data[tax_data['strategy'] == s]['mean'].values[0] if len(tax_data[tax_data['strategy'] == s]) > 0 else 0 for s in strategies]
    tax_stds = [tax_data[tax_data['strategy'] == s]['std'].values[0] if len(tax_data[tax_data['strategy'] == s]) > 0 else 0 for s in strategies]
    
    ax.bar(x + width/2, tax_means, width, label='Tax-Evation (inst_mem=1)',
           yerr=tax_stds, capsize=5, alpha=0.8, color='#d62728')
    
    ax.set_xlabel('Strategy', fontsize=11, fontweight='bold')
    ax.set_ylabel('Mean Risk Aversion', fontsize=11, fontweight='bold')
    ax.set_title(f'Period Frauds = {int(period)}', fontsize=12, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(strategies, fontsize=10)
    ax.grid(True, alpha=0.3, axis='y')
    
    if plot_idx == 0:
        ax.legend(fontsize=10)

plt.suptitle('Mean Risk Aversion Comparison: ABM vs Tax-Evation', 
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(BASE / 'comparison_grouped_bars.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PLOT 3: Difference Heatmap
# ============================================================================

fig, ax = plt.subplots(figsize=(10, 6))

# Create difference table
diff_data = []
for strategy in strategies:
    for period in periods:
        abm_val = abm_summary[(abm_summary['strategy'] == strategy) & (abm_summary['period'] == period)]['mean'].values
        tax_val = tax_summary[(tax_summary['strategy'] == strategy) & (tax_summary['period'] == period)]['mean'].values
        
        if len(abm_val) > 0 and len(tax_val) > 0:
            diff = tax_val[0] - abm_val[0]
            diff_data.append({'Strategy': strategy, 'Period': period, 'Difference': diff})

diff_df = pd.DataFrame(diff_data)
pivot_diff = diff_df.pivot(index='Strategy', columns='Period', values='Difference')

sns.heatmap(pivot_diff, annot=True, fmt='.6f', cmap='RdBu_r', center=0,
            cbar_kws={'label': 'Difference (Tax-Evation - ABM)'}, ax=ax, linewidths=0.5)

ax.set_xlabel('Period Frauds', fontsize=12, fontweight='bold')
ax.set_ylabel('Strategy', fontsize=12, fontweight='bold')
ax.set_title('Difference in Mean Risk Aversion\n(Tax-Evation - ABM_Original)\nPositive = Tax-Evation higher', 
             fontsize=13, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig(BASE / 'comparison_difference_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# PLOT 4: Box Plot Comparison
# ============================================================================

fig, ax = plt.subplots(figsize=(12, 6))

# Prepare data for box plot
combined_data = []
for _, row in abm_df.iterrows():
    combined_data.append({
        'model': 'ABM_Original',
        'strategy': row['strategy'],
        'period': int(row['period']),
        'risk_aversion': row['risk_aversion']
    })

for _, row in tax_df_renamed.iterrows():
    combined_data.append({
        'model': 'Tax-Evation',
        'strategy': row['strategy'],
        'period': int(row['period']),
        'risk_aversion': row['risk_aversion']
    })

combined_df = pd.DataFrame(combined_data)

# Create labels
combined_df['group'] = combined_df['strategy'] + '\n' + combined_df['period'].astype(str)

positions = []
labels_box = []
pos = 0

for strategy in strategies:
    for period in periods:
        labels_box.append(f'{strategy}\nP={int(period)}')
        pos += 1

# Plot
for strategy in strategies:
    for period in periods:
        abm_vals = abm_df[(abm_df['strategy'] == strategy) & (abm_df['period'] == period)]['risk_aversion'].values
        tax_vals = tax_df_renamed[(tax_df_renamed['strategy'] == strategy) & (tax_df_renamed['period'] == period)]['risk_aversion'].values
        
        x_abm = len(positions) * 0.1 + len(positions) - len(strategies) * len(periods)
        positions.append(x_abm)

# Use seaborn for cleaner box plot
box_data = []
for strategy in strategies:
    for period in periods:
        abm_vals = abm_df[(abm_df['strategy'] == strategy) & (abm_df['period'] == period)]['risk_aversion'].values
        tax_vals = tax_df_renamed[(tax_df_renamed['strategy'] == strategy) & (tax_df_renamed['period'] == period)]['risk_aversion'].values
        
        for val in abm_vals:
            box_data.append({'model': 'ABM', 'group': f'{strategy}\nP={int(period)}', 'risk_aversion': val})
        for val in tax_vals:
            box_data.append({'model': 'Tax-Evation', 'group': f'{strategy}\nP={int(period)}', 'risk_aversion': val})

box_df = pd.DataFrame(box_data)
sns.boxplot(data=box_df, x='group', y='risk_aversion', hue='model', ax=ax, palette=['#1f77b4', '#d62728'])

ax.set_xlabel('Strategy × Period', fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Risk Aversion', fontsize=12, fontweight='bold')
ax.set_title('Distribution of Risk Aversion by Model\n(with 3 repetitions each)', 
             fontsize=13, fontweight='bold', pad=20)
ax.legend(title='Model', fontsize=10, title_fontsize=11)
ax.grid(True, alpha=0.3, axis='y')

plt.xticks(rotation=0, fontsize=9)
plt.tight_layout()
plt.savefig(BASE / 'comparison_boxplot.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# SAVE SUMMARY TABLES
# ============================================================================

summary_comparison = pd.concat([
    abm_summary[['strategy', 'period', 'mean', 'std']].assign(model='ABM_Original'),
    tax_summary[['strategy', 'period', 'mean', 'std']].assign(model='Tax-Evation')
], ignore_index=True)

summary_comparison.to_csv(BASE / 'summary_comparison.csv', index=False)

# Calculate absolute differences
diff_summary = []
for strategy in strategies:
    for period in periods:
        abm_val = abm_summary[(abm_summary['strategy'] == strategy) & (abm_summary['period'] == period)]['mean'].values
        tax_val = tax_summary[(tax_summary['strategy'] == strategy) & (tax_summary['period'] == period)]['mean'].values
        
        if len(abm_val) > 0 and len(tax_val) > 0:
            abs_diff = tax_val[0] - abm_val[0]
            pct_diff = (abs_diff / abm_val[0] * 100) if abm_val[0] != 0 else 0
            
            diff_summary.append({
                'Strategy': strategy,
                'Period': int(period),
                'ABM_Mean': abm_val[0],
                'TaxEvation_Mean': tax_val[0],
                'Absolute_Difference': abs_diff,
                'Percent_Difference': pct_diff
            })

diff_df_summary = pd.DataFrame(diff_summary)
diff_df_summary.to_csv(BASE / 'difference_summary.csv', index=False)

print("\n✓ All comparison plots generated successfully!")
print("✓ summary_comparison.csv")
print("✓ difference_summary.csv")
print("\nDifference Summary:")
print(diff_df_summary.to_string(index=False))
