"""Run pipelines.run_case over all extracted cases; write long tables to out/cache/."""
import glob
import os
import sys
import time
import numpy as np
import pandas as pd
from multiprocessing import Pool

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pipelines import run_case

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
CASES = pd.read_csv(os.path.join(ROOT, 'data', 'cases.csv.gz')).set_index('caseid')
COLS = ['family', 'filter', 'res', 'offset', 'thr', 'minutes', 'auc', 'twa', 'monitored']


def one(f):
    cid = int(os.path.basename(f)[:-4])
    d = dict(np.load(f))
    r = run_case(d, CASES.anestart[cid], CASES.aneend[cid])
    if r is None:
        return cid, None
    rows = pd.DataFrame(r['rows'], columns=COLS)
    rows['caseid'] = cid
    o2 = pd.DataFrame(r['o2'])
    o2['caseid'] = cid
    eps = pd.DataFrame(r['eps'])
    eps['caseid'] = cid
    desc = dict(caseid=cid, p0=r['period'][0], p1=r['period'][1], **r['desc'])
    return cid, (rows, o2, eps, desc)


if __name__ == '__main__':
    files = sorted(glob.glob(os.path.join(ROOT, 'data', 'cases', '*.npz')))
    if len(sys.argv) > 1:
        files = files[:int(sys.argv[1])]
    out = os.path.join(ROOT, 'out', 'cache')
    os.makedirs(out, exist_ok=True)
    t0 = time.time()
    R, O, E, D, none = [], [], [], [], []
    with Pool(int(os.environ.get('NPROC', 12))) as p:
        for cid, res in p.imap_unordered(one, files, chunksize=4):
            if res is None:
                none.append(cid)
                continue
            R.append(res[0]); O.append(res[1]); E.append(res[2]); D.append(res[3])
    pd.concat(R).to_pickle(os.path.join(out, 'exposures.pkl'))
    pd.concat(O).to_pickle(os.path.join(out, 'o2.pkl'))
    pd.concat(E).to_pickle(os.path.join(out, 'episodes.pkl'))
    pd.DataFrame(D).to_pickle(os.path.join(out, 'desc.pkl'))
    pd.Series(none, name='caseid').to_csv(os.path.join(out, 'no_period.csv'), index=False)
    print(f'{len(D)} cases, {len(none)} without a monitoring period, {time.time() - t0:.0f}s')
