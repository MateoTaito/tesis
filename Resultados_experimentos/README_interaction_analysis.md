# Interaction Analysis - Mean Risk Aversion by Strategy and Period Frauds

## Overview
This script analyzes the interaction between audit selection strategies (`tax-payer-audit-selection`) and social memory levels (`period-frauds`) by measuring the mean risk aversion of tax-payers.

## Data Source
- **Input file**: `exp_emu_paper.csv` (NetLogo BehaviorSpace output)
- **Format**: CSV with metadata headers (rows 1-6) and data starting at row 7

## Dependencies
Create and activate the virtual environment:
```bash
cd /home/MTS/UAI/tesis/Resultados_experimentos
source venv/bin/activate  # On Linux/Mac
# or: venv\Scripts\activate  (On Windows)
```

Required packages:
- pandas
- matplotlib
- seaborn
- numpy

Install with:
```bash
pip install pandas matplotlib seaborn numpy
```

## Usage
Run the script from the `Resultados_experimentos` directory:
```bash
source venv/bin/activate
python plot_interaction_analysis.py
```

## Output Files

### 1. **interaction_plot_line.png** (249 KB)
Line plot showing how Mean Risk Aversion changes across different social memory levels (period-frauds) for each audit strategy.
- **Best for**: Visualizing trends and interactions between strategies
- **Interpretation**: Crossing or diverging lines indicate interaction effects

### 2. **interaction_plot_grouped_bars.png** (140 KB)
Grouped bar chart comparing Mean Risk Aversion across strategies for each social memory level.
- **Best for**: Direct comparison of strategy performance at each memory level
- **Interpretation**: Taller bars = higher risk aversion; grouped comparison shows strategy effects

### 3. **interaction_plot_heatmap.png** (163 KB)
Heatmap showing Mean Risk Aversion values color-coded by intensity.
- **Rows**: Audit selection strategies (income-level, random, strategic)
- **Columns**: Period Frauds levels (social memory: 1 or 5)
- **Color scale**: Red = higher risk aversion, Green = lower risk aversion
- **Best for**: Quick visual identification of high/low combinations

### 4. **interaction_plot_faceted.png** (143 KB)
Separate bar charts for each social memory level (period-frauds value).
- **Panels**: One per memory level (1, 5)
- **X-axis**: Audit strategies with value labels on bars
- **Best for**: Examining strategy differences within each memory level

### 5. **summary_mean_risk_aversion.csv** (159 B)
Summary table in CSV format:
```
Period Frauds,1,5
income-level,0.3932,0.3951
random,0.3926,0.3932
strategic,0.3944,0.3921
```

## Key Findings (from current data)

| Strategy | Period Frauds = 1 | Period Frauds = 5 | Change |
|----------|-------------------|-------------------|--------|
| **income-level** | 0.3932 | 0.3951 | +0.0019 ↑ |
| **random** | 0.3926 | 0.3932 | +0.0006 ↑ |
| **strategic** | 0.3944 | 0.3921 | -0.0023 ↓ |

### Observations:
1. **Small effect sizes**: Mean Risk Aversion values are very similar across conditions (~0.393)
2. **Strategic strategy**: Shows a *negative* trend (decreases with higher social memory)
3. **Income-level strategy**: Shows the largest *positive* trend (increases with higher social memory)
4. **Weak interaction**: The three strategies show different trends, suggesting some interaction effect, but the magnitudes are small

## Customization
To modify the script:
1. Edit the `colors` dictionary (line ~39) to change color scheme
2. Modify figure sizes (e.g., `figsize=(10, 6)`) for different dimensions
3. Change `dpi=300` for lower/higher resolution outputs
4. Adjust `cmap='RdYlGn_r'` in heatmap for different color palettes

## Notes
- The script skips the first 6 metadata rows from the NetLogo BehaviorSpace output
- Numeric columns are automatically converted to appropriate data types
- Summary statistics are rounded to 4 decimal places in visualizations
