# Graph Report - US-Asset-Allocation  (2026-10-07)

## Corpus Check
- 13 files · ~26,077 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 512 nodes · 1132 edges · 19 communities (16 shown, 3 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ae131301`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- ndarray
- scale_moments
- DataFrame
- Any
- US Asset Manager.py
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- cornish_fisher_moments
- FakeResponse
- risk_estimators.py
- cov_ewma_shrunk
- WeightTests
- .__init__
- Corp_FR_Optimization.py
- sweep_tail_penalty.py
- test_optimizer.py
- cornish_fisher_params
- CLAUDE.md
- numpy

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 26 edges
2. `FMPClient` - 16 edges
3. `APIError` - 16 edges
4. `APIAuthorizationError` - 16 edges
5. `ImpliedMomentsEngine` - 15 edges
6. `OptimizationResult` - 14 edges
7. `PortfolioOptimizer` - 14 edges
8. `export_portfolio_json()` - 14 edges
9. `FMPClient` - 13 edges
10. `FactorModelBuilder` - 13 edges

## Surprising Connections (you probably didn't know these)
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `FMPClient` --uses--> `APIAuthorizationError`  [INFERRED]
  Corp_FR_Optimization.py → fmp_client.py
- `FMPClient` --uses--> `APIError`  [INFERRED]
  Corp_FR_Optimization.py → fmp_client.py
- `FMPClient` --uses--> `APIAuthorizationError`  [INFERRED]
  US Asset Manager.py → fmp_client.py
- `UniverseBuilder` --uses--> `APIAuthorizationError`  [INFERRED]
  US Asset Manager.py → fmp_client.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (19 total, 3 thin omitted)

### Community 0 - "ndarray"
Cohesion: 0.07
Nodes (12): portfolio_moment_gradients(), q_to_p_vol(), BKMEstimator, ImpliedCovarianceBuilder, ImpliedTailModel, _nearest_psd(), OptimizationError, PortfolioOptimizer (+4 more)

### Community 1 - "scale_moments"
Cohesion: 0.22
Nodes (4): annualize(), scale_bkm_moments(), scale_moments(), to_years()

### Community 2 - "DataFrame"
Cohesion: 0.08
Nodes (14): _clip(), _combine_scores(), ConsoleReporter, DashboardBuilder, ExpectedReturnModel, FactorModelBuilder, _historical_betas(), OptimizationResult (+6 more)

### Community 3 - "Any"
Cohesion: 0.10
Nodes (6): ETFDescriptor, _first_number(), FMPClient, ImpliedMomentsEngine, _to_float(), UniverseBuilder

### Community 4 - "US Asset Manager.py"
Cohesion: 0.10
Nodes (11): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), configure_logging(), _is_configured_key(), main() (+3 more)

### Community 5 - "pipeline_io.py"
Cohesion: 0.07
Nodes (13): atomic_write_json(), _atomic_write_text(), _dumps(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), _warn() (+5 more)

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "cornish_fisher_moments"
Cohesion: 0.22
Nodes (5): cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_tail(), cornish_fisher_z(), var_cvar_cornish_fisher()

### Community 8 - "FakeResponse"
Cohesion: 0.07
Nodes (10): definitions(), main(), _client(), CorpTolerantClientTests, FakeResponse, TransportTests, _delta_referencia(), LedoitWolfEwmaTests (+2 more)

### Community 9 - "risk_estimators.py"
Cohesion: 0.22
Nodes (6): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), scale_cov()

### Community 10 - "cov_ewma_shrunk"
Cohesion: 0.25
Nodes (4): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ledoit_wolf_constant_correlation()

### Community 12 - ".__init__"
Cohesion: 0.29
Nodes (3): higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 13 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (39): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), export_universe_json(), fcf_metrics() (+31 more)

### Community 15 - "test_optimizer.py"
Cohesion: 0.07
Nodes (11): FactorTargetTests, HorizonAlignmentTests, mock_patch, PortfolioConstraintTests, _profile(), RiskContributionTests, _synthetic_inputs(), _tail_inputs() (+3 more)

### Community 16 - "cornish_fisher_params"
Cohesion: 0.40
Nodes (4): cornish_fisher_domain(), cornish_fisher_params(), a_parametros(), residuo()

### Community 21 - "numpy"
Cohesion: 0.17
Nodes (6): ewma_cov(), ewma_weights(), martin_wagner_excess_return(), nearest_psd(), portfolio_moments(), q_to_p_correlation()

## Knowledge Gaps
- **18 isolated node(s):** `graphify`, `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 158 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FMPClient` connect `US Asset Manager.py` to `FakeResponse`, `Any`, `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **What connects `graphify`, `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `ndarray` be split into smaller, more focused modules?**
  _Cohesion score 0.07397959183673469 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.08078431372549019 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Should `Any` be split into smaller, more focused modules?**
  _Cohesion score 0.09815078236130868 - nodes in this community are weakly interconnected._