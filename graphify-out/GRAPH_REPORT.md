# Graph Report - US-Asset-Allocation  (2026-10-11)

## Corpus Check
- 14 files · ~29,195 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 561 nodes · 1252 edges · 21 communities (19 shown, 2 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 43 edges (avg confidence: 0.89)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8697bde5`
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
- .__init__
- sweep_tail_penalty.py
- test_optimizer.py
- ndarray
- cov_ewma_shrunk
- Any
- Working with the graphify knowledge graph
- risk_estimators.py
- Working with the graphify knowledge graph
- WeightTests

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
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `FMPClient` --uses--> `APIAuthorizationError`  [INFERRED]
  Corp_FR_Optimization.py → fmp_client.py
- `FMPClient` --uses--> `APIError`  [INFERRED]
  Corp_FR_Optimization.py → fmp_client.py
- `FactorModelBuilder` --uses--> `APIAuthorizationError`  [INFERRED]
  US Asset Manager.py → fmp_client.py
- `FactorModelBuilder` --uses--> `APIError`  [INFERRED]
  US Asset Manager.py → fmp_client.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (21 total, 2 thin omitted)

### Community 0 - "DataFrame"
Cohesion: 0.07
Nodes (17): beta_band_text(), BetaPoolFilter, _clip(), _combine_scores(), ConsoleReporter, DashboardBuilder, ExpectedReturnModel, FactorModelBuilder (+9 more)

### Community 1 - "cornish_fisher_params"
Cohesion: 0.40
Nodes (4): cornish_fisher_domain(), cornish_fisher_params(), a_parametros(), residuo()

### Community 2 - "ImpliedMomentsEngine"
Cohesion: 0.14
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 3 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (39): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), FMPClient (+31 more)

### Community 4 - "US Asset Manager.py"
Cohesion: 0.18
Nodes (4): configure_logging(), _is_configured_key(), main(), validate_configuration()

### Community 5 - "pipeline_io.py"
Cohesion: 0.06
Nodes (15): export_universe_json(), atomic_write_json(), _atomic_write_text(), _dumps(), iso_bogota(), normalize_weights(), now_bogota(), resolve_risk_free_rate() (+7 more)

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
Cohesion: 0.14
Nodes (7): ewma_cov(), ewma_weights(), martin_wagner_excess_return(), nearest_psd(), portfolio_moment_gradients(), q_to_p_correlation(), q_to_p_vol()

### Community 10 - "cornish_fisher_moments"
Cohesion: 0.22
Nodes (5): cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_tail(), cornish_fisher_z(), var_cvar_cornish_fisher()

### Community 12 - ".__init__"
Cohesion: 0.29
Nodes (3): higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 15 - "test_optimizer.py"
Cohesion: 0.06
Nodes (14): FactorTargetTests, HorizonAlignmentTests, MfikCapTests, mock_patch, mock_stub(), OneSidedPenaltyTests, PortfolioConstraintTests, _profile() (+6 more)

### Community 16 - "ndarray"
Cohesion: 0.08
Nodes (10): beta_range_reachable(), BKMEstimator, ImpliedTailModel, OptimizationError, PortfolioOptimizer, flip_delta(), violation(), objective() (+2 more)

### Community 17 - "cov_ewma_shrunk"
Cohesion: 0.25
Nodes (4): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ledoit_wolf_constant_correlation()

### Community 18 - "Any"
Cohesion: 0.08
Nodes (13): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), ETFDescriptor, _first_number(), FMPClient (+5 more)

### Community 20 - "Working with the graphify knowledge graph"
Cohesion: 0.33
Nodes (5): Freshness check, Git hygiene, Navigating, Verify before asserting, Working with the graphify knowledge graph

### Community 21 - "risk_estimators.py"
Cohesion: 0.14
Nodes (9): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), mfik_cap(), mfik_cap_tenor(), portfolio_moments() (+1 more)

### Community 25 - "Working with the graphify knowledge graph"
Cohesion: 0.33
Nodes (5): Freshness check, Git hygiene, Navigating, Verify before asserting, Working with the graphify knowledge graph

## Knowledge Gaps
- **17 isolated node(s):** `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 181 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **What connects `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.07213114754098361 - nodes in this community are weakly interconnected._
- **Why does `FMPClient` connect `Any` to `FakeResponse`, `Corp_FR_Optimization.py`, `US Asset Manager.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `ImpliedMomentsEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.1383399209486166 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05056179775280899 - nodes in this community are weakly interconnected._