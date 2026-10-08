# Graph Report - US-Asset-Allocation  (2026-10-08)

## Corpus Check
- 14 files · ~27,583 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 548 nodes · 1164 edges · 32 communities (22 shown, 10 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 12 edges (avg confidence: 0.88)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ce83ab72`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DataFrame
- fmp_client.py
- ImpliedMomentsEngine
- run_pipeline
- US Asset Manager.py
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- test_risk_estimators.py
- FakeResponse
- numpy
- cornish_fisher_moments
- RiskFreeCurve
- .__init__
- Corp_FR_Optimization.py
- sweep_tail_penalty.py
- test_optimizer.py
- var_cvar_cornish_fisher
- cov_ewma_shrunk
- Any
- stage_scoring
- Working with the graphify knowledge graph
- risk_estimators.py
- math
- FMPClient
- build_html_report
- Working with the graphify knowledge graph
- stage_rating
- select_ratings
- AtomicWriteTests
- WeightTests

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 26 edges
2. `FMPClient` - 15 edges
3. `OptimizationResult` - 14 edges
4. `PortfolioOptimizer` - 14 edges
5. `export_portfolio_json()` - 14 edges
6. `ImpliedMomentsEngine` - 13 edges
7. `FMPClient` - 13 edges
8. `FakeResponse` - 12 edges
9. `FactorModelBuilder` - 11 edges
10. `build_html_report()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `FMPClient` --calls--> `_client()`  [EXTRACTED]
  fmp_client.py → tests/test_fmp_client.py
- `APIAuthorizationError` --uses--> `FMPClient`  [INFERRED]
  fmp_client.py → Corp_FR_Optimization.py
- `APIError` --uses--> `FMPClient`  [INFERRED]
  fmp_client.py → Corp_FR_Optimization.py
- `FMPClient` --inherits--> `FMPClient`  [EXTRACTED]
  fmp_client.py → Corp_FR_Optimization.py
- `export_portfolio_json()` --calls--> `iso_bogota()`  [EXTRACTED]
  US Asset Manager.py → pipeline_io.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (32 total, 10 thin omitted)

### Community 0 - "DataFrame"
Cohesion: 0.06
Nodes (20): BKMEstimator, _combine_scores(), ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, ImpliedTailModel (+12 more)

### Community 1 - "fmp_client.py"
Cohesion: 0.16
Nodes (5): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float()

### Community 2 - "ImpliedMomentsEngine"
Cohesion: 0.14
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 3 - "run_pipeline"
Cohesion: 0.29
Nodes (11): _banner(), _fmt_pct(), portfolio_summary(), print_curve(), print_overlay(), print_ranking(), print_refinitiv_instructions(), print_weights() (+3 more)

### Community 4 - "US Asset Manager.py"
Cohesion: 0.18
Nodes (4): configure_logging(), _is_configured_key(), main(), validate_configuration()

### Community 5 - "pipeline_io.py"
Cohesion: 0.07
Nodes (14): export_universe_json(), atomic_write_json(), _atomic_write_text(), _dumps(), iso_bogota(), normalize_weights(), now_bogota(), resolve_risk_free_rate() (+6 more)

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "test_risk_estimators.py"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 8 - "FakeResponse"
Cohesion: 0.11
Nodes (6): definitions(), main(), _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 9 - "numpy"
Cohesion: 0.17
Nodes (6): martin_wagner_excess_return(), mfik_cap(), mfik_cap_tenor(), portfolio_moments(), q_to_p_correlation(), q_to_p_vol()

### Community 10 - "cornish_fisher_moments"
Cohesion: 0.18
Nodes (8): cornish_fisher_domain(), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params(), a_parametros(), residuo(), cornish_fisher_tail(), cornish_fisher_z()

### Community 12 - ".__init__"
Cohesion: 0.29
Nodes (3): higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 13 - "Corp_FR_Optimization.py"
Cohesion: 0.22
Nodes (6): _abort_if_empty(), build_risk_free_curve(), _check_keys(), _fred_last_value_fredapi(), _fred_last_value_requests(), print_funnel()

### Community 15 - "test_optimizer.py"
Cohesion: 0.06
Nodes (14): FactorTargetTests, HorizonAlignmentTests, MfikCapTests, mock_patch, mock_stub(), OneSidedPenaltyTests, PortfolioConstraintTests, _profile() (+6 more)

### Community 17 - "cov_ewma_shrunk"
Cohesion: 0.25
Nodes (4): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ledoit_wolf_constant_correlation()

### Community 18 - "Any"
Cohesion: 0.09
Nodes (11): _clip(), ETFDescriptor, FactorModelBuilder, _first_number(), FMPClient, _json_float(), MarketDataLoader, PipelineInputs (+3 more)

### Community 19 - "stage_scoring"
Cohesion: 0.18
Nodes (5): cap_weights(), _rating_rank(), stage_scoring(), stage_weights(), zscore()

### Community 20 - "Working with the graphify knowledge graph"
Cohesion: 0.33
Nodes (5): Freshness check, Git hygiene, Navigating, Verify before asserting, Working with the graphify knowledge graph

### Community 21 - "risk_estimators.py"
Cohesion: 0.12
Nodes (10): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), ewma_cov(), ewma_weights(), nearest_psd() (+2 more)

### Community 22 - "math"
Cohesion: 0.20
Nodes (6): fcf_metrics(), _json_score(), _latest(), stage_fcf(), stage_solvency(), _to_float()

### Community 25 - "Working with the graphify knowledge graph"
Cohesion: 0.33
Nodes (5): Freshness check, Git hygiene, Navigating, Verify before asserting, Working with the graphify knowledge graph

### Community 26 - "stage_rating"
Cohesion: 0.33
Nodes (3): rating_bucket(), stage_rating(), synthetic_rating()

## Knowledge Gaps
- **25 isolated node(s):** `Freshness check`, `Git hygiene`, `Navigating`, `Verify before asserting`, `Freshness check` (+20 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 179 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **What connects `Freshness check`, `Git hygiene`, `Navigating` to the rest of the system?**
  _25 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.055379746835443035 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `ImpliedMomentsEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.1383399209486166 - nodes in this community are weakly interconnected._
- **Why does `FMPClient` connect `fmp_client.py` to `FakeResponse`, `US Asset Manager.py`, `Corp_FR_Optimization.py`, `FMPClient`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `pipeline_io.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07373737373737374 - nodes in this community are weakly interconnected._