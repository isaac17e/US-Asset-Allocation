# Graph Report - US-Asset-Allocation  (2026-10-14)

## Corpus Check
- 12 files · ~29,200 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 4)

## Summary
- 579 nodes · 1240 edges · 21 communities (14 shown, 7 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 26 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3840471c`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DataFrame
- ImpliedMomentsEngine
- Corp_FR_Optimization.py
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- test_risk_estimators.py
- FakeResponse
- ._profile
- _tail_inputs
- ndarray
- US Asset Manager.py
- numpy
- test_optimizer.py
- Any
- WeightTests
- mock_patch
- MfikCapTests
- AtomicWriteTests
- RawBetaTests
- ExportProfileTests
- TailPenaltySolveTests

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

## Communities (21 total, 7 thin omitted)

### Community 0 - "DataFrame"
Cohesion: 0.07
Nodes (16): var_cvar_cornish_fisher(), _combine_scores(), ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, market_beta() (+8 more)

### Community 2 - "ImpliedMomentsEngine"
Cohesion: 0.13
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 3 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (35): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), _figure() (+27 more)

### Community 5 - "pipeline_io.py"
Cohesion: 0.05
Nodes (20): export_universe_json(), atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), iso_bogota(), normalize_weights(), now_bogota() (+12 more)

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "test_risk_estimators.py"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 8 - "FakeResponse"
Cohesion: 0.11
Nodes (6): definitions(), main(), _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 11 - "._profile"
Cohesion: 0.19
Nodes (3): FactorTargetTests, PortfolioConstraintTests, RiskProfileSelectionTests

### Community 15 - "_tail_inputs"
Cohesion: 0.19
Nodes (4): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailRiskReportTests

### Community 16 - "ndarray"
Cohesion: 0.08
Nodes (9): beta_range_reachable(), BKMEstimator, ImpliedTailModel, OptimizationError, PortfolioOptimizer, flip_delta(), violation(), objective() (+1 more)

### Community 18 - "US Asset Manager.py"
Cohesion: 0.09
Nodes (11): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), configure_logging(), _is_configured_key(), main() (+3 more)

### Community 21 - "numpy"
Cohesion: 0.05
Nodes (33): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cornish_fisher_es_gradient() (+25 more)

### Community 26 - "test_optimizer.py"
Cohesion: 0.22
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

### Community 28 - "Any"
Cohesion: 0.10
Nodes (7): beta_band_text(), BetaPoolFilter, ETFDescriptor, FactorModelBuilder, _first_number(), FMPClient, UniverseBuilder

## Knowledge Gaps
- **17 isolated node(s):** `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 186 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `ndarray` to `DataFrame`, `US Asset Manager.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **What connects `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.07329462989840348 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **Should `ImpliedMomentsEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.13043478260869565 - nodes in this community are weakly interconnected._
- **Why does `FMPClient` connect `US Asset Manager.py` to `FakeResponse`, `Corp_FR_Optimization.py`, `Any`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.050774526678141134 - nodes in this community are weakly interconnected._