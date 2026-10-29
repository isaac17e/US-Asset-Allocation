# US Asset Allocation

Python tools that build US investment portfolios from live market data. Two independent pipelines share a few support modules. Each one runs end to end, prints tables to the console, writes an interactive Plotly HTML report and exports a JSON file.

> Code comments, console output and HTML reports are in Spanish.

| File | Role |
|---|---|
| [`US Asset Manager.py`](US%20Asset%20Manager.py) | **ETF allocation**: universe → factors → risk/return estimates → optimal weights. |
| [`Corp_FR_Optimization.py`](Corp_FR_Optimization.py) | **IG corporate bonds (USD)**: issuer screening, ranking and minimum required yield by tenor. |
| [`risk_estimators.py`](risk_estimators.py) | Covariance (EWMA + Ledoit-Wolf), Q→P correction, portfolio moments, Cornish-Fisher. |
| [`bs_pricing.py`](bs_pricing.py) | Black-Scholes and Bjerksund-Stensland (American) option pricing. |
| [`price_cache.py`](price_cache.py) | Per-ticker price cache with incremental download; Yahoo Finance prices (FMP only as fallback). |
| [`fmp_client.py`](fmp_client.py) | Shared FMP HTTP client (throttling, retries, cache, plan-error detection). |
| [`pipeline_io.py`](pipeline_io.py) | Env/CLI parameter resolution and the JSON output contract. |
| [`report_pdf.py`](report_pdf.py) | Optional HTML → PDF export. |

## Quick start

```bash
pip install -r requirements.txt -c constraints.txt   # Python 3.10+

# .env next to the scripts (git-ignored)
#   FMP_API_KEY=...       required (both scripts)
#   FRED_API_KEY=...      required (Corp_FR_Optimization.py)
#   POLYGON_API_KEY=...   optional: option chains; without it, historical moments are used

python "US Asset Manager.py" --risk-profile moderado   # → portfolio_dashboard.html
python Corp_FR_Optimization.py                         # → reporte_portafolio_renta_fija.html
```

Parameters (profile, solver, thresholds, weights) live in the configuration block at the top of each script. Some FMP endpoints depend on your plan; if one is unavailable the script disables it and uses neutral or fallback values.

## 1. ETF allocation (`US Asset Manager.py`)

Orchestrated by `PassiveETFAllocationPipeline`:

1. **Universe**: ~50 core ETFs plus FMP screener candidates (liquidity filter, no leveraged/inverse). Near-duplicates (correlation ≥ 0.985) are removed.
2. **Factors (matrix B)**: Value, Growth, Momentum and Quality scores in [0, 1], from top-holdings fundamentals or, if the plan lacks `etf/holdings`, a returns-based style regression.
3. **Risk and return**:
   - Implied volatility, skewness and kurtosis from option chains (Bakshi-Kapadia-Madan), scaled to a common horizon (default 60 days).
   - Covariance Σ = D·R·D: implied vols adjusted from Q to P measure, EWMA correlation with Ledoit-Wolf shrinkage.
   - Expected return: 75% CAPM + 25% historical mean.
4. **Optimization**: maximize `μᵀw − ½λwᵀΣw` subject to full investment, a weight cap, minimum factor targets and a portfolio-beta band vs. SPY. An optional tail penalty (Cornish-Fisher expected shortfall) discourages fat tails. Solvers: `cvxpy` (default), `scipy` SLSQP, `qubo_sa`.
5. **Outputs**: console tables, `portfolio_dashboard.html`, and the pipeline JSON.

Profiles (`--risk-profile` or `RISK_PROFILE`):

| Profile | Style | Max weight | Beta band vs. SPY |
|---|---|---|---|
| `conservador` | Value + Quality, risk-averse (λ=8) | 15% | 0.60 – 0.80 |
| `moderado` (default → Crecimiento) | Growth + Momentum + Quality (λ=4) | 20% | 0.80 – 0.95 |
| `agresivo` (Momentum) | Growth + Momentum (λ=2) | 25% | ≥ 0.95 |

Useful environment variables: `RISK_FREE_RATE` (default 0.040), `USAA_HORIZON_DAYS` / `USAA_HORIZON_MONTHS` (7–400 days, default 60).

Prices: Yahoo Finance (`yfinance`) is the primary source and FMP is only a fallback when `FMP_API_KEY` is set. Each ticker's adjusted close is cached in `/workspace/pipeline/state/prices` and only the missing range is downloaded. `USAA_PRICE_CACHE_DIR` moves the cache, `USAA_PRICE_CACHE=off` disables it, and `USAA_PRICE_SOURCE` (`yahoo,fmp` default, `yahoo` or `fmp`) sets the source order.

## 2. IG corporate bonds (`Corp_FR_Optimization.py`)

`run_pipeline` in six steps:

1. **Risk-free curve**: Treasury nodes from FRED, PCHIP-interpolated.
2. **Solvency screen**: US non-financial companies, market cap ≥ USD 10bn, Debt/EBITDA ≤ 3.0x, EBITDA/Interest ≥ 2.5x, debt ≥ USD 2bn. Those two limits are baselines: the rating selection relaxes them just enough to reach its worst rating (e.g. BBB down to B+ → ≤ 6.0x and ≥ 1.75x); they are never tightened.
3. **Free cash flow**: increasing FCF or 3-year CAGR > 3%.
4. **Synthetic rating**: worse of an interest-coverage rating and a Debt/EBITDA rating (overridable with `MANUAL_RATING_OVERRIDES`). Issuers rated below BBB- survive only if the rating selection includes them.
5. **Credit score**: weighted Z-scores of coverage, leverage, FCF growth and rating; top `TOP_N` (25) issuers selected. Set the range with `RATING_CEILING` and `RATING_FLOOR` (e.g. `"BBB"` and `"B+"` keep BBB, BBB-, BB+, BB, BB-, B+); or give an exact list in `RATING_SELECTION`, which overrides them; all `None` keeps everything. Z-scores are computed over the whole universe before this filter. Minimum spreads per rating letter live in `MIN_SPREAD_BPS_BY_BUCKET` (BB 250 bp, B 400 bp are indicative).
6. **Weights and target yield**: Equal and Score weighting (15% cap); minimum yield for 3/5/10 years = `Rf + rating spread + tenor premium + score adjustment`.

Outputs: console funnel and ranking, a Refinitiv checklist (buy if YTW ≥ target and OAS ≥ minimum), `reporte_portafolio_renta_fija.html` and the universe JSON.

## Pipeline JSON

Both scripts write `*_latest.json` plus a timestamped copy (UTF-8, atomic write, Bogotá timestamps). A write failure only prints a warning.

| Script | Directory (env var) | Files |
|---|---|---|
| `US Asset Manager.py` | `PORTFOLIO_OUT_DIR` | `portfolio_latest.json`, `portfolio_us_asset_manager_<timestamp>.json` |
| `Corp_FR_Optimization.py` | `UNIVERSE_OUT_DIR` | `corp_fr_latest.json`, `corp_fr_<timestamp>.json` |

## Tests and tools

```bash
python -m unittest discover -s tests          # offline, no network
python scripts/sweep_tail_penalty.py          # sweep the tail-penalty γ per profile (real data)
python scripts/check_risk_estimators_sync.py  # diff risk_estimators.py against the AM-PM copy
```

Browser report checks need `requirements-dev.txt` and `playwright install chromium` (set `SKIP_BROWSER_TESTS=1` to skip). Set `REPORT_PDF=1` to also export the reports as PDF.

`risk_estimators.py` is a hand-synced copy of the AM-PM repository module.

## Disclaimer

For academic and research purposes only; not investment advice. Synthetic ratings are a quantitative proxy and do not replace S&P, Moody's or Fitch ratings.
