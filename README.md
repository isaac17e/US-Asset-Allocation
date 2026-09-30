# US Asset Allocation

Python tools for building investment portfolios in the US market from live market data. The repository contains two independent pipelines and a shared risk-estimation module:

| File | What it does |
|---|---|
| [`US Asset Manager.py`](US%20Asset%20Manager.py) | **ETF** asset allocation: builds the universe, estimates factor exposures, option-implied moments and covariance, and optimizes weights for an investment profile. |
| [`Corp_FR_Optimization.py`](Corp_FR_Optimization.py) | **Investment Grade corporate fixed income (USD)** portfolio selection: screens issuers on solvency, cash flow and rating, ranks them, and computes the minimum required yield by tenor. |
| [`risk_estimators.py`](risk_estimators.py) | Risk estimator library (EWMA + Ledoit-Wolf covariance, Q→P correction, portfolio moments, Cornish-Fisher). Used by `US Asset Manager.py`. |

Each script runs end to end, prints tables to the console and produces an interactive Plotly HTML report.

> Code comments, console output and the HTML reports are in Spanish.

---

## 1. `US Asset Manager.py` — Passive ETF allocation

A pipeline orchestrated by the `PassiveETFAllocationPipeline` class, organized in phases:

### Phase 0 · Hybrid universe
- **Master list** of ~50 ETFs (`MASTER_ETF_LIST`): US core indices, factor/style, sectors, megatrends, international, commodities, fixed income and real estate.
- **Dynamic candidates** from the FMP screener (NYSE, NASDAQ, AMEX), filtered by dollar volume (≥ USD 1M per day), excluding leveraged and inverse ETFs.
- Downloads adjusted prices (3 years) and **removes replicas**: a dynamic ETF is dropped if its correlation with one already included is ≥ 0.985.

### Phase 1 · Factor loading matrix **B**
Each ETF gets a score between 0 and 1 on five factors:

| Factor | How it is measured |
|---|---|
| Value | Earnings yield and book yield of the top 10 holdings |
| Growth | Revenue and EPS growth of the holdings |
| Momentum | 12-1 month return |
| Quality | ROE and ROIC of the holdings |
| LowVol | 252-day realized volatility (inverted) |

Fundamentals are aggregated by holding weight and converted into percentiles within the universe. Missing data leaves the factor neutral (0.5).

### Phase 2 · Moments, covariance and expected return
- **Implied moments (BKM)**: from the Polygon option chain (30 to 90 day expiries), the model-free implied volatility, skewness and kurtosis (MFIV, MFIS, MFIK) are estimated with Bakshi, Kapadia & Madan (2003). Each strike's implied volatility is obtained by inverting the Bjerksund-Stensland American option model, smoothed with a spline, and the results are interpolated to a 60-day horizon. Dividend yields are read per ticker from FMP. If no options are available, historical moments are used instead.
- **Covariance**: Σ = D·R·D, where
  - **D** holds the implied volatilities adjusted from the Q (risk-neutral) measure to the P (physical) measure to remove the variance risk premium;
  - **R** is the historical EWMA correlation (120-day half-life) with Ledoit-Wolf shrinkage toward constant correlation.
  - A `beta` mode (single-factor model against SPY) is also available.
- **Expected return μ**: 75% CAPM (4% risk-free rate + β · 5% equity premium) and 25% historical mean.

### Phase 3 · Optimization
Maximizes mean-variance utility

```
max  μᵀw − ½·λ·wᵀΣw
s.t. Σw = 1,   0 ≤ w ≤ w_max,   Bᵀw ≥ factor targets
```

Parameters depend on the selected profile:

| Profile | λ | w_max | Minimum targets |
|---|---|---|---|
| Conservador (Conservative) | 8 | 15% | Value 0.45 · Quality 0.55 · LowVol 0.70 |
| Crecimiento (Growth) | 4 | 20% | Growth 0.60 · Momentum 0.45 · Quality 0.55 |
| Momentum/Agresivo (Aggressive) | 2 | 25% | Growth 0.55 · Momentum 0.70 |

Before optimizing, a linear program checks that the targets are attainable and, if they are not, relaxes them by the minimum amount needed. Three solvers are available and can optionally be compared against each other:
- `cvxpy`: quadratic programming (default);
- `scipy`: SLSQP;
- `qubo_sa`: QUBO formulation with 5 bits per asset, solved with *simulated annealing*.

### Phases 4 and 5 · Outputs
- Console: universe composition, dropped ETFs, factors, moments, μ, optimal weights, target vs. achieved factor exposure, metrics (return, volatility, Sharpe, effective N) and the solver comparison.
- `portfolio_dashboard.html`: allocation chart, factor radar, risk-return scatter and weight vs. risk contribution.

---

## 2. `Corp_FR_Optimization.py` — IG corporate bond portfolio

A six-phase issuer screening pipeline (`run_pipeline`):

1. **Risk-free curve**: Treasury CMT nodes (1M to 30Y) from FRED, interpolated with PCHIP.
2. **Screening and solvency**: US companies with market cap ≥ USD 10bn, excluding financial services. Requires Debt/EBITDA ≤ 3.0x and EBITDA/Interest ≥ 2.5x.
3. **Free cash flow**: strictly increasing FCF **or** 3-year CAGR > 3% (configurable as `AND`).
4. **Rating**: investment grade only (AAA to BBB-). FMP's rating is used as a proxy, and `MANUAL_RATING_OVERRIDES` lets you replace it with actual agency ratings.
5. **Composite Credit Score**: `0.40·Z(Coverage) + 0.30·Z(−Debt/EBITDA) + 0.30·Z(FCF CAGR)`, with Z-scores winsorized at ±3. The top 15 issuers are selected.
6. **Weighting and Yield Target**:
   - two weighting schemes: Equal Weight and Credit-Score Weight (15% cap per issuer), on a USD 10M notional;
   - **minimum required yield** for 3, 5 and 10 year tenors: `Rf(t) + rating spread + tenor premium + score adjustment`.

**Outputs**: screening funnel, ranking, weights, yield target table, a checklist for finding the actual bond issues in **Refinitiv Workspace** (buy rule: YTW ≥ Target and OAS ≥ minimum spread) and the `reporte_portafolio_renta_fija.html` report.

---

## 3. `risk_estimators.py` — Risk estimators

A module with no network dependencies. It is a copy of the module of the same name in the AM-PM repository and must be kept in sync with it.

1. **Covariance**: EWMA, Kish effective sample size and Ledoit-Wolf (2003) shrinkage toward constant correlation (`cov_ewma_shrunk`), plus projection onto the nearest positive semidefinite matrix.
2. **Q → P correction**: for implied volatility (variance risk premium) and implied correlation (correlation risk premium).
3. **Portfolio moments**: portfolio skewness and kurtosis computed over a scenario panel in O(J·n), without building the co-moment tensors, along with their analytical gradients.
4. **Cornish-Fisher**: admissibility check (K ≥ 1 + S²) and moment → parameter inversion following Maillard (2012), giving monotonic and consistent VaR/CVaR.
5. **SVIX / Martin-Wagner**: expected return from implied variances. *Experimental and disabled*: the formula has not yet been verified against the paper.

---

## Requirements

Python 3.10 or later and:

```bash
pip install numpy pandas scipy requests plotly python-dotenv cvxpy tabulate fredapi
```

`cvxpy`, `tabulate` and `fredapi` are optional: without them the scripts fall back to SciPy, `pandas.to_string` and the FRED REST API, respectively.

### API keys

| Variable | Service | Used by |
|---|---|---|
| `FMP_API_KEY` | [Financial Modeling Prep](https://financialmodelingprep.com) | Both scripts (required) |
| `POLYGON_API_KEY` | [Polygon.io](https://polygon.io): options snapshot | `US Asset Manager.py` (optional; without it, historical moments are used) |
| `FRED_API_KEY` | [FRED](https://fred.stlouisfed.org/docs/api/api_key.html) | `Corp_FR_Optimization.py` (required) |

Some FMP endpoints (ETF holdings, financial statements, ratings) depend on your subscription plan. If an endpoint is unavailable, the script disables it and continues with neutral or fallback values.

## Usage

```bash
cp .env.example .env    # then edit .env with your keys (it is git-ignored)
pip install python-dotenv

python "US Asset Manager.py"        # produces portfolio_dashboard.html
python Corp_FR_Optimization.py      # produces reporte_portafolio_renta_fija.html
```

All parameters (investment profile, solver, screening thresholds, score weights, rating spreads, etc.) live in the configuration block at the top of each file.

## Disclaimer

This code is for academic and research purposes only and does not constitute investment advice. In particular, FMP ratings are a quantitative proxy and do not replace ratings from S&P, Moody's or Fitch.
