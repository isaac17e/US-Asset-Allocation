# Graph Report - US-Asset-Allocation  (2026-10-14)

## Corpus Check
- 11 files · ~29,200 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 597 nodes · 1272 edges · 38 communities (19 shown, 19 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 27 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Corp FR Pipeline Functions
- risk_estimators & README Concepts
- Optimizer Beta Constraints
- README Corp FR & Options Concepts
- Tail Risk & Report Plotting
- US Asset Manager Imports
- FMP Client Tests
- ImpliedMomentsEngine
- FMP HTTP Transport
- FMPClient Data Endpoints
- ._profile
- Pipeline JSON Export
- test_risk_estimators.py
- _tail_inputs
- Sync Check & README Meta
- pipeline_io Test Imports
- Atomic JSON Writing
- test_optimizer.py
- mock_patch
- Implied Covariance Builder
- UniverseBuilder
- Factor Model Builder
- Market Data Loader
- MfikCapTests
- AtomicWriteTests
- RiskProfileTests
- RawBetaTests
- ExportProfileTests
- TailPenaltySolveTests
- RiskFreeRate Tests
- WeightTests
- Risk Profile Resolution

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

## Communities (38 total, 19 thin omitted)

### Community 0 - "Corp FR Pipeline Functions"
Cohesion: 0.05
Nodes (35): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), _figure() (+27 more)

### Community 1 - "risk_estimators & README Concepts"
Cohesion: 0.06
Nodes (30): BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params() (+22 more)

### Community 2 - "Optimizer Beta Constraints"
Cohesion: 0.08
Nodes (9): beta_range_reachable(), BKMEstimator, ImpliedTailModel, OptimizationError, PortfolioOptimizer, flip_delta(), violation(), objective() (+1 more)

### Community 3 - "README Corp FR & Options Concepts"
Cohesion: 0.06
Nodes (36): resolve_risk_free_rate(), Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD) (+28 more)

### Community 4 - "Tail Risk & Report Plotting"
Cohesion: 0.10
Nodes (11): var_cvar_cornish_fisher(), beta_band_text(), BetaPoolFilter, _combine_scores(), ConsoleReporter, DashboardBuilder, OptimizationResult, PassiveETFAllocationPipeline (+3 more)

### Community 5 - "US Asset Manager Imports"
Cohesion: 0.11
Nodes (8): _clip(), configure_logging(), ExpectedReturnModel, _historical_betas(), _json_float(), main(), market_beta(), _to_float()

### Community 6 - "FMP Client Tests"
Cohesion: 0.16
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 7 - "ImpliedMomentsEngine"
Cohesion: 0.14
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 8 - "FMP HTTP Transport"
Cohesion: 0.18
Nodes (5): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float()

### Community 9 - "FMPClient Data Endpoints"
Cohesion: 0.17
Nodes (4): FMPClient, _is_configured_key(), PolygonClient, validate_configuration()

### Community 10 - "._profile"
Cohesion: 0.19
Nodes (3): FactorTargetTests, PortfolioConstraintTests, RiskProfileSelectionTests

### Community 11 - "Pipeline JSON Export"
Cohesion: 0.23
Nodes (6): export_universe_json(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), export_portfolio_json()

### Community 12 - "test_risk_estimators.py"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 13 - "_tail_inputs"
Cohesion: 0.19
Nodes (4): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailRiskReportTests

### Community 14 - "Sync Check & README Meta"
Cohesion: 0.20
Nodes (5): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Manual risk_estimators.py sync with AM-PM (drift check), definitions(), main()

### Community 16 - "Atomic JSON Writing"
Cohesion: 0.29
Nodes (5): atomic_write_json(), _atomic_write_text(), _dumps(), _warn(), write_json_files()

### Community 17 - "test_optimizer.py"
Cohesion: 0.20
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

### Community 19 - "Implied Covariance Builder"
Cohesion: 0.28
Nodes (3): q_to_p_vol(), ImpliedCovarianceBuilder, _nearest_psd()

### Community 22 - "Market Data Loader"
Cohesion: 0.22
Nodes (3): MarketDataLoader, PipelineInputs, RedundancyFilter

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 189 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **19 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `Optimizer Beta Constraints` to `Tail Risk & Report Plotting`, `US Asset Manager Imports`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Corp FR Pipeline Functions` be split into smaller, more focused modules?**
  _Cohesion score 0.05048766494549627 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `README Corp FR & Options Concepts` to `Corp FR Pipeline Functions`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `risk_estimators & README Concepts` be split into smaller, more focused modules?**
  _Cohesion score 0.05552617662612375 - nodes in this community are weakly interconnected._
- **Why does `FMPClient` connect `FMP HTTP Transport` to `Corp FR Pipeline Functions`, `FMPClient Data Endpoints`, `US Asset Manager Imports`, `FMP Client Tests`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Should `Optimizer Beta Constraints` be split into smaller, more focused modules?**
  _Cohesion score 0.08282828282828283 - nodes in this community are weakly interconnected._