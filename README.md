# Paying for the Renovation Boom: the fiscal footprint of Italy's Superbonus 110%

Independent research paper by **Ettore Mancuso** (BSc Economics and Finance, Università degli Studi di Palermo), September 2026.

- **Paper (English):** [`paper/superbonus_paper.pdf`](paper/superbonus_paper.pdf)
- **Paper (Italian):** [`paper/superbonus_paper_it.pdf`](paper/superbonus_paper_it.pdf)
- **Notebook:** [`superbonus_analysis.ipynb`](superbonus_analysis.ipynb)

## What this project does

Between 2020 and 2025 Italy financed the renovation of about half a million buildings through the Superbonus 110%, a tax credit worth more than the cost of the works and, until 2023, freely transferable. The paper puts the public numbers into one sourced dataset and runs four exercises on it:

1. **Take-up.** How certified investment grew, and how it stalled once credits could no longer be transferred.
2. **Deficit.** How much of Italy's net borrowing in 2021–2024 came from the building credits, and how the Eurostat reclassification changed the published figures.
3. **Debt timing.** A small cash-offset simulation that shows why the same cost reaches public debt years after it reaches the deficit.
4. **Break-even multiplier.** Given the deadweight estimated by the Bank of Italy and the Treasury, how large the GDP effect of the scheme would have had to be to break even or to pay for itself.

## Main results

| | |
|---|---|
| Certified investment, end-2025 | EUR 124bn across 502,544 buildings |
| Building credits in the 2023 deficit | about 4 of 7.2 points of GDP |
| Cash cost reaching debt, 2025–2027 | 5.05 points of GDP (model) |
| GDP effect needed to break even | 1.36–1.60 euro per euro of additional works |
| Multiplier needed to pay for itself | above 2.3 |

## Repository structure

```
superbonus-fiscal-footprint/
├── superbonus_analysis.ipynb      # full analysis: every figure, table and number in the paper
├── data/                          # hand-collected inputs, one source per row
│   ├── enea_takeup.csv
│   ├── enea_composition_2025q3.csv
│   ├── deficit.csv
│   └── literature_estimates.csv
├── figures/                       # charts used by the English paper (+ results.json, Table 2)
├── figures_it/                    # same charts with Italian labels
├── scripts/make_figures_it.py     # builds figures_it/
└── paper/                         # LaTeX sources and PDFs (English and Italian)
```

## How to run

```bash
pip install -r requirements.txt
jupyter nbconvert --to notebook --execute --inplace superbonus_analysis.ipynb
python scripts/make_figures_it.py     # optional: Italian figures
```

The papers compile with XeLaTeX (font: TeX Gyre Termes): `cd paper && xelatex superbonus_paper.tex` (twice).

## Data notes

All values are hand-collected from ENEA, Istat, the European Commission and published studies; the `source` column in each file in `data/` says where each number comes from. Some values come from press reports of official releases rather than the original documents; the paper discusses this in its Limitations section.

## Tools and AI use

Python (pandas, NumPy, matplotlib), Jupyter, LaTeX, Git.
I used AI tools while writing the code and the Italian translation. The research question, the analysis and the interpretation of the results are my own.

## License

All rights reserved, © 2026 Ettore Mancuso. You are welcome to read the code and reproduce the results; reuse or redistribution requires my written permission. See [LICENSE](LICENSE).
