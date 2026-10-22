"""Trayectorias PIR/PRA/cobertura a tasa 0.02 (40 runs x 50k ticks, N=10 por celda).

Uso: venv/bin/python Resultados_experimentos/Exp_trajectories/plot_trajectories.py
Lee trajectory_50k.csv (321MB), escribe 5 PNG + imprime métricas de divergencia.
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

BASE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(BASE, 'trajectory_50k.csv')
PIR = 'mean [pct-income-report] of tax-payers'
PRA = 'mean [risk-aversion] of tax-payers'
COV = 'count tax-payers with [sum fraud-detect-hist > 0] / count tax-payers'
STEP = '[step]'

print("cargando CSV (solo columnas necesarias)...")
df = pd.read_csv(SRC, skiprows=6,
                 usecols=['[run number]', 'tax-payer-audit-selection',
                          'period-frauds', STEP, PIR, PRA, COV])
df = df.rename(columns={'[run number]': 'run',
                        'tax-payer-audit-selection': 'strat',
                        'period-frauds': 'pf', STEP: 'tick'})
df['pf'] = df['pf'].astype(int)
print(f"filas: {len(df)} (esperado 2000040 = 40 runs x 50001 ticks)")

cells = [('random', 1), ('random', 5), ('strategic', 1), ('strategic', 5)]
colors = {'random': '#1f77b4', 'strategic': '#2ca02c'}

# ---- divergencia: std y rango entre runs por tick y celda ----
print("\n=== divergencia: primer tick con std>0.10 sostenida 500 ticks ===")
div = {}
for s, pf in cells:
    g = df[(df.strat == s) & (df.pf == pf)]
    piv = g.pivot_table(index='tick', columns='run', values=PIR)
    std = piv.std(axis=1)
    rng = piv.max(axis=1) - piv.min(axis=1)
    div[(s, pf)] = (std, rng)
    over = (std > 0.10)
    sustained = over.rolling(500, min_periods=500).apply(lambda w: w.all(), raw=True) > 0
    t = sustained[sustained].index.min() if sustained.any() else None
    print(f"{s:9s} PF{pf}: std_final={std.iloc[-1]:.3f} rango_final={rng.iloc[-1]:.3f} "
          f"std>0.10 desde tick {t}")

# ---- FIG 1: spaghetti PIR por celda (submuestreo c/50) ----
fig, axes = plt.subplots(2, 2, figsize=(15, 9), sharex=True, sharey=True)
for ax, (s, pf) in zip(axes.flat, cells):
    g = df[(df.strat == s) & (df.pf == pf)]
    for r, gd in g.groupby('run'):
        gd = gd.sort_values('tick')
        ax.plot(gd['tick'].values[::50], gd[PIR].values[::50],
                color=colors[s], alpha=0.45, linewidth=1.0)
    m = g.groupby('tick')[PIR].mean()
    ax.plot(m.index.values[::50], m.values[::50], color='black', linewidth=2.2, label='media')
    ax.set_title(f'{s} · PF{pf} (N=10)', fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0, 50000)
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=9)
    if ax in axes[1, :]:
        ax.set_xlabel('tick', fontsize=12, fontweight='bold')
    if ax in axes[:, 0]:
        ax.set_ylabel('PIR medio', fontsize=12, fontweight='bold')
plt.suptitle('Trayectorias PIR a tasa 0.02: 40 runs, 50k ticks (submuestreo c/50)',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'traj_PIR_spaghetti.png'), dpi=200, bbox_inches='tight')
print("\nSaved: traj_PIR_spaghetti.png")
plt.close()

# ---- FIG 2: zoom temprano 0-3000 (resolución completa) ----
fig, axes = plt.subplots(2, 2, figsize=(15, 9), sharex=True, sharey=True)
for ax, (s, pf) in zip(axes.flat, cells):
    g = df[(df.strat == s) & (df.pf == pf) & (df.tick <= 3000)]
    for r, gd in g.groupby('run'):
        gd = gd.sort_values('tick')
        ax.plot(gd['tick'].values, gd[PIR].values, color=colors[s], alpha=0.5, linewidth=1.0)
    ax.set_title(f'{s} · PF{pf}', fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.grid(True, alpha=0.3)
    if ax in axes[1, :]:
        ax.set_xlabel('tick', fontsize=12, fontweight='bold')
    if ax in axes[:, 0]:
        ax.set_ylabel('PIR medio', fontsize=12, fontweight='bold')
plt.suptitle('Primeros 3000 ticks: ¿divergencia temprana o tardía?',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'traj_PIR_early.png'), dpi=200, bbox_inches='tight')
print("Saved: traj_PIR_early.png")
plt.close()

# ---- FIG 3: std(t) por celda (cuándo explota la dispersión) ----
fig, ax = plt.subplots(figsize=(12, 6))
for (s, pf) in cells:
    std, _ = div[(s, pf)]
    ax.plot(std.index.values[::50], std.values[::50], linewidth=2.2,
            label=f'{s} PF{pf} (final {std.iloc[-1]:.2f})',
            color=colors[s], linestyle='-' if pf == 1 else '--')
ax.axhline(0.10, color='gray', linestyle=':', alpha=0.7, label='umbral 0.10')
ax.set_xlabel('tick', fontsize=12, fontweight='bold')
ax.set_ylabel('std entre runs (PIR)', fontsize=12, fontweight='bold')
ax.set_title('Dispersión entre réplicas en el tiempo: ¿cuándo se separan los destinos?',
             fontsize=13, fontweight='bold')
ax.grid(True, alpha=0.3)
ax.legend(fontsize=10)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'traj_std_over_time.png'), dpi=200, bbox_inches='tight')
print("Saved: traj_std_over_time.png")
plt.close()

# ---- FIG 4: spaghetti cobertura ----
fig, axes = plt.subplots(2, 2, figsize=(15, 9), sharex=True, sharey=True)
for ax, (s, pf) in zip(axes.flat, cells):
    g = df[(df.strat == s) & (df.pf == pf)]
    for r, gd in g.groupby('run'):
        gd = gd.sort_values('tick')
        ax.plot(gd['tick'].values[::50], gd[COV].values[::50],
                color=colors[s], alpha=0.45, linewidth=1.0)
    ax.set_title(f'{s} · PF{pf}', fontsize=13, fontweight='bold')
    ax.set_ylim(-0.05, 1.05)
    ax.set_xlim(0, 50000)
    ax.grid(True, alpha=0.3)
    if ax in axes[1, :]:
        ax.set_xlabel('tick', fontsize=12, fontweight='bold')
    if ax in axes[:, 0]:
        ax.set_ylabel('cobertura recordada', fontsize=12, fontweight='bold')
plt.suptitle('Trayectorias de cobertura (detección en últ. PF auditorías) a tasa 0.02',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'traj_coverage_spaghetti.png'), dpi=200, bbox_inches='tight')
print("Saved: traj_coverage_spaghetti.png")
plt.close()

# ---- pendiente final por run (últimos 5k ticks, OLS) ----
print("\n=== pendiente PIR por run en últimos 5k ticks (x1000) ===")
for s, pf in cells:
    g = df[(df.strat == s) & (df.pf == pf) & (df.tick >= 45000)]
    slopes = []
    for r, gd in g.groupby('run'):
        x = gd['tick'].values
        b, _ = np.polyfit(x, gd[PIR].values, 1)
        slopes.append(b * 1000)
    slopes = np.array(slopes)
    print(f"{s:9s} PF{pf}: media {slopes.mean():+.4f}/ktick, "
          f"rango [{slopes.min():+.4f}, {slopes.max():+.4f}] "
          f"({'converge' if np.abs(slopes).max() < 0.005 else 'AÚN SE MUEVE'})")

print("\nALL DONE")
