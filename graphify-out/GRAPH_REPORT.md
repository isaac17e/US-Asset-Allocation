# Graph Report - US-Asset-Allocation  (2026-10-19)

## Corpus Check
- 16 files · ~31,756 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 4, .bak-20261018 1)

## Summary
- 672 nodes · 1421 edges · 35 communities (24 shown, 11 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 30 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `1cab0735`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Corp_FR_Optimization.py
- numpy
- DataFrame
- sweep_tail_penalty.py
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
- browser_test_helpers.py
- _load_manager
- US Asset Manager.py
- test_optimizer.py
- mock_patch
- RiskProfileTests
- export_portfolio_json
- APIAuthorizationError
- .prepare
- FactorModelBuilder
- AtomicWriteTests
- test_pipeline_io.py
- RawBetaTests
- Any
- UniverseBuilder
- cornish_fisher_moments
- WeightTests
- MassiveBaseTests
- math
- RiskFreeRateTests
- mfik_cap_tenor

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 26 edges
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
- `resolve_risk_profile()` --implements--> `Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile)`  [EXTRACTED]
  pipeline_io.py → README.md
- `mfik_cap_tenor()` --implements--> `BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor)`  [EXTRACTED]
  risk_estimators.py → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (35 total, 11 thin omitted)

### Community 0 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (35): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), _figure() (+27 more)

### Community 1 - "numpy"
Cohesion: 0.09
Nodes (16): Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cov_ewma_shrunk(), effective_sample_size(), ewma_cov(), ewma_weights() (+8 more)

### Community 2 - "DataFrame"
Cohesion: 0.05
Nodes (19): var_cvar_cornish_fisher(), beta_band_text(), beta_range_reachable(), BetaPoolFilter, ConsoleReporter, DashboardBuilder, ImpliedCovarianceBuilder, ImpliedTailModel (+11 more)

### Community 3 - "sweep_tail_penalty.py"
Cohesion: 0.05
Nodes (38): resolve_risk_free_rate(), Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD) (+30 more)

### Community 5 - "test_html_reports_browser.py"
Cohesion: 0.16
Nodes (8): wait_for_plotly(), AllocationDashboardTests, CorpFixedIncomeHTMLTests, CorpFixedIncomeReportTests, OfflineBrowserTestCase, _synthetic_corporate_inputs(), _synthetic_dashboard_inputs(), _write_corporate_report()

### Community 6 - "FakeResponse"
Cohesion: 0.17
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
Cohesion: 0.17
Nodes (11): atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), _horizon_from_source(), _horizon_number(), months_to_days(), resolve_horizon_days() (+3 more)

### Community 12 - "_delta_referencia"
Cohesion: 0.26
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 13 - "_tail_inputs"
Cohesion: 0.14
Nodes (5): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailPenaltySolveTests, TailRiskReportTests

### Community 14 - "browser_test_helpers.py"
Cohesion: 0.15
Nodes (4): collect_page_errors(), install_offline_route(), launch_browser(), load_playwright()

### Community 15 - "_load_manager"
Cohesion: 0.24
Nodes (3): ExportHorizonTests, _load_manager(), ManagerHorizonTests

### Community 16 - "US Asset Manager.py"
Cohesion: 0.17
Nodes (4): configure_logging(), _is_configured_key(), main(), validate_configuration()

### Community 18 - "mock_patch"
Cohesion: 0.15
Nodes (4): HorizonAlignmentTests, MfikCapTests, mock_patch, mock_stub()

### Community 20 - "export_portfolio_json"
Cohesion: 0.22
Nodes (6): export_universe_json(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), export_portfolio_json()

### Community 21 - "APIAuthorizationError"
Cohesion: 0.19
Nodes (4): APIAuthorizationError, APIError, MarketDataLoader, PolygonClient

### Community 22 - ".prepare"
Cohesion: 0.15
Nodes (5): ExpectedReturnModel, _historical_betas(), market_beta(), PipelineInputs, RedundancyFilter

### Community 23 - "FactorModelBuilder"
Cohesion: 0.26
Nodes (4): _clip(), _combine_scores(), FactorModelBuilder, _percentile_score()

### Community 29 - "cornish_fisher_moments"
Cohesion: 0.13
Nodes (10): cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params(), a_parametros(), residuo(), cornish_fisher_tail(), cornish_fisher_z(), higher_moments_admissible() (+2 more)

### Community 32 - "math"
Cohesion: 0.40
Nodes (4): horizon_option_window(), _first_number(), _json_float(), _to_float()

### Community 34 - "mfik_cap_tenor"
Cohesion: 0.40
Nodes (3): BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), mfik_cap(), mfik_cap_tenor()

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 217 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **11 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `DataFrame` to `US Asset Manager.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05048766494549627 - nodes in this community are weakly interconnected._
- **Why does `to_years()` connect `ImpliedMomentsEngine` to `US Asset Manager.py`, `numpy`, `DataFrame`, `test_optimizer.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.09269162210338681 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `sweep_tail_penalty.py` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.05348101265822785 - nodes in this community are weakly interconnected._