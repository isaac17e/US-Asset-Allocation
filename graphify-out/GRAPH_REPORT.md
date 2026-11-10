# Graph Report - US-Asset-Allocation  (2026-11-10)

## Corpus Check
- 24 files · ~36,789 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 4, .example 1)

## Summary
- 855 nodes · 1889 edges · 51 communities (37 shown, 14 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 56 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3a321f5c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- _rating_rank
- numpy
- DataFrame
- IG corporate bond issuer screening pipeline (run_pipeline)
- FMPClient
- test_html_reports_browser.py
- FakeResponse
- ImpliedMomentsEngine
- Any
- Corp_FR_Optimization.py
- ._profile
- pipeline_io.py
- FakeProvider
- _tail_inputs
- test_risk_estimators_sync.py
- _load_manager
- math
- PriceCache
- mock_patch
- fetch_yahoo_adjusted_close
- export_portfolio_json
- market_beta
- pandas
- cornish_fisher_moments
- test_pipeline_contract.py
- RiskFreeCurve
- RawBetaTests
- Mean-variance optimization with factor targets
- stage_scoring
- report_pdf.py
- build_html_report
- .__init__
- ledoit_wolf_constant_correlation
- LoaderIntegrationTests
- cache_dir_from_env
- Bakshi-Kapadia-Madan (BKM) model-free implied moments
- _Frozen
- MassiveBaseTests
- Minimum required yield by tenor
- US Asset Manager.py
- resolve_horizon_days
- .test_returns_covariance_and_weights_match
- Risk-free curve (FRED Treasury CMT, PCHIP)
- sweep_tail_penalty.py
- resolve_risk_profile
- resolve_risk_free_rate

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 29 edges
2. `FakeProvider` - 18 edges
3. `PortfolioOptimizer` - 17 edges
4. `PriceCache` - 16 edges
5. `APIAuthorizationError` - 16 edges
6. `FMPClient` - 16 edges
7. `ImpliedMomentsEngine` - 15 edges
8. `resolve_horizon_days()` - 15 edges
9. `OptimizationResult` - 14 edges
10. `APIError` - 14 edges

## Surprising Connections (you probably didn't know these)
- `historical_adjusted_close()` --calls--> `APIAuthorizationError`  [EXTRACTED]
  tests/test_price_cache.py → fmp_client.py
- `mfik_cap_tenor()` --implements--> `BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor)`  [EXTRACTED]
  risk_estimators.py → README.md
- `resolve_risk_profile()` --implements--> `Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile)`  [EXTRACTED]
  pipeline_io.py → README.md
- `ImpliedTailModel` --implements--> `ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (51 total, 14 thin omitted)

### Community 0 - "_rating_rank"
Cohesion: 0.14
Nodes (9): effective_solvency_limits(), rating_bucket(), _rating_rank(), select_ratings(), _selected_ratings(), stage_rating(), synthetic_rating(), validate_rating_selection() (+1 more)

### Community 1 - "numpy"
Cohesion: 0.10
Nodes (14): Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), ewma_weights(), martin_wagner_excess_return(), mfik_cap(), mfik_cap_tenor(), nearest_psd() (+6 more)

### Community 2 - "DataFrame"
Cohesion: 0.06
Nodes (20): beta_range_reachable(), _combine_scores(), ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, ImpliedTailModel (+12 more)

### Community 3 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.19
Nodes (12): Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Free cash flow screen (increasing or CAGR > 3%), Financial Modeling Prep (FMP) API, Shared FMP HTTP transport (throttling, retries, cache, plan-error detection), Phase 0 Hybrid ETF Universe, Offline unit tests (python -m unittest discover -s tests), PassiveETFAllocationPipeline (ETF allocation pipeline) (+4 more)

### Community 4 - "FMPClient"
Cohesion: 0.15
Nodes (4): FMPClient, _latest(), stage_solvency(), _to_float()

### Community 5 - "test_html_reports_browser.py"
Cohesion: 0.09
Nodes (12): collect_page_errors(), install_offline_route(), launch_browser(), load_playwright(), wait_for_plotly(), AllocationDashboardTests, CorpFixedIncomeHTMLTests, CorpFixedIncomeReportTests (+4 more)

### Community 6 - "FakeResponse"
Cohesion: 0.19
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 7 - "ImpliedMomentsEngine"
Cohesion: 0.15
Nodes (4): annualize(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 8 - "Any"
Cohesion: 0.06
Nodes (16): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, redact_secrets(), _to_float(), SecretRedactionTests, beta_band_text() (+8 more)

### Community 9 - "Corp_FR_Optimization.py"
Cohesion: 0.22
Nodes (7): _abort_if_empty(), _check_keys(), export_universe_json(), fcf_metrics(), print_funnel(), run_pipeline(), stage_fcf()

### Community 10 - "._profile"
Cohesion: 0.11
Nodes (7): ExportProfileTests, FactorTargetTests, PortfolioConstraintTests, _reload_manager(), RiskContributionTests, RiskProfileSelectionTests, _synthetic_inputs()

### Community 11 - "pipeline_io.py"
Cohesion: 0.11
Nodes (8): atomic_write_json(), _atomic_write_text(), _dumps(), _horizon_from_source(), _horizon_number(), _warn(), write_json_files(), AtomicWriteTests

### Community 12 - "FakeProvider"
Cohesion: 0.17
Nodes (4): FakeProvider, IncrementalCacheTests, boom(), _raw_prices()

### Community 13 - "_tail_inputs"
Cohesion: 0.14
Nodes (5): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailPenaltySolveTests, TailRiskReportTests

### Community 14 - "test_risk_estimators_sync.py"
Cohesion: 0.15
Nodes (8): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Manual risk_estimators.py sync with AM-PM (drift check), definitions(), main(), _all_names(), _other_path(), RiskEstimatorsSyncTests

### Community 15 - "_load_manager"
Cohesion: 0.24
Nodes (3): ExportHorizonTests, _load_manager(), ManagerHorizonTests

### Community 16 - "math"
Cohesion: 0.09
Nodes (14): american_call(), american_price(), bs93_phi(), bs_price(), horizon_option_window(), BlackScholesPricingTests, _load_manager(), _outcome() (+6 more)

### Community 18 - "mock_patch"
Cohesion: 0.15
Nodes (4): HorizonAlignmentTests, MfikCapTests, mock_patch, mock_stub()

### Community 19 - "fetch_yahoo_adjusted_close"
Cohesion: 0.17
Nodes (4): _drop_open_session(), fetch_yahoo_adjusted_close(), to_yahoo_symbol(), YahooFetchTests

### Community 20 - "export_portfolio_json"
Cohesion: 0.16
Nodes (8): iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), TimestampTests, WeightTests, export_portfolio_json(), _json_float()

### Community 22 - "pandas"
Cohesion: 0.26
Nodes (10): _banner(), _fmt_pct(), _overlay_pivot(), portfolio_summary(), print_curve(), print_overlay(), print_ranking(), print_refinitiv_instructions() (+2 more)

### Community 23 - "cornish_fisher_moments"
Cohesion: 0.15
Nodes (9): cornish_fisher_domain(), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params(), a_parametros(), residuo(), cornish_fisher_tail(), cornish_fisher_z() (+1 more)

### Community 24 - "test_pipeline_contract.py"
Cohesion: 0.27
Nodes (6): _am_pm_sample(), _load_by_path(), _load_us_manager(), PortfolioContractTests, _sibling_imports(), _us_sample()

### Community 25 - "RiskFreeCurve"
Cohesion: 0.18
Nodes (3): build_risk_free_curve(), RiskFreeCurve, stage_overlay()

### Community 27 - "Mean-variance optimization with factor targets"
Cohesion: 0.25
Nodes (7): Factor loading matrix B (Value, Growth, Momentum, Quality), Investment profiles (Conservador, Crecimiento, Momentum/Agresivo), Mean-variance optimization with factor targets, Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile), Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing, Tail penalty (USE_TAIL_PENALTY, one-sided ES_CF - ES_Gaussian, SLSQP), Linear program for factor target feasibility and relaxation

### Community 28 - "stage_scoring"
Cohesion: 0.22
Nodes (4): cap_weights(), stage_scoring(), stage_weights(), zscore()

### Community 29 - "report_pdf.py"
Cohesion: 0.10
Nodes (7): default_pdf_path(), export_report_pdf(), main(), _QuietHandler, ReportExportError, ReportPdfBrowserTests, ReportPdfUnitTests

### Community 31 - ".__init__"
Cohesion: 0.29
Nodes (3): higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 32 - "ledoit_wolf_constant_correlation"
Cohesion: 0.17
Nodes (8): cov_ewma_shrunk(), effective_sample_size(), ewma_cov(), ledoit_wolf_constant_correlation(), _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 34 - "cache_dir_from_env"
Cohesion: 0.22
Nodes (3): cache_dir_from_env(), resolve_price_sources(), SymbolAndEnvTests

### Community 35 - "Bakshi-Kapadia-Madan (BKM) model-free implied moments"
Cohesion: 0.22
Nodes (8): Bjerksund-Stensland American option model, BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), Bakshi-Kapadia-Madan (BKM) model-free implied moments, Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), EWMA correlation with Ledoit-Wolf shrinkage, ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula), Polygon.io options API

### Community 39 - "Minimum required yield by tenor"
Cohesion: 0.40
Nodes (5): Composite Credit Score, Academic-use disclaimer, Minimum required yield by tenor, Refinitiv Workspace bond-finding checklist (YTW, OAS buy rule), Weighting schemes (Equal Weight, Credit-Score Weight)

### Community 40 - "US Asset Manager.py"
Cohesion: 0.18
Nodes (4): configure_logging(), _is_configured_key(), main(), validate_configuration()

### Community 42 - "resolve_horizon_days"
Cohesion: 0.20
Nodes (3): months_to_days(), resolve_horizon_days(), ResolveHorizonTests

### Community 43 - ".test_returns_covariance_and_weights_match"
Cohesion: 0.40
Nodes (3): OptimizerInputsTests, loader(), yahoo()

### Community 44 - "Risk-free curve (FRED Treasury CMT, PCHIP)"
Cohesion: 0.50
Nodes (4): Expected return mu (75% CAPM, 25% historical), FRED API, Risk-free curve (FRED Treasury CMT, PCHIP), RISK_FREE_RATE override (resolve_risk_free_rate)

### Community 53 - "resolve_risk_profile"
Cohesion: 0.31
Nodes (3): _cli_risk_profile(), resolve_risk_profile(), RiskProfileTests

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing`, `Linear program for factor target feasibility and relaxation`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 241 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **14 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PriceCache` connect `PriceCache` to `LoaderIntegrationTests`, `Any`, `pipeline_io.py`, `FakeProvider`, `.test_returns_covariance_and_weights_match`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `_rating_rank` be split into smaller, more focused modules?**
  _Cohesion score 0.1437908496732026 - nodes in this community are weakly interconnected._
- **Why does `PortfolioOptimizer` connect `DataFrame` to `US Asset Manager.py`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.10317460317460317 - nodes in this community are weakly interconnected._
- **Why does `FMPClient` connect `Any` to `US Asset Manager.py`, `Corp_FR_Optimization.py`, `FakeResponse`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.05939629990262902 - nodes in this community are weakly interconnected._