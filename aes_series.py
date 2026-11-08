"""AES 1998-2025 series: support for reducing immigration, by birthplace and party.

Usage: python aes_series.py <aes1998.dta> <aes2010.dta> <aes2019.dta> <aes2022.dta> <aes2025.dta> <out.csv>

Question (all years): "Do you think the number of immigrants allowed into Australia
nowadays should be reduced or increased?" 1 increased a lot ... 5 reduced a lot.
"Reduce" = reduced a little + reduced a lot. Weights: 1998 none (unweighted);
2010 weight2; 2019 wt_pooled; 2022 weight; 2025 weight.
"""
import sys
import numpy as np
import pandas as pd
import pyreadstat

f98, f10, f19, f22, f25, out = sys.argv[1:7]


def load(path):
    df, _ = pyreadstat.read_dta(path)
    return df


y = {}
d = load(f98)
d["w"] = 1.0
d["att"] = d.F6
d["party"] = d.B11REPS.map({1: "Liberal", 2: "Labor", 3: "National", 5: "Greens", 6: "One Nation"})
d["born"] = np.select([d.I3OWN == 1, d.I3OWN > 1], ["Australia", "Overseas"], None)
y["1998"] = d

d = load(f10)
d["w"] = d.weight2
d["att"] = d.f9
d["party"] = d.xb9reps.map({18: "Liberal", 5: "Labor", 20: "National", 3: "Greens", 27: "One Nation"})
d["born"] = np.select([d.h3own == 1, d.h3own > 1], ["Australia", "Overseas"], None)
y["2010"] = d

d = load(f19)
d["w"] = d.wt_pooled
d["att"] = d.F7
d["party"] = d.B9_1.map({1: "Liberal", 2: "Labor", 3: "National", 4: "Greens", 11: "One Nation"})
d["born"] = np.select([d.H3_1.isin([1100, 1101]), d.H3_1.between(1000, 9999)], ["Australia", "Overseas"], None)
y["2019"] = d

d = load(f22)
d["w"] = d.weight
d["att"] = d.F7
d["party"] = d.B9_1.map({1: "Liberal", 2: "Labor", 3: "National", 4: "Greens", 11: "One Nation"})
d["born"] = np.select([d.H3_1.isin([1100, 1101]), d.H3_1.between(1000, 9999)], ["Australia", "Overseas"], None)
y["2022"] = d

d = load(f25)
d["w"] = d.weight
d["att"] = d.F7
d["party"] = d.B9_1_r.map({1: "Liberal", 2: "Labor", 3: "National", 4: "Greens", 11: "One Nation"})
d["born"] = np.select([d.H3_1_r == 0, d.H3_1_r.between(1, 918)], ["Australia", "Overseas"], None)
y["2025"] = d


def row(year, label, s):
    s = s[s.att.between(1, 5)]
    n = len(s)
    if n == 0:
        return None
    W = s.w.sum()
    red = s.w[s.att >= 4].sum() / W * 100
    lot = s.w[s.att == 5].sum() / W * 100
    moe = 1.96 * np.sqrt(red / 100 * (1 - red / 100) / n) * 100
    return dict(year=year, group=label, n=n, reduce=round(red, 1), reduce_a_lot=round(lot, 1), moe_reduce=round(moe, 1))


rows = []
for yr, d in y.items():
    rows.append(row(yr, "All", d))
    for g in ["Australia", "Overseas"]:
        rows.append(row(yr, "Born " + g, d[d.born == g]))
    for p in ["One Nation", "Liberal", "National", "Labor", "Greens"]:
        rows.append(row(yr, p, d[d.party == p]))
res = pd.DataFrame([r for r in rows if r])
res.to_csv(out, index=False)
wide = res.pivot(index="group", columns="year", values="reduce")
ns = res.pivot(index="group", columns="year", values="n")
print("Reduce immigration, % (n in brackets)")
print(wide.astype(str).where(wide.isna(), wide.astype(str) + " (" + ns.astype("Int64").astype(str) + ")").to_string())
