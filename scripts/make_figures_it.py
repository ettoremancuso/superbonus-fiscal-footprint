"""Rigenera le figure del paper sul Superbonus con etichette in italiano.
I dati sono quelli del notebook originale (superbonus_analysis.ipynb), ricopiati dagli output."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

FIG = Path(__file__).resolve().parent.parent / "figures_it"
FIG.mkdir(exist_ok=True)

BLUE, ORANGE, GREY, LIGHT, INK = "#2a78d6", "#eb6834", "#8c8b86", "#d9d8d3", "#2b2b2b"
plt.rcParams.update({
    "font.family": "serif", "font.serif": ["Liberation Serif", "Times New Roman", "DejaVu Serif"],
    "font.size": 9.5, "axes.titlesize": 10.5, "axes.titleweight": "bold",
    "axes.edgecolor": GREY, "axes.linewidth": 0.6, "axes.labelcolor": INK,
    "xtick.color": INK, "ytick.color": INK, "axes.grid": True,
    "grid.color": "#ebeae6", "grid.linewidth": 0.6, "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False,
    "legend.frameon": False, "figure.dpi": 150, "savefig.dpi": 400, "savefig.bbox": "tight",
    "axes.formatter.use_locale": False, "pdf.fonttype": 42,
})


def it(x, dec=1):
    """Numero in formato italiano (virgola decimale, punto per le migliaia)."""
    s = f"{x:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def save(fig, name):
    from matplotlib.ticker import ScalarFormatter, FuncFormatter
    f = FuncFormatter(lambda v, p: f"{v:g}".replace(".", ","))
    for ax in fig.axes:
        for axis in (ax.xaxis, ax.yaxis):
            if isinstance(axis.get_major_formatter(), ScalarFormatter):
                axis.set_major_formatter(f)
    fig.savefig(FIG / f"{name}.pdf")
    plt.close(fig)


# --- Dati (dal notebook) ---
takeup = pd.DataFrame({
    "date": pd.to_datetime(["2021-09-30", "2022-07-31", "2023-12-31", "2024-09-30",
                            "2025-02-28", "2025-09-30", "2025-12-31"]),
    "inv": [5.10, 40.00, 104.00, 116.33, 119.99, 122.24, 124.00],
    "measure": ["concluded", "admitted", "total", "deduction", "deduction", "deduction", "deduction"],
})
comp = pd.DataFrame({
    "tipo": ["Condomini", "Edifici unifamiliari", "Unità indipendenti"],
    "cert": [138352, 245184, 117386],
    "inv": [83.0, 27.9, 11.3],
})
deficit = pd.DataFrame({
    "year": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "nb": [1.5, 9.4, 8.9, 8.1, 7.2, 3.4, 3.1],
    "credits": [0.0, 0.0, 1.0, 3.0, 4.0, 0.5, 0.0],
    "first": [np.nan, 9.5, 7.2, 5.6, np.nan, np.nan, np.nan],
})
lit = pd.DataFrame({
    "studio": ["Banca d'Italia", "MEF"],
    "takeup": [170, 186], "deadweight": [45, 70],
})

# --- Figura 1 ---
fig, ax = plt.subplots(figsize=(6.4, 3.1))
main = takeup[takeup.measure != "concluded"]
early = takeup[takeup.measure == "concluded"]
ax.plot(main.date, main.inv, color=BLUE, lw=2, marker="o", ms=5, label="Investimenti certificati")
ax.plot(early.date, early.inv, ls="none", marker="o", ms=6, mfc="white", mec=BLUE, mew=1.5,
        label="Solo lavori conclusi (set. 2021)")
for _, r in takeup.iterrows():
    ax.annotate(it(r.inv, 0), (r.date, r.inv), textcoords="offset points", xytext=(0, 7),
                ha="center", fontsize=8, color=INK)
ax.axvspan(pd.Timestamp("2024-01-01"), pd.Timestamp("2026-01-15"), color=LIGHT, alpha=0.45, lw=0)
ax.text(pd.Timestamp("2024-02-15"), 20, "Stop alla cessione del credito,\naliquota al 70% e poi al 65%",
        fontsize=8, color=INK)
ax.set_ylabel("Miliardi di euro (cumulati)")
ax.set_ylim(0, 140)
ax.xaxis.set_major_locator(mdates.YearLocator()); ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax.set_title("Investimenti Superbonus certificati all'ENEA, valori cumulati")
ax.legend(loc="upper left")
save(fig, "fig1_takeup")

# --- Figura 2 ---
comp["share_cert"] = comp.cert / comp.cert.sum() * 100
comp["share_inv"] = comp.inv / comp.inv.sum() * 100
comp["avg_k"] = comp.inv * 1e6 / comp.cert
fig, ax = plt.subplots(figsize=(6.4, 2.7))
y = np.arange(len(comp))[::-1]
h = 0.36
ax.barh(y + h / 2, comp.share_cert, h, color=GREY, label="Quota delle asseverazioni", edgecolor="white", lw=1)
ax.barh(y - h / 2, comp.share_inv, h, color=BLUE, label="Quota degli investimenti", edgecolor="white", lw=1)
for yi, (_, r) in zip(y, comp.iterrows()):
    ax.text(r.share_cert + 1, yi + h / 2, f"{r.share_cert:.0f}%", va="center", fontsize=8)
    ax.text(r.share_inv + 1, yi - h / 2, f"{r.share_inv:.0f}%  (media {it(r.avg_k, 0)} mila euro)",
            va="center", fontsize=8)
ax.set_yticks(y, comp.tipo)
ax.set_xlim(0, 100); ax.set_xlabel("Percentuale del totale (ENEA, 30 settembre 2025)")
ax.set_title("A chi sono andati i soldi: edifici e importi a confronto")
ax.legend(loc="lower right")
ax.grid(axis="y", visible=False)
save(fig, "fig2_composition")

# --- Figura 3 ---
d = deficit.copy()
d["other"] = d.nb - d.credits
fig, ax = plt.subplots(figsize=(6.4, 3.2))
x = d.year.values
ax.bar(x, d.other, 0.62, color=LIGHT, edgecolor="white", lw=2, label="Indebitamento netto esclusi i crediti edilizi")
ax.bar(x, d.credits, 0.62, bottom=d.other, color=BLUE, edgecolor="white", lw=2,
       label="Crediti d'imposta edilizi (per competenza)")
fe = d.dropna(subset=["first"])
ax.plot(fe.year, fe["first"], ls="none", marker="D", ms=6, color=ORANGE, mec="white", mew=1,
        label="Prima stima pubblicata")
for _, r in d.iterrows():
    top = max(r.nb, r["first"] if pd.notna(r["first"]) else 0)
    ax.text(r.year, top + 0.3, it(r.nb), ha="center", fontsize=8)
ax.axhline(3, color=INK, lw=0.8, ls="--")
ax.text(2018.55, 3.15, "Valore di riferimento 3%", fontsize=8)
ax.set_ylabel("Percentuale del PIL"); ax.set_ylim(0, 11)
ax.set_xticks(x)
ax.set_title("Indebitamento netto delle PA e componente dei crediti edilizi")
ax.legend(loc="upper right", fontsize=8)
ax.grid(axis="x", visible=False)
save(fig, "fig3_deficit")


# --- Figura 4 ---
def cash_profile(accruals, instalments, start_lag=1, horizon=(2021, 2034)):
    years = np.arange(horizon[0], horizon[1] + 1)
    cash = pd.Series(0.0, index=years)
    for t, a in accruals.items():
        n = instalments[t]
        for k in range(n):
            s = t + start_lag + k
            if s in cash.index:
                cash[s] += a / n
    return cash


acc = {t: v for t, v in zip(d.year, d.credits) if v > 0}
base_n = {2021: 5, 2022: 4, 2023: 4, 2024: 10}
cash = cash_profile(acc, base_n)
accr = pd.Series(acc).reindex(cash.index, fill_value=0)
fig, ax = plt.subplots(figsize=(6.4, 3.1))
ax.bar(cash.index, accr, 0.62, color=LIGHT, edgecolor="white", lw=2,
       label="Contabilizzati nel deficit (crediti \"pagabili\", Eurostat)")
ax.plot(cash.index, cash, color=BLUE, lw=2, marker="o", ms=4.5,
        label="Compensazioni di cassa (pesano su fabbisogno e debito)")
ax.set_ylabel("Percentuale del PIL"); ax.set_xticks(cash.index[::2])
ax.set_title("Stesso costo, tempi diversi: deficit e cassa a confronto")
ax.legend(loc="upper right", fontsize=8)
ax.grid(axis="x", visible=False)
save(fig, "fig4_cash_sim")
assert round(cash.loc[2025:2027].sum(), 2) == 5.05

# --- Figura 5 ---
lit["d"] = lit.deadweight / lit.takeup
tau, s = 0.427, 1.0
dd = np.linspace(0, 0.6, 241)
kk = np.linspace(0.6, 3.0, 241)
D, K = np.meshgrid(dd, kk)
M = K * (1 - D) / s
fig, ax = plt.subplots(figsize=(6.4, 3.6))
im = ax.pcolormesh(D * 100, K, M, cmap="Blues", shading="auto", vmin=0, vmax=3, rasterized=True)
cs = ax.contour(D * 100, K, M, levels=[1, 1 / tau], colors=[INK, ORANGE], linewidths=[1.2, 1.4],
                linestyles=["--", "-"])
ax.clabel(cs, fmt={1: "m = 1 (pareggio)", 1 / tau: "m = 2,34 (autofinanziamento)"}, fontsize=7.5)
for _, r in lit.iterrows():
    ax.axvline(r.d * 100, color=INK, lw=0.7, ls=":")
    ax.text(r.d * 100 + 0.8, 0.68, r.studio, rotation=90, fontsize=7.5, va="bottom")
cb = fig.colorbar(im, ax=ax, pad=0.02); cb.set_label("Moltiplicatore implicito m", fontsize=8.5)
ax.set_xlabel("Quota di deadweight d (%)"); ax.set_ylabel("Effetto sul PIL della spesa aggiuntiva k")
ax.set_title("Moltiplicatore implicito della spesa pubblica, m = k(1 − d)/s")
ax.grid(False)
save(fig, "fig5_multiplier")

# --- Figura 6 ---
total, sb = 13.0, 7.0
fig, ax = plt.subplots(figsize=(6.4, 1.9))
ax.barh([0], [sb], color=BLUE, edgecolor="white", lw=2, label="Attribuiti al Superbonus")
ax.barh([0], [total - sb], left=[sb], color=LIGHT, edgecolor="white", lw=2, label="Energia, materiali e altro")
ax.text(sb / 2, 0, f"~{sb:.0f} p.p.", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
ax.text(sb + (total - sb) / 2, 0, f"~{total - sb:.0f} p.p.", ha="center", va="center", fontsize=9)
ax.set_yticks([]); ax.set_xlim(0, 14)
ax.set_xlabel("Crescita cumulata dell'indice dei costi di costruzione, set. 2021 – dic. 2023 (p.p.)")
ax.set_title("Scomposizione della crescita dei costi di costruzione")
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.42), ncol=2, fontsize=8)
ax.grid(False)
save(fig, "fig6_costs")
print("ok")
