"""Compara PhaseTransition (libros congelados) vs FixBooks (libros vivos), N=10 c/u.

Uso: venv/bin/python Resultados_experimentos/Exp_fixbooks/compare_fixbooks.py
Lee phase_transition_50k_N10.csv y fixbooks_50k_N10.csv. Escribe overlay PNGs +
tabla de deltas. Chequeos pre-registrados:
  (a) en FIXBOOKS, det_rate debe escalar con evasión (r(det, 1-PIR) alto);
      en CHANGES debe ser ~plana (lotería contable);
  (b) strategic PF5 0.02: ¿persiste la indeterminación o cambia de nivel/forma?
"""
import csv
import pandas as pd
import matplotlib.pyplot as plt
import os

BASE = os.path.dirname(os.path.abspath(__file__))
OLD = '/home/mts/Proyectos/Tesis/tesis/Resultados_experimentos/Exp_phase_transition/phase_transition_50k_N10.csv'
NEW = os.path.join(BASE, 'fixbooks_50k_N10.csv')
PIR = 'mean [pct-income-report] of tax-payers'


def load(path, tag):
    rows = list(csv.reader(open(path)))
    df = pd.DataFrame(rows[7:], columns=rows[6])
    df[PIR] = df[PIR].astype(float)
    df['det'] = df['acum_frauds_detected'].astype(float) / 25000
    df['rate'] = df['actual-audit-rate'].astype(float)
    df['pf'] = df['period-frauds'].astype(int)
    df['strat'] = df['tax-payer-audit-selection']
    df['modelo'] = tag
    return df


old = load(OLD, 'congelados')
new = load(NEW, 'vivos')
assert len(old) == 160 and len(new) == 160, (len(old), len(new))
print(f"filas: old={len(old)} new={len(new)}")

# ---- chequeo (a): det vs evasión por modelo ----
print("\n=== r(det_rate, 1-PIR) por modelo [pre-registrado] ===")
for tag, df in [('congelados', old), ('vivos', new)]:
    r = df['det'].corr(1 - df[PIR])
    print(f"{tag}: r={r:+.3f} (vivos debe ser alto; congelados ~plano)")

# ---- tabla de deltas por celda ----
g_old = old.groupby(['strat', 'pf', 'rate'])[PIR].agg(['mean', 'std'])
g_new = new.groupby(['strat', 'pf', 'rate'])[PIR].agg(['mean', 'std'])
comp = pd.DataFrame({'old_mean': g_old['mean'], 'old_std': g_old['std'],
                     'new_mean': g_new['mean'], 'new_std': g_new['std']})
comp['delta'] = comp['new_mean'] - comp['old_mean']
print("\n=== PIR por celda: congelados vs vivos ===")
print(comp.round(3).to_string())
comp.round(4).to_csv(os.path.join(BASE, 'summary_old_vs_new_pir.csv'))

# ---- FIG 1: overlay PIR vs audit-rate, faceted PF x modelo ----
fig, axes = plt.subplots(2, 2, figsize=(15, 10), sharex=True, sharey=True)
for row, pf in enumerate([1, 5]):
    for col, (tag, df) in enumerate([('congelados', old), ('vivos', new)]):
        ax = axes[row, col]
        for s, co in [('random', '#1f77b4'), ('strategic', '#2ca02c')]:
            d = df[(df.strat == s) & (df.pf == pf)].groupby('rate')[PIR].agg(['mean', 'std'])
            ax.plot(d.index, d['mean'], marker='o', linewidth=2.2, label=s, color=co)
            ax.fill_between(d.index, d['mean'] - d['std'], d['mean'] + d['std'], alpha=0.2, color=co)
        ax.set_title(f'{"Congelados (original)" if tag == "congelados" else "Vivos (fix)"} · PF{pf}',
                     fontsize=12, fontweight='bold')
        ax.set_xticks(sorted(df['rate'].unique()))
        ax.set_ylim(-0.05, 1.05)
        ax.grid(True, alpha=0.3)
        if row == 1:
            ax.set_xlabel('Audit rate', fontsize=11, fontweight='bold')
        if col == 0:
            ax.set_ylabel('PIR final', fontsize=11, fontweight='bold')
        ax.legend(fontsize=9)
plt.suptitle('Mismo experimento, otro modelo contable: ¿replican los patrones? (N=10 c/u)',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'compare_PIR_overlay.png'), dpi=200, bbox_inches='tight')
print("\nSaved: compare_PIR_overlay.png")
plt.close()

# ---- FIG 2: det_rate vs (1-PIR) por modelo (firma conductual) ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharex=True, sharey=True)
for ax, (tag, df) in zip(axes, [('congelados', old), ('vivos', new)]):
    for s, co in [('random', '#1f77b4'), ('strategic', '#2ca02c')]:
        d = df[df.strat == s]
        ax.scatter(1 - d[PIR], d['det'], label=s, color=co, alpha=0.6, s=40)
    r = df['det'].corr(1 - df[PIR])
    ax.set_title(f'{tag}: r={r:+.2f}', fontsize=13, fontweight='bold')
    ax.set_xlabel('Evasión (1 - PIR final)', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(fontsize=10)
axes[0].set_ylabel('Detecciones/tick', fontsize=12, fontweight='bold')
plt.suptitle('Firma conductual: ¿la detección sigue a la evasión real?',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'compare_detection_signature.png'), dpi=200, bbox_inches='tight')
print("Saved: compare_detection_signature.png")
plt.close()

# ---- FIG 3: distribuciones strategic PF5 0.02 y PF1 0.02, viejo vs nuevo ----
fig, axes = plt.subplots(1, 2, figsize=(14, 6), sharey=True)
for ax, pf in zip(axes, [1, 5]):
    vals = []
    for tag, df in [('congelados', old), ('vivos', new)]:
        v = sorted(df[(df.strat == 'strategic') & (df.pf == pf) & (df.rate == 0.02)][PIR].values)
        vals.append(v)
        ax.scatter(v, [tag] * len(v), s=60, alpha=0.8,
                   color='#c45200' if tag == 'congelados' else '#2ca02c')
    ax.set_title(f'strategic PF{pf} @ 0.02: ¿persiste la dispersión?', fontsize=12, fontweight='bold')
    ax.set_xlabel('PIR final por run', fontsize=11, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x')
    ax.set_xlim(-0.05, 1.05)
plt.suptitle('Zona biestable/indeterminada: viejo vs nuevo modelo',
             fontsize=14, fontweight='bold', y=1.0)
plt.tight_layout()
plt.savefig(os.path.join(BASE, 'compare_bistable_zone.png'), dpi=200, bbox_inches='tight')
print("Saved: compare_bistable_zone.png")
plt.close()

print("\nALL DONE")
