# Graph Report - US-Asset-Allocation  (2026-10-06)

## Corpus Check
- 9 files · ~21,972 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 396 nodes · 867 edges · 21 communities (12 shown, 9 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `b4651ede`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FMPClient
- risk_estimators.py
- DataFrame
- US Asset Manager.py
- Any
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- test_risk_estimators.py
- BKMEstimator
- RiskFreeCurve
- AtomicWriteTests
- WeightTests
- run_pipeline
- Corp_FR_Optimization.py
- stage_scoring
- ImpliedMomentsEngine
- build_html_report
- stage_rating
- stage_fcf
- select_ratings
- CLAUDE.md

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 26 edges
2. `FMPClient` - 19 edges
3. `export_portfolio_json()` - 14 edges
4. `OptimizationResult` - 13 edges
5. `PortfolioOptimizer` - 13 edges
6. `ImpliedMomentsEngine` - 12 edges
7. `FMPClient` - 11 edges
8. `FactorModelBuilder` - 11 edges
9. `build_html_report()` - 11 edges
10. `export_universe_json()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `export_universe_json()` --calls--> `iso_bogota()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py
- `export_universe_json()` --calls--> `now_bogota()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py
- `export_universe_json()` --calls--> `stamp_bogota()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py
- `export_universe_json()` --calls--> `write_json_files()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py
- `export_portfolio_json()` --calls--> `iso_bogota()`  [EXTRACTED]
  US Asset Manager.py → pipeline_io.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (21 total, 9 thin omitted)

### Community 0 - "FMPClient"
Cohesion: 0.13
Nodes (6): FMPClient, _json_score(), _json_text(), _latest(), stage_solvency(), _to_float()

### Community 1 - "risk_estimators.py"
Cohesion: 0.06
Nodes (30): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cornish_fisher_es_gradient() (+22 more)

### Community 2 - "DataFrame"
Cohesion: 0.09
Nodes (15): ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, MarketDataLoader, _nearest_psd(), OptimizationError (+7 more)

### Community 3 - "US Asset Manager.py"
Cohesion: 0.08
Nodes (14): _clip(), _combine_scores(), configure_logging(), ETFDescriptor, FactorModelBuilder, _first_number(), _is_configured_key(), _json_float() (+6 more)

### Community 4 - "Any"
Cohesion: 0.16
Nodes (5): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, PolygonClient

### Community 5 - "pipeline_io.py"
Cohesion: 0.09
Nodes (12): export_universe_json(), atomic_write_json(), _atomic_write_text(), _dumps(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota() (+4 more)

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "test_risk_estimators.py"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 12 - "run_pipeline"
Cohesion: 0.24
Nodes (13): _abort_if_empty(), _banner(), _fmt_pct(), portfolio_summary(), print_curve(), print_funnel(), print_overlay(), print_ranking() (+5 more)

### Community 13 - "Corp_FR_Optimization.py"
Cohesion: 0.27
Nodes (4): build_risk_free_curve(), _check_keys(), _fred_last_value_fredapi(), _fred_last_value_requests()

### Community 14 - "stage_scoring"
Cohesion: 0.18
Nodes (5): cap_weights(), _rating_rank(), stage_scoring(), stage_weights(), zscore()

### Community 17 - "stage_rating"
Cohesion: 0.33
Nodes (3): rating_bucket(), stage_rating(), synthetic_rating()

## Knowledge Gaps
- **18 isolated node(s):** `graphify`, `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 122 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FMPClient` connect `Any` to `DataFrame`, `US Asset Manager.py`?**
  _High betweenness centrality (0.056) - this node is a cross-community bridge._
- **What connects `graphify`, `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FMPClient` be split into smaller, more focused modules?**
  _Cohesion score 0.13157894736842105 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.052) - this node is a cross-community bridge._
- **Should `risk_estimators.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05701754385964912 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.08735150244584207 - nodes in this community are weakly interconnected._