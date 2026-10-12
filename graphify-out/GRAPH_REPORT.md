# Graph Report - US-Asset-Allocation  (2026-10-12)

## Corpus Check
- 14 files · ~30,280 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 598 nodes · 1257 edges · 46 communities (26 shown, 20 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fed0d43d`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DataFrame
- cornish_fisher_params
- ImpliedMomentsEngine
- Corp_FR_Optimization.py
- US Asset Manager.py
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- test_risk_estimators.py
- FakeResponse
- numpy
- cornish_fisher_moments
- ._profile
- .__init__
- Any
- sweep_tail_penalty.py
- _tail_inputs
- BKMEstimator
- cov_ewma_shrunk
- fmp_client.py
- .prepare
- Working with the graphify knowledge graph
- risk_estimators.py
- export_portfolio_json
- FactorModelBuilder
- test_pipeline_io.py
- Working with the graphify knowledge graph
- test_optimizer.py
- beta_range_reachable
- _first_number
- WeightTests
- mock_patch
- sys
- .__init__
- MfikCapTests
- AtomicWriteTests
- RiskProfileTests
- RawBetaTests
- ExportProfileTests
- TailPenaltySolveTests
- RiskFreeRateTests
- resolve_risk_profile

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 26 edges
2. `PortfolioOptimizer` - 17 edges
3. `FMPClient` - 15 edges
4. `OptimizationResult` - 14 edges
5. `export_portfolio_json()` - 14 edges
6. `ImpliedMomentsEngine` - 13 edges
7. `FMPClient` - 13 edges
8. `FakeResponse` - 12 edges
9. `build_html_report()` - 12 edges
10. `scale_moments()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `FMPClient` --uses--> `APIAuthorizationError`  [INFERRED]
  Corp_FR_Optimization.py → fmp_client.py
- `FMPClient` --uses--> `APIError`  [INFERRED]
  Corp_FR_Optimization.py → fmp_client.py
- `export_portfolio_json()` --calls--> `write_json_files()`  [EXTRACTED]
  US Asset Manager.py → pipeline_io.py
- `export_universe_json()` --calls--> `now_bogota()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (46 total, 20 thin omitted)

### Community 0 - "DataFrame"
Cohesion: 0.06
Nodes (17): ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, ImpliedTailModel, _nearest_psd(), OptimizationError (+9 more)

### Community 1 - "cornish_fisher_params"
Cohesion: 0.40
Nodes (4): cornish_fisher_domain(), cornish_fisher_params(), a_parametros(), residuo()

### Community 2 - "ImpliedMomentsEngine"
Cohesion: 0.14
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 3 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (39): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), export_universe_json(), fcf_metrics() (+31 more)

### Community 5 - "pipeline_io.py"
Cohesion: 0.23
Nodes (6): atomic_write_json(), _atomic_write_text(), _dumps(), resolve_risk_free_rate(), _warn(), write_json_files()

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "test_risk_estimators.py"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 8 - "FakeResponse"
Cohesion: 0.16
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 9 - "numpy"
Cohesion: 0.17
Nodes (6): martin_wagner_excess_return(), mfik_cap(), mfik_cap_tenor(), portfolio_moment_gradients(), q_to_p_correlation(), q_to_p_vol()

### Community 10 - "cornish_fisher_moments"
Cohesion: 0.22
Nodes (5): cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_tail(), cornish_fisher_z(), var_cvar_cornish_fisher()

### Community 11 - "._profile"
Cohesion: 0.19
Nodes (3): FactorTargetTests, PortfolioConstraintTests, RiskProfileSelectionTests

### Community 12 - ".__init__"
Cohesion: 0.29
Nodes (3): higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 14 - "sweep_tail_penalty.py"
Cohesion: 0.36
Nodes (4): load_manager(), main(), configure_logging(), main()

### Community 15 - "_tail_inputs"
Cohesion: 0.19
Nodes (4): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailRiskReportTests

### Community 17 - "cov_ewma_shrunk"
Cohesion: 0.25
Nodes (4): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ledoit_wolf_constant_correlation()

### Community 18 - "fmp_client.py"
Cohesion: 0.18
Nodes (5): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float()

### Community 19 - ".prepare"
Cohesion: 0.17
Nodes (4): market_beta(), MarketDataLoader, PipelineInputs, RedundancyFilter

### Community 20 - "Working with the graphify knowledge graph"
Cohesion: 0.33
Nodes (5): Freshness check, Git hygiene, Navigating, Verify before asserting, Working with the graphify knowledge graph

### Community 21 - "risk_estimators.py"
Cohesion: 0.15
Nodes (9): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), ewma_cov(), ewma_weights(), nearest_psd() (+1 more)

### Community 22 - "export_portfolio_json"
Cohesion: 0.23
Nodes (6): iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), export_portfolio_json(), _json_float()

### Community 23 - "FactorModelBuilder"
Cohesion: 0.26
Nodes (4): _clip(), _combine_scores(), FactorModelBuilder, _percentile_score()

### Community 25 - "Working with the graphify knowledge graph"
Cohesion: 0.33
Nodes (5): Freshness check, Git hygiene, Navigating, Verify before asserting, Working with the graphify knowledge graph

### Community 26 - "test_optimizer.py"
Cohesion: 0.20
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

### Community 27 - "beta_range_reachable"
Cohesion: 0.20
Nodes (3): beta_band_text(), beta_range_reachable(), BetaPoolFilter

### Community 28 - "_first_number"
Cohesion: 0.33
Nodes (4): ETFDescriptor, _first_number(), _to_float(), UniverseBuilder

### Community 32 - ".__init__"
Cohesion: 0.29
Nodes (3): _is_configured_key(), PolygonClient, validate_configuration()

## Knowledge Gaps
- **25 isolated node(s):** `Freshness check`, `Git hygiene`, `Navigating`, `Verify before asserting`, `Freshness check` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 199 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **20 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **What connects `Freshness check`, `Git hygiene`, `Navigating` to the rest of the system?**
  _25 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.06459627329192547 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Should `ImpliedMomentsEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.1383399209486166 - nodes in this community are weakly interconnected._
- **Why does `PortfolioOptimizer` connect `DataFrame` to `US Asset Manager.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05172413793103448 - nodes in this community are weakly interconnected._