# Graph Report - US-Asset-Allocation  (2026-10-29)

## Corpus Check
- 24 files · ~36,531 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 850 nodes · 1897 edges · 52 communities (39 shown, 13 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 63 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `abc9d80d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Corp_FR_Optimization.py
- numpy
- ndarray
- IG corporate bond issuer screening pipeline (run_pipeline)
- ImpliedTailModel
- test_html_reports_browser.py
- FakeResponse
- ImpliedMomentsEngine
- fmp_client.py
- Any
- ._profile
- write_json_files
- FakeProvider
- _tail_inputs
- test_risk_estimators_sync.py
- _load_manager
- math
- PriceCache
- mock_patch
- price_cache.py
- export_portfolio_json
- .prepare
- _historical_betas
- risk_estimators.py
- test_pipeline_contract.py
- DataFrame
- RawBetaTests
- Mean-variance optimization with factor targets
- Series
- report_pdf.py
- cornish_fisher_params
- to_years
- ledoit_wolf_constant_correlation
- LoaderIntegrationTests
- cache_dir_from_env
- Bakshi-Kapadia-Madan (BKM) model-free implied moments
- redact_secrets
- FactorModelBuilder
- MassiveBaseTests
- Minimum required yield by tenor
- US Asset Manager.py
- UniverseBuilder
- resolve_horizon_days
- .test_returns_covariance_and_weights_match
- Risk-free curve (FRED Treasury CMT, PCHIP)
- sweep_tail_penalty.py
- beta_range_reachable
- resolve_risk_profile
- MarketDataLoader
- resolve_risk_free_rate
- normalize_weights

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 29 edges
2. `FakeProvider` - 18 edges
3. `PortfolioOptimizer` - 17 edges
4. `APIAuthorizationError` - 17 edges
5. `FMPClient` - 16 edges
6. `PriceCache` - 16 edges
7. `ImpliedMomentsEngine` - 15 edges
8. `APIError` - 15 edges
9. `resolve_horizon_days()` - 15 edges
10. `build_html_report()` - 14 edges

## Surprising Connections (you probably didn't know these)
- `market_beta()` --implements--> `Market risk via beta band (market_beta, Blume shrinkage, raw beta for commodities)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `historical_adjusted_close()` --calls--> `APIAuthorizationError`  [EXTRACTED]
  tests/test_price_cache.py → fmp_client.py
- `resolve_risk_profile()` --implements--> `Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile)`  [EXTRACTED]
  pipeline_io.py → README.md
- `mfik_cap_tenor()` --implements--> `BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor)`  [EXTRACTED]
  risk_estimators.py → README.md
- `ImpliedTailModel` --implements--> `ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula)`  [EXTRACTED]
  US Asset Manager.py → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (52 total, 13 thin omitted)

### Community 0 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (38): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), effective_solvency_limits(), fcf_metrics() (+30 more)

### Community 1 - "numpy"
Cohesion: 0.12
Nodes (8): average_correlation(), ewma_weights(), martin_wagner_excess_return(), mfik_cap(), mfik_cap_tenor(), nearest_psd(), portfolio_moment_gradients(), q_to_p_correlation()

### Community 2 - "ndarray"
Cohesion: 0.17
Nodes (6): OptimizationError, PortfolioOptimizer, flip_delta(), violation(), objective(), _project_capped_simplex()

### Community 3 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.19
Nodes (12): Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Free cash flow screen (increasing or CAGR > 3%), Financial Modeling Prep (FMP) API, Shared FMP HTTP transport (throttling, retries, cache, plan-error detection), Phase 0 Hybrid ETF Universe, Offline unit tests (python -m unittest discover -s tests), PassiveETFAllocationPipeline (ETF allocation pipeline) (+4 more)

### Community 5 - "test_html_reports_browser.py"
Cohesion: 0.09
Nodes (12): collect_page_errors(), install_offline_route(), launch_browser(), load_playwright(), wait_for_plotly(), AllocationDashboardTests, CorpFixedIncomeHTMLTests, CorpFixedIncomeReportTests (+4 more)

### Community 6 - "FakeResponse"
Cohesion: 0.19
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 8 - "fmp_client.py"
Cohesion: 0.15
Nodes (5): APIAuthorizationError, APIError, BaseHTTPClient, _to_float(), PolygonClient

### Community 9 - "Any"
Cohesion: 0.26
Nodes (4): FMPClient, FMPClient, _json_float(), _to_float()

### Community 10 - "._profile"
Cohesion: 0.11
Nodes (7): ExportProfileTests, FactorTargetTests, PortfolioConstraintTests, _reload_manager(), RiskContributionTests, RiskProfileSelectionTests, _synthetic_inputs()

### Community 11 - "write_json_files"
Cohesion: 0.18
Nodes (8): atomic_write_json(), _atomic_write_text(), _dumps(), _horizon_from_source(), _horizon_number(), _warn(), write_json_files(), AtomicWriteTests

### Community 12 - "FakeProvider"
Cohesion: 0.17
Nodes (4): FakeProvider, IncrementalCacheTests, boom(), _raw_prices()

### Community 13 - "_tail_inputs"
Cohesion: 0.14
Nodes (5): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailPenaltySolveTests, TailRiskReportTests

### Community 14 - "test_risk_estimators_sync.py"
Cohesion: 0.17
Nodes (6): US Asset Allocation README, definitions(), main(), _all_names(), _other_path(), RiskEstimatorsSyncTests

### Community 15 - "_load_manager"
Cohesion: 0.24
Nodes (3): ExportHorizonTests, _load_manager(), ManagerHorizonTests

### Community 16 - "math"
Cohesion: 0.09
Nodes (11): american_call(), american_price(), bs93_phi(), bs_price(), horizon_option_window(), BlackScholesPricingTests, _Frozen, _load_manager() (+3 more)

### Community 18 - "mock_patch"
Cohesion: 0.15
Nodes (4): HorizonAlignmentTests, MfikCapTests, mock_patch, mock_stub()

### Community 19 - "price_cache.py"
Cohesion: 0.16
Nodes (4): _drop_open_session(), fetch_yahoo_adjusted_close(), to_yahoo_symbol(), YahooFetchTests

### Community 20 - "export_portfolio_json"
Cohesion: 0.23
Nodes (6): export_universe_json(), iso_bogota(), now_bogota(), stamp_bogota(), TimestampTests, export_portfolio_json()

### Community 21 - ".prepare"
Cohesion: 0.14
Nodes (5): beta_band_text(), BetaPoolFilter, market_beta(), PipelineInputs, RedundancyFilter

### Community 22 - "_historical_betas"
Cohesion: 0.22
Nodes (4): ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, _nearest_psd()

### Community 23 - "risk_estimators.py"
Cohesion: 0.12
Nodes (13): AM-PM repository (source of risk_estimators copy), Portfolio skewness/kurtosis in O(J n) with analytical gradients, Manual risk_estimators.py sync with AM-PM (drift check), SVIX / Martin-Wagner expected return (experimental, disabled), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_tail(), cornish_fisher_z() (+5 more)

### Community 24 - "test_pipeline_contract.py"
Cohesion: 0.26
Nodes (6): _am_pm_sample(), _load_by_path(), _load_us_manager(), PortfolioContractTests, _sibling_imports(), _us_sample()

### Community 25 - "DataFrame"
Cohesion: 0.40
Nodes (3): ConsoleReporter, OptimizationResult, PassiveETFAllocationPipeline

### Community 27 - "Mean-variance optimization with factor targets"
Cohesion: 0.20
Nodes (8): Factor loading matrix B (Value, Growth, Momentum, Quality), ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula), Investment profiles (Conservador, Crecimiento, Momentum/Agresivo), Mean-variance optimization with factor targets, Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile), Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing, Tail penalty (USE_TAIL_PENALTY, one-sided ES_CF - ES_Gaussian, SLSQP), Linear program for factor target feasibility and relaxation

### Community 29 - "report_pdf.py"
Cohesion: 0.10
Nodes (7): default_pdf_path(), export_report_pdf(), main(), _QuietHandler, ReportExportError, ReportPdfBrowserTests, ReportPdfUnitTests

### Community 30 - "cornish_fisher_params"
Cohesion: 0.40
Nodes (4): cornish_fisher_domain(), cornish_fisher_params(), a_parametros(), residuo()

### Community 31 - "to_years"
Cohesion: 0.22
Nodes (4): annualize(), scale_bkm_moments(), scale_moments(), to_years()

### Community 32 - "ledoit_wolf_constant_correlation"
Cohesion: 0.17
Nodes (8): cov_ewma_shrunk(), effective_sample_size(), ewma_cov(), ledoit_wolf_constant_correlation(), _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 34 - "cache_dir_from_env"
Cohesion: 0.22
Nodes (3): cache_dir_from_env(), resolve_price_sources(), SymbolAndEnvTests

### Community 35 - "Bakshi-Kapadia-Madan (BKM) model-free implied moments"
Cohesion: 0.22
Nodes (7): Bjerksund-Stensland American option model, BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), Bakshi-Kapadia-Madan (BKM) model-free implied moments, Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), EWMA correlation with Ledoit-Wolf shrinkage, Polygon.io options API

### Community 37 - "FactorModelBuilder"
Cohesion: 0.26
Nodes (4): _clip(), _combine_scores(), FactorModelBuilder, _percentile_score()

### Community 39 - "Minimum required yield by tenor"
Cohesion: 0.40
Nodes (5): Composite Credit Score, Academic-use disclaimer, Minimum required yield by tenor, Refinitiv Workspace bond-finding checklist (YTW, OAS buy rule), Weighting schemes (Equal Weight, Credit-Score Weight)

### Community 40 - "US Asset Manager.py"
Cohesion: 0.15
Nodes (4): portfolio_moments(), q_to_p_vol(), configure_logging(), main()

### Community 41 - "UniverseBuilder"
Cohesion: 0.38
Nodes (3): ETFDescriptor, _first_number(), UniverseBuilder

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

### Community 54 - "MarketDataLoader"
Cohesion: 0.25
Nodes (3): _is_configured_key(), MarketDataLoader, validate_configuration()

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 234 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PriceCache` connect `PriceCache` to `LoaderIntegrationTests`, `.test_returns_covariance_and_weights_match`, `FakeProvider`, `price_cache.py`, `.prepare`, `MarketDataLoader`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05056179775280899 - nodes in this community are weakly interconnected._
- **Why does `FMPClient` connect `Any` to `Corp_FR_Optimization.py`, `redact_secrets`, `FakeResponse`, `fmp_client.py`, `US Asset Manager.py`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `PortfolioOptimizer` connect `ndarray` to `US Asset Manager.py`, `DataFrame`, `beta_range_reachable`, `Series`?**
  _High betweenness centrality (0.025) - this node is a cross-community bridge._
- **Should `test_html_reports_browser.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0907563025210084 - nodes in this community are weakly interconnected._