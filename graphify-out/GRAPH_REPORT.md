# Graph Report - US-Asset-Allocation  (2026-10-19)

## Corpus Check
- 18 files · ~32,433 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 4, .bak-20261018 1)

## Summary
- 700 nodes · 1470 edges · 39 communities (27 shown, 12 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `11c183b6`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Corp_FR_Optimization.py
- numpy
- DataFrame
- IG corporate bond issuer screening pipeline (run_pipeline)
- BKMEstimator
- test_html_reports_browser.py
- FakeResponse
- ImpliedMomentsEngine
- check_risk_estimators_sync.py
- fmp_client.py
- ._profile
- pipeline_io.py
- _delta_referencia
- _tail_inputs
- test_report_pdf.py
- _load_manager
- US Asset Manager.py
- test_optimizer.py
- mock_patch
- RiskProfileTests
- os
- APIAuthorizationError
- Mean-variance optimization with factor targets
- FactorModelBuilder
- AtomicWriteTests
- test_pipeline_io.py
- RawBetaTests
- Any
- UniverseBuilder
- report_pdf.py
- WeightTests
- MassiveBaseTests
- Bakshi-Kapadia-Madan (BKM) model-free implied moments
- RiskFreeRateTests
- logging
- Tail penalty (USE_TAIL_PENALTY, one-sided ES_CF - ES_Gaussian, SLSQP)
- resolve_risk_free_rate
- Minimum required yield by tenor
- ReportPdfUnitTests

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 27 edges
2. `PortfolioOptimizer` - 17 edges
3. `FMPClient` - 16 edges
4. `APIError` - 16 edges
5. `APIAuthorizationError` - 16 edges
6. `ImpliedMomentsEngine` - 15 edges
7. `OptimizationResult` - 14 edges
8. `export_portfolio_json()` - 14 edges
9. `FMPClient` - 13 edges
10. `build_html_report()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `market_beta()` --implements--> `Market risk via beta band (market_beta, Blume shrinkage, raw beta for commodities)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `ImpliedTailModel` --implements--> `ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `mfik_cap_tenor()` --implements--> `BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor)`  [EXTRACTED]
  risk_estimators.py → README.md
- `FMPClient` --uses--> `APIAuthorizationError`  [INFERRED]
  Corp_FR_Optimization.py → fmp_client.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (39 total, 12 thin omitted)

### Community 0 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (35): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), _figure() (+27 more)

### Community 1 - "numpy"
Cohesion: 0.05
Nodes (32): BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params() (+24 more)

### Community 2 - "DataFrame"
Cohesion: 0.05
Nodes (21): beta_band_text(), beta_range_reachable(), BetaPoolFilter, ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder (+13 more)

### Community 3 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.19
Nodes (12): Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Free cash flow screen (increasing or CAGR > 3%), Financial Modeling Prep (FMP) API, Shared FMP HTTP transport (throttling, retries, cache, plan-error detection), Phase 0 Hybrid ETF Universe, Offline unit tests (python -m unittest discover -s tests), PassiveETFAllocationPipeline (ETF allocation pipeline) (+4 more)

### Community 5 - "test_html_reports_browser.py"
Cohesion: 0.11
Nodes (10): collect_page_errors(), install_offline_route(), wait_for_plotly(), AllocationDashboardTests, CorpFixedIncomeHTMLTests, CorpFixedIncomeReportTests, OfflineBrowserTestCase, _synthetic_corporate_inputs() (+2 more)

### Community 6 - "FakeResponse"
Cohesion: 0.19
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 7 - "ImpliedMomentsEngine"
Cohesion: 0.08
Nodes (6): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ResolveHorizonTests, ImpliedMomentsEngine

### Community 8 - "check_risk_estimators_sync.py"
Cohesion: 0.24
Nodes (5): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Manual risk_estimators.py sync with AM-PM (drift check), definitions(), main()

### Community 9 - "fmp_client.py"
Cohesion: 0.23
Nodes (3): BaseHTTPClient, FMPClient, _to_float()

### Community 10 - "._profile"
Cohesion: 0.11
Nodes (7): ExportProfileTests, FactorTargetTests, PortfolioConstraintTests, _reload_manager(), RiskContributionTests, RiskProfileSelectionTests, _synthetic_inputs()

### Community 11 - "pipeline_io.py"
Cohesion: 0.20
Nodes (9): atomic_write_json(), _atomic_write_text(), _dumps(), _horizon_from_source(), _horizon_number(), months_to_days(), resolve_horizon_days(), _warn() (+1 more)

### Community 12 - "_delta_referencia"
Cohesion: 0.26
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 13 - "_tail_inputs"
Cohesion: 0.14
Nodes (5): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailPenaltySolveTests, TailRiskReportTests

### Community 14 - "test_report_pdf.py"
Cohesion: 0.24
Nodes (3): launch_browser(), load_playwright(), ReportPdfBrowserTests

### Community 15 - "_load_manager"
Cohesion: 0.24
Nodes (3): ExportHorizonTests, _load_manager(), ManagerHorizonTests

### Community 16 - "US Asset Manager.py"
Cohesion: 0.12
Nodes (5): horizon_option_window(), _clip(), _json_float(), PortfolioTailRisk, _to_float()

### Community 18 - "mock_patch"
Cohesion: 0.15
Nodes (4): HorizonAlignmentTests, MfikCapTests, mock_patch, mock_stub()

### Community 20 - "os"
Cohesion: 0.22
Nodes (6): export_universe_json(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), export_portfolio_json()

### Community 21 - "APIAuthorizationError"
Cohesion: 0.21
Nodes (4): APIAuthorizationError, APIError, MarketDataLoader, PolygonClient

### Community 22 - "Mean-variance optimization with factor targets"
Cohesion: 0.22
Nodes (5): Factor loading matrix B (Value, Growth, Momentum, Quality), Mean-variance optimization with factor targets, Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing, Linear program for factor target feasibility and relaxation, market_beta()

### Community 23 - "FactorModelBuilder"
Cohesion: 0.31
Nodes (4): _combine_scores(), FactorModelBuilder, _first_number(), _percentile_score()

### Community 29 - "report_pdf.py"
Cohesion: 0.13
Nodes (5): default_pdf_path(), export_report_pdf(), main(), _QuietHandler, ReportExportError

### Community 32 - "Bakshi-Kapadia-Madan (BKM) model-free implied moments"
Cohesion: 0.25
Nodes (7): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), EWMA correlation with Ledoit-Wolf shrinkage, ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula), Polygon.io options API

### Community 34 - "logging"
Cohesion: 0.38
Nodes (4): configure_logging(), _is_configured_key(), main(), validate_configuration()

### Community 35 - "Tail penalty (USE_TAIL_PENALTY, one-sided ES_CF - ES_Gaussian, SLSQP)"
Cohesion: 0.29
Nodes (5): _cli_risk_profile(), resolve_risk_profile(), Investment profiles (Conservador, Crecimiento, Momentum/Agresivo), Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile), Tail penalty (USE_TAIL_PENALTY, one-sided ES_CF - ES_Gaussian, SLSQP)

### Community 36 - "resolve_risk_free_rate"
Cohesion: 0.33
Nodes (5): resolve_risk_free_rate(), Expected return mu (75% CAPM, 25% historical), FRED API, Risk-free curve (FRED Treasury CMT, PCHIP), RISK_FREE_RATE override (resolve_risk_free_rate)

### Community 37 - "Minimum required yield by tenor"
Cohesion: 0.40
Nodes (5): Composite Credit Score, Academic-use disclaimer, Minimum required yield by tenor, Refinitiv Workspace bond-finding checklist (YTW, OAS buy rule), Weighting schemes (Equal Weight, Credit-Score Weight)

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 234 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `DataFrame` to `US Asset Manager.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05048766494549627 - nodes in this community are weakly interconnected._
- **Why does `to_years()` connect `ImpliedMomentsEngine` to `US Asset Manager.py`, `numpy`, `test_optimizer.py`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.05110809588421529 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`, `resolve_risk_free_rate`, `Minimum required yield by tenor`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.051061388410786 - nodes in this community are weakly interconnected._