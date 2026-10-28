"""Confirmatorio N=30: tests de biestabilidad (dip, mixtura, Levene, logística).

Uso: venv/bin/python Resultados_experimentos/Exp_confirmacion/analyze_confirmacion.py
Lee confirmacion_50k_N30.csv (600 filas). Decisiones pre-registradas en Notas/05.
"""
import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from diptest import diptest
from scipy.stats import levene
from sklearn.mixture import GaussianMixture
from sklearn.linear_model import LogisticRegression

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'confirmacion_50k_N30.csv')
PIR = 'mean [pct-income-report] of tax-payers'

rows = list(csv.reader(open(SRC)))
df = pd.DataFrame(rows[7:], columns=rows[6])
assert len(df) == 600, f"filas={len(df)}, esperado 600"
df[PIR] = df[PIR].astype(float)
df['rate'] = df['actual-audit-rate'].astype(float)
df['pf'] = df['period-frauds'].astype(int)
df['strat'] = df['tax-payer-audit-selection']
df['techo'] = (df[PIR] >= 0.9).astype(int)

print("=" * 70)
print("CONFIRMATORIO N=30: 20 celdas x 30 runs")
print("=" * 70)

# ---- 1. Dip test por celda (Holm sobre strategic PF5 x5) ----
print("\n--- dip test (H0: unimodal) ---")
res = []
for (s, pf, r), g in sorted(df.groupby(['strat', 'pf', 'rate']),
                            key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
    v = g[PIR].values
    dip, p = diptest(v)
    res.append((s, pf, r, dip, p, v.mean(), v.std(ddof=1)))
    print(f"{s:9s} PF{pf} {r}: dip={dip:.4f} p={p:.4f} "
          f"mean={v.mean():.3f} std={v.std(ddof=1):.3f}")
ps = [(s, pf, r, p) for (s, pf, r, d, p, m, sd) in res if s == 'strategic' and pf == 5]
order = sorted(range(len(ps)), key=lambda i: ps[i][3])
print("\nHolm (strategic PF5, m=5):")
m = len(ps)
for rank, i in enumerate(order):
    s, pf, r, p = ps[i]
    print(f"  rate {r}: p={p:.4f} vs alfa/{m - rank}={0.05 / (m - rank):.4f} "
          f"{'RECHAZA unimodalidad' if p < 0.05 / (m - rank) else 'no rechaza'}")

# ---- 2. Mixtura 1 vs 2 componentes (BIC) ----
print("\n--- GMM 1 vs 2 comp (BIC menor gana) ---")
for s, pf, r in [('strategic', 5, 0.02), ('strategic', 5, 0.03),
                 ('strategic', 1, 0.02), ('random', 1, 0.02)]:
    v = df[(df.strat == s) & (df.pf == pf) & (df.rate == r)][PIR].values.reshape(-1, 1)
    b1 = GaussianMixture(1, random_state=0).fit(v).bic(v)
    g2 = GaussianMixture(2, random_state=0).fit(v)
    print(f"{s:9s} PF{pf} {r}: BIC1={b1:.1f} BIC2={g2.bic(v):.1f} "
          f"medias={sorted(g2.means_.flatten().round(3))} -> "
          f"{'2 CUENCAS' if g2.bic(v) < b1 else '1 cuenca'}")

# ---- 3. Levene strategic-PF5 vs controles (por tasa) ----
print("\n--- Levene varianzas (strategic PF5 vs cada control) ---")
for r in sorted(df.rate.unique()):
    a = df[(df.strat == 'strategic') & (df.pf == 5) & (df.rate == r)][PIR].values
    for s2, pf2 in [('strategic', 1), ('random', 1), ('random', 5)]:
        b = df[(df.strat == s2) & (df.pf == pf2) & (df.rate == r)][PIR].values
        _, p = levene(a, b)
        print(f"rate {r}: stratPF5 vs {s2}PF{pf2}: p={p:.4f} "
              f"(sd {a.std(ddof=1):.3f} vs {b.std(ddof=1):.3f})")

# ---- 4. Destino ~ PIAR_10000 (logística por celda strategic) ----
print("\n--- logística techo ~ PIAR_10000 (strategic) ---")
for pf in [1, 5]:
    for r in sorted(df.rate.unique()):
        g = df[(df.strat == 'strategic') & (df.pf == pf) & (df.rate == r)]
        if g['techo'].nunique() < 2:
            print(f"strategic PF{pf} {r}: sin variación (todos techo={g['techo'].iloc[0]})")
            continue
        X = g[['PIAR_10000']].values.astype(float)
        m = LogisticRegression().fit(X, g['techo'].values)
        print(f"strategic PF{pf} {r}: coef={m.coef_[0][0]:+.2f} "
              f"acc_train={m.score(X, g['techo'].values):.2f}")

# ---- FIG 1: distribuciones por run (stripplot por tasa, facetas PF x estrategia) ----
fig, axes = plt.subplots(2, 2, figsize=(15, 9), sharey=True)
for ax, (s, pf) in zip(axes.flat, [('random', 1), ('random', 5),
                                   ('strategic', 1), ('strategic', 5)]):
    import seaborn as sns
    d = df[(df.strat == s) & (df.pf == pf)]
    sns.stripplot(data=d, x='rate', y=PIR, ax=ax, size=6, alpha=0.8,
                  color='#1f77b4' if s == 'random' else '#2ca02c', jitter=0.15)
    ax.axhline(0.9, color='red', linestyle='--', alpha=0.6)
    ax.set_title(f'{s} · PF{pf} (N=30/celda)', fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3, axis='y')
    if ax in axes[1, :]:
        ax.set_xlabel('Audit rate', fontsize=12, fontweight='bold')
    if ax in axes[:, 0]:
        ax.set_ylabel('PIR final', fontsize=12, fontweight='bold')
plt.suptitle('Confirmatorio N=30: distribución por run (1 punto = 1 run)',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'confirm_distributions.png'), dpi=200, bbox_inches='tight')
print("\nSaved: confirm_distributions.png")
plt.close()

# ---- FIG 2: tasa en techo por tasa (con IC95 Wilson) ----
from math import sqrt
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
for ax, pf in zip(axes, [1, 5]):
    for s, co in [('random', '#1f77b4'), ('strategic', '#2ca02c')]:
        rs, ps, lo, hi = [], [], [], []
        for r in sorted(df.rate.unique()):
            v = df[(df.strat == s) & (df.pf == pf) & (df.rate == r)][PIR].values
            n, k = len(v), int((v >= 0.9).sum())
            z = 1.96
            denom = 1 + z * z / n
            c = (k / n + z * z / (2 * n)) / denom
            h = z * sqrt(k * (n - k) / n ** 3 + z * z / (4 * n ** 2)) / denom
            rs.append(r)
            ps.append(k / n)
            lo.append(max(0, c - h))
            hi.append(min(1, c + h))
        ax.plot(rs, ps, marker='o', linewidth=2.5, label=s, color=co)
        ax.fill_between(rs, lo, hi, alpha=0.2, color=co)
    ax.set_title(f'PF{pf}: P(PIR≥0.9) vs tasa (N=30, IC95 Wilson)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Audit rate', fontsize=11, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
axes[0].set_ylabel('Fracción en techo', fontsize=12, fontweight='bold')
plt.suptitle('Curva de "probabilidad de techo": ¿dónde está el umbral? (N=30)',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'confirm_techo_curve.png'), dpi=200, bbox_inches='tight')
print("Saved: confirm_techo_curve.png")
plt.close()

print("\nALL DONE")
