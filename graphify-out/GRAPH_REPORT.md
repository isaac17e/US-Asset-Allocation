# Graph Report - US-Asset-Allocation  (2026-10-06)

## Corpus Check
- Corpus is ~21,824 words - fits in a single context window. You may not need a graph.

## Summary
- 394 nodes · 866 edges · 12 communities (8 shown, 4 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 8 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- API Clients & Corp FR Optimization
- Risk Estimators & Cornish-Fisher
- ETF Asset Manager
- Fundamentals & Candidate Universe
- Data Fetch & Backoff
- Pipeline IO Tests
- README: Pipeline Concepts
- Ledoit-Wolf EWMA Tests
- American Option Pricing
- Risk-Free Curve
- Atomic Write Tests
- Weight Rounding Tests

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 26 edges
2. `FMPClient` - 19 edges
3. `export_portfolio_json()` - 14 edges
4. `OptimizationResult` - 13 edges
5. `PortfolioOptimizer` - 13 edges
6. `ImpliedMomentsEngine` - 12 edges
7. `FMPClient` - 11 edges
8. `build_html_report()` - 11 edges
9. `export_universe_json()` - 11 edges
10. `FactorModelBuilder` - 11 edges

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
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (12 total, 4 thin omitted)

### Community 0 - "API Clients & Corp FR Optimization"
Cohesion: 0.06
Nodes (37): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), FMPClient (+29 more)

### Community 1 - "Risk Estimators & Cornish-Fisher"
Cohesion: 0.06
Nodes (30): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cornish_fisher_es_gradient() (+22 more)

### Community 2 - "ETF Asset Manager"
Cohesion: 0.09
Nodes (15): ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, MarketDataLoader, _nearest_psd(), OptimizationError (+7 more)

### Community 3 - "Fundamentals & Candidate Universe"
Cohesion: 0.08
Nodes (13): _clip(), _combine_scores(), configure_logging(), ETFDescriptor, FactorModelBuilder, _first_number(), _is_configured_key(), _json_float() (+5 more)

### Community 4 - "Data Fetch & Backoff"
Cohesion: 0.11
Nodes (7): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, ImpliedMomentsEngine, PolygonClient, _to_float()

### Community 5 - "Pipeline IO Tests"
Cohesion: 0.09
Nodes (12): export_universe_json(), atomic_write_json(), _atomic_write_text(), _dumps(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota() (+4 more)

### Community 6 - "README: Pipeline Concepts"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "Ledoit-Wolf EWMA Tests"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

## Knowledge Gaps
- **17 isolated node(s):** `Bjerksund-Stensland American option model`, `Expected return mu (75% CAPM, 25% historical)`, `Investment profiles (Conservador, Crecimiento, Momentum/Agresivo)`, `Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing`, `Linear program for factor target feasibility and relaxation` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 120 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FMPClient` connect `Data Fetch & Backoff` to `ETF Asset Manager`, `Fundamentals & Candidate Universe`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **What connects `Bjerksund-Stensland American option model`, `Expected return mu (75% CAPM, 25% historical)`, `Investment profiles (Conservador, Crecimiento, Momentum/Agresivo)` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `API Clients & Corp FR Optimization` be split into smaller, more focused modules?**
  _Cohesion score 0.05540499849442939 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `README: Pipeline Concepts` to `API Clients & Corp FR Optimization`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Should `Risk Estimators & Cornish-Fisher` be split into smaller, more focused modules?**
  _Cohesion score 0.05701754385964912 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `README: Pipeline Concepts` to `Fundamentals & Candidate Universe`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Should `ETF Asset Manager` be split into smaller, more focused modules?**
  _Cohesion score 0.09125188536953242 - nodes in this community are weakly interconnected._