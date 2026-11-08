"""Supplementary AES items cited in the essay.

Usage: python aes_extra_items.py <aes1998.dta> <aes2025.dta>

1. 2025: "Immigrants increase the cost of housing" (F8_5), % agree or strongly agree,
   by House first-preference vote. Weighted by 'weight'.
2. 1998: whether "people" would mind an Asian boss (G12ASIAN) or an Asian relative
   by marriage (G13ASIAN), % "mind a lot", and perceived prejudice against Asians
   (G8, % "a lot"), by House vote. Unweighted (no weight in the 1998 file).
"""
import sys
import pyreadstat

f98, f25 = sys.argv[1:3]
a, _ = pyreadstat.read_dta(f98)
b, _ = pyreadstat.read_dta(f25)

p25 = {1: "Liberal", 2: "Labor", 3: "National", 4: "Greens", 11: "One Nation"}
b["party"] = b.B9_1_r.map(p25)
d = b[b.F8_5.between(1, 5)]
print("2025: immigrants increase the cost of housing, % agree (weighted)")
for p in ["One Nation", "Liberal", "National", "Labor", "Greens"]:
    s = d[d.party == p]
    print(f"  {p:<11} {100 * s.weight[s.F8_5 <= 2].sum() / s.weight.sum():5.1f}  (n={len(s)})")
print(f"  {'All':<11} {100 * d.weight[d.F8_5 <= 2].sum() / d.weight.sum():5.1f}  (n={len(d)})")

p98 = {1: "Liberal", 2: "Labor", 6: "One Nation"}
a["party"] = a.B11REPS.map(p98)
print("\n1998 perception items, % 'a lot' (unweighted)")
for v, label in [("G12ASIAN", "people would mind an Asian boss a lot"),
                 ("G13ASIAN", "people would mind an Asian relative by marriage a lot"),
                 ("G8", "a lot of prejudice against Asians")]:
    d = a[a[v] > 0]
    row = {p: float(round(100 * (d[d.party == p][v] == 1).mean(), 1)) for p in ["One Nation", "Liberal", "Labor"]}
    row["All"] = float(round(100 * (d[v] == 1).mean(), 1))
    print(f"  {label}: {row}")
