"""Cohort table: covariates and outcomes per case (KDIGO creatinine AKI, in-hospital death)."""
import os
import numpy as np
import pandas as pd

D = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def ckd_epi_2021(cr, age, female):
    """eGFR, CKD-EPI 2021 race-free equation (mL/min/1.73 m2)."""
    k = np.where(female, 0.7, 0.9)
    a = np.where(female, -0.241, -0.302)
    r = cr / k
    return (142 * np.minimum(r, 1) ** a * np.maximum(r, 1) ** -1.200
            * 0.9938 ** age * np.where(female, 1.012, 1.0))


def build():
    c = pd.read_csv(os.path.join(D, 'cases.csv.gz'))
    labs = pd.read_csv(os.path.join(D, 'labs.csv.gz'))
    cr = labs[labs.name == 'cr'].merge(c[['caseid', 'anestart', 'aneend']], on='caseid')
    cr = cr[(cr.result > 0) & (cr.result < 30)]

    # baseline: last value within 30 days before induction, else the recorded preop_cr
    pre = cr[(cr.dt < cr.anestart) & (cr.dt >= cr.anestart - 30 * 86400)]
    base = pre.sort_values('dt').groupby('caseid').result.last().rename('cr_base_lab')
    post = cr[cr.dt > cr.aneend]
    rel = post.dt - post.aneend
    p48 = post[rel <= 48 * 3600].groupby('caseid').result.max().rename('cr_max48')
    p7 = post[rel <= 7 * 86400].groupby('caseid').result.max().rename('cr_max7d')
    n7 = post[rel <= 7 * 86400].groupby('caseid').size().rename('n_cr_post7d')

    df = c.set_index('caseid').join([base, p48, p7, n7])
    df['cr_base'] = df.cr_base_lab.fillna(df.preop_cr)
    b = df.cr_base
    stage = np.zeros(len(df))
    has = df.cr_max7d.notna() & b.notna()
    ratio = df.cr_max7d / b
    s1 = (ratio >= 1.5) | ((df.cr_max48 - b) >= 0.3)
    s2 = ratio >= 2.0
    s3 = (ratio >= 3.0) | ((df.cr_max7d >= 4.0) & s1)
    stage = np.select([s3, s2, s1], [3, 2, 1], 0).astype(float)
    df['aki_stage'] = np.where(has, stage, np.nan)
    df['aki'] = np.where(has, (stage >= 1).astype(float), np.nan)
    df['female'] = (df.sex == 'F').astype(int)
    df['egfr'] = ckd_epi_2021(b, df.age.astype(float), df.female.astype(bool))
    df['ane_dur_h'] = (df.aneend - df.anestart) / 3600
    return df.reset_index()


if __name__ == '__main__':
    df = build()
    df.to_pickle(os.path.join(D, 'cohort_raw.pkl'))
    print(df[['aki', 'aki_stage', 'death_inhosp', 'cr_base', 'egfr']].describe().T)
    print(df.aki_stage.value_counts(dropna=False))
