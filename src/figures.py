"""Figures for the manuscript. Usage: python src/figures.py [descriptive|outcome]"""
import json
import os
import sys
import numpy as np
import pandas as pd
import vitaldb
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from models import ROOT, CACHE
from analysis import descriptive_cohort
from artifact import classify, ARTEFACT, LABELS
from pipelines import best_lag, shift

FIG = os.path.join(ROOT, 'paper', 'figures')
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
BLUE, ORANGE, AQUA, YELLOW = '#2a78d6', '#eb6834', '#1baf7a', '#eda100'
SEQ = ['#cde2fb', '#9ec5f4', '#6da7ec', '#3987e5', '#256abf', '#184f95', '#0d366b']
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 8, 'axes.edgecolor': INK2,
                     'axes.labelcolor': INK, 'xtick.color': INK2, 'ytick.color': INK2,
                     'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.grid': True, 'grid.color': GRID, 'grid.linewidth': 0.5,
                     'savefig.dpi': 300, 'savefig.bbox': 'tight'})


def save(fig, name):
    os.makedirs(FIG, exist_ok=True)
    fig.savefig(os.path.join(FIG, name + '.png'))
    fig.savefig(os.path.join(FIG, name + '.pdf'))
    plt.close(fig)


def fig_examples(c):
    """Figure 1: four flagged low-MAP episodes, waveform vs monitor numerics."""
    e = pd.read_pickle(os.path.join(ROOT, 'out', 'descriptive', 'episodes_labelled.pkl'))
    desc = pd.read_pickle(os.path.join(CACHE, 'desc.pkl')).set_index('caseid')
    want = [(2, 'Transducer open to air / zeroing'), (4, 'Closed stopcock (blood sampling)'),
            (3, 'Fast flush, then recovery'), (4, 'Damped / interrupted trace near cuff inflation')]
    rng = np.random.default_rng(4)
    fig, axs = plt.subplots(4, 1, figsize=(7.2, 7.4))
    used = set()
    for ax, (lab, title) in zip(axs, want):
        g = e[(e.cls == 'flagged') & (e.lab_mode == lab) & (e.dur_s.between(6, 40)) & ~e.caseid.isin(used)]
        if 'cuff' in title:
            g = g[g.nibp_near.notna()]
        if not len(g):
            continue
        r = g.iloc[rng.integers(len(g))]
        used.add(r.caseid)
        p0 = int(desc.loc[r.caseid, 'p0'])
        vf = vitaldb.VitalFile(int(r.caseid), ['SNUADC/ART', 'Solar8000/ART_MBP', 'Solar8000/NIBP_MBP'])
        w = vf.to_numpy(['SNUADC/ART'], 1 / 500)[:, 0]
        d = dict(np.load(os.path.join(ROOT, 'data', 'cases', f'{r.caseid}.npz')))
        lb = classify(d)
        lag = best_lag(d, lb)
        m = shift(d['n_ART_MBP'], lag)
        i0 = p0 + int(r.start)
        a, b = i0 - 20, i0 + int(r.dur_s // 2) + 25
        t = np.arange(a * 1000, b * 1000) / 500 - i0 * 2
        ax.plot(t, w[a * 1000:b * 1000], color=INK2, lw=0.5, label='Arterial waveform (500 Hz)')
        tm = np.arange(a, b) * 2 - i0 * 2
        ax.step(tm, m[a:b], where='post', color=ORANGE, lw=1.6, label='Monitor MAP (2 s, lag-aligned)')
        ax.axhline(65, color=BLUE, lw=1, ls='--')
        art = np.isin(lb[a:b], ARTEFACT) | (lb[a:b] == 6)
        for k in np.flatnonzero(art):
            ax.axvspan(tm[k], tm[k] + 2, color=YELLOW, alpha=0.25, lw=0)
        ax.set_ylim(-20, 320 if lab == 3 else 200)
        ax.set_title(title, loc='left', fontsize=8.5, color=INK)
        ax.set_ylabel('mmHg')
    axs[-1].set_xlabel('Seconds from start of recorded MAP < 65 mmHg')
    axs[0].legend(loc='upper right', frameon=False, fontsize=7)
    fig.text(0.01, 0.005, 'Shaded: windows labelled artefact or guard. Dashed line: 65 mmHg.', color=INK2, fontsize=7)
    fig.tight_layout()
    save(fig, 'fig1_examples')


def fig_o2():
    """Figure 2: spurious and indeterminate share of recorded hypotensive minutes."""
    t = pd.read_csv(os.path.join(ROOT, 'out', 'descriptive', 'o2_spurious.csv'))
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.6), sharey=True)
    names = {'R1': 'R1: every 2 s', 'R2': 'R2: 1 value per min', 'R3': 'R3: 1-min median'}
    for ax, res in zip(axs, ['R1', 'R2', 'R3']):
        g = t[t.res == res].set_index('filter').loc[['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6']]
        x = np.arange(len(g))
        ax.bar(x - 0.2, 100 * g.spurious_frac, 0.38, color=ORANGE, label='Spurious (reference ≥ 65)')
        ax.errorbar(x - 0.2, 100 * g.spurious_frac, yerr=[100 * (g.spurious_frac - g.lo), 100 * (g.hi - g.spurious_frac)],
                    fmt='none', ecolor=INK, lw=0.7, capsize=1.5)
        ax.bar(x + 0.2, 100 * g.indeterminate_frac, 0.38, color=SEQ[1], label='Indeterminate (no reference)')
        ax.set_xticks(x, g.index)
        ax.set_title(names[res], fontsize=8.5, loc='left')
        ax.grid(axis='x', visible=False)
    axs[0].set_ylabel('% of recorded minutes with MAP < 65')
    axs[0].legend(frameon=False, fontsize=7, loc='upper left')
    fig.tight_layout()
    save(fig, 'fig2_spurious')


def fig_o6():
    """Figure 4: probability that a monitor low-MAP episode is waveform-flagged."""
    t = pd.read_csv(os.path.join(ROOT, 'out', 'descriptive', 'o6_probability_table.csv'))
    durs = ['<=10 s', '11-30 s', '31-60 s', '1-2 min', '2-5 min', '>5 min']
    nads = ['<20', '20-39', '40-54', '55-64']
    P = np.full((len(nads), len(durs)), np.nan)
    N = np.zeros_like(P)
    for _, r in t.iterrows():
        if r.duration in durs and r.nadir in nads:
            P[nads.index(r.nadir), durs.index(r.duration)] = r.p_flagged
            N[nads.index(r.nadir), durs.index(r.duration)] = r.episodes
    from matplotlib.colors import LinearSegmentedColormap
    cm = LinearSegmentedColormap.from_list('seq', ['#f4f8fd'] + SEQ)
    fig, ax = plt.subplots(figsize=(5.6, 2.8))
    im = ax.imshow(np.where(N >= 20, P, np.nan), cmap=cm, vmin=0, vmax=1, aspect='auto')
    for i in range(len(nads)):
        for j in range(len(durs)):
            if N[i, j] >= 20:
                ax.text(j, i, f'{100 * P[i, j]:.0f}%\n(n={int(N[i, j])})', ha='center', va='center',
                        fontsize=6.5, color='white' if P[i, j] > 0.55 else INK)
            elif N[i, j] > 0:
                ax.text(j, i, f'n={int(N[i, j])}', ha='center', va='center', fontsize=6, color=INK2)
    ax.set_xticks(range(len(durs)), durs)
    ax.set_yticks(range(len(nads)), [f'{n} mmHg' for n in nads])
    ax.set_xlabel('Episode duration'); ax.set_ylabel('Episode nadir')
    ax.grid(False)
    cb = fig.colorbar(im, ax=ax, fraction=0.04)
    cb.set_label('P(waveform-flagged)')
    fig.tight_layout()
    save(fig, 'fig4_episode_probability')


def fig_nibp(c):
    """Figure 5: artefact fraction around non-invasive cuff readings."""
    desc = pd.read_pickle(os.path.join(CACHE, 'desc.pkl')).set_index('caseid')
    off = np.arange(-60, 16)            # windows (2 s) relative to NIBP value appearing
    num = np.zeros(len(off)); den = np.zeros(len(off))
    for cid in c.index:
        d = dict(np.load(os.path.join(ROOT, 'data', 'cases', f'{cid}.npz')))
        lb = classify(d)
        lag = best_lag(d, lb)
        nb = shift(d['n_NIBP_MBP'], lag)
        p0, p1 = int(desc.loc[cid, 'p0']), int(desc.loc[cid, 'p1'])
        prev = np.concatenate([[np.nan], nb[:-1]])
        ev = np.flatnonzero(np.isfinite(nb) & ~(prev == nb))
        ev = ev[(ev >= p0 + 60) & (ev < p1 - 16)]
        art = np.isin(lb, ARTEFACT).astype(float)
        for j in ev:
            num += art[j + off]
            den += 1
    fig, ax = plt.subplots(figsize=(5.6, 2.4))
    ax.plot(off * 2, 100 * num / den, color=BLUE, lw=2)
    ax.axvline(0, color=INK2, lw=0.8, ls=':')
    ax.set_xlabel('Seconds relative to the moment a new cuff (NIBP) value appears')
    ax.set_ylabel('% of arterial windows\nlabelled artefact')
    ax.text(1, ax.get_ylim()[1] * 0.9, f'{int(den[0])} cuff readings', color=INK2, fontsize=7)
    fig.tight_layout()
    save(fig, 'fig5_nibp_cuff')
    return dict(events=int(den[0]), peak_pct=float(100 * (num / den).max()),
                peak_offset_s=int(off[np.argmax(num / den)] * 2), baseline_pct=float(100 * (num / den)[:10].mean()))


def fig_spec_curve(mode):
    """Figure 3: specification curve of ROR (pipeline vs matched reference)."""
    sc = pd.read_csv(os.path.join(ROOT, 'out', f'results_{mode}', 'spec_curve.csv'))
    fr = pd.read_csv(os.path.join(ROOT, 'out', f'results_{mode}', 'ror_binary_FxR.csv'))
    p = sc[sc.family == 'pipe'].sort_values('ror').reset_index(drop=True)
    fig = plt.figure(figsize=(7.2, 6.4))
    gs = fig.add_gridspec(2, 1, height_ratios=[1.5, 1.6], hspace=0.08)
    ax = fig.add_subplot(gs[0])
    col = {'binary': BLUE, 'minutes': ORANGE, 'auc': AQUA, 'twa': YELLOW}
    for m, g in p.groupby('metric'):
        ax.scatter(g.index, g.ror, s=7, color=col[m], label=m, lw=0)
    ax.axhline(1, color=INK2, lw=0.8)
    ax.axhspan(0.8, 1.25, color=GRID, alpha=0.6, lw=0)
    ax.set_yscale('log')
    ax.set_ylabel('Ratio of odds ratios\n(pipeline / matched reference)')
    ax.legend(frameon=False, ncol=4, fontsize=7, loc='upper left', title='Exposure metric', title_fontsize=7)
    ax.set_xticks([])
    ax2 = fig.add_subplot(gs[1], sharex=ax)
    rows = [('filter', f) for f in ['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6']] + \
           [('res', r) for r in ['R1', 'R2', 'R3', 'R4', 'R5']] + [('thr', t) for t in [55, 60, 65]]
    for k, (fld, val) in enumerate(rows):
        idx = p.index[p[fld] == val]
        ax2.scatter(idx, np.full(len(idx), k), s=2, color=INK, marker='|', lw=0.6)
    ax2.set_yticks(range(len(rows)), [f'{v}' if fld != 'thr' else f'MAP<{v}' for fld, v in rows])
    ax2.invert_yaxis()
    ax2.set_xlabel(f'{len(p)} pipeline specifications, sorted by ratio of odds ratios')
    ax2.grid(False)
    save(fig, 'fig3_spec_curve')


def fig_forest(mode):
    """Figure 6: ROR for all 35 filter x resolution cells, calibrated 95% CI and simultaneous band."""
    fr = pd.read_csv(os.path.join(ROOT, 'out', f'results_{mode}', 'ror_binary_FxR.csv'))
    rname = {'R1': '2-s', 'R2': '1/min', 'R3': '1-min median', 'R4': '5-min chart', 'R5': '15-min chart'}
    fig, axes = plt.subplots(1, 5, figsize=(7.2, 3.4), sharey=True)
    for ax, r in zip(axes, ['R1', 'R2', 'R3', 'R4', 'R5']):
        g = fr[fr.res == r].reset_index(drop=True)
        yv = np.arange(len(g))[::-1]
        ax.axvspan(0.8, 1.25, color=GRID, alpha=0.6, lw=0)
        ax.axvline(1, color=INK2, lw=0.8)
        ax.hlines(yv, g.ror_simlo, g.ror_simhi, color=BLUE, alpha=0.35, lw=4)
        ax.hlines(yv, g.ror_lo, g.ror_hi, color=BLUE, lw=1.4)
        ax.scatter(g.ror, yv, s=16, color=BLUE, zorder=3, edgecolor='white', lw=0.6)
        ax.set_xscale('log')
        ax.set_xlim(0.4, 2.5)
        ax.set_xticks([0.5, 1, 2], ['0.5', '1', '2'])
        ax.minorticks_off()
        ax.set_title(rname[r], fontsize=8)
        ax.grid(axis='y', visible=False)
    axes[0].set_yticks(np.arange(7)[::-1], ['F0', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6'])
    fig.subplots_adjust(bottom=0.22, wspace=0.12)
    fig.supxlabel('Ratio of odds ratios for AKI (pipeline / reference at the same resolution)', fontsize=8, y=0.08)
    fig.text(0.01, 0.01, 'Thin line: 95% CI; wide band: simultaneous 95% band over 35 cells; '
             'grey: equivalence margin 0.80–1.25.', fontsize=6.5, color=INK2)
    save(fig, 'fig6_forest')


if __name__ == '__main__':
    what = sys.argv[1] if len(sys.argv) > 1 else 'descriptive'
    if what == 'descriptive':
        c = descriptive_cohort()
        fig_o2()
        fig_o6()
        info = fig_nibp(c)
        json.dump(info, open(os.path.join(ROOT, 'out', 'descriptive', 'nibp_profile.json'), 'w'))
        print(info)
        fig_examples(c)
    else:
        fig_spec_curve(what)
        fig_forest(what)
