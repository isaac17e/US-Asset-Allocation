# Graph Report - US-Asset-Allocation  (2026-10-07)

## Corpus Check
- 13 files · ~26,077 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 3 file(s) not represented in the graph (top: (none) 3)

## Summary
- 513 nodes · 1132 edges · 26 communities (20 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `221de39f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DataFrame
- fmp_client.py
- FactorModelBuilder
- ImpliedMomentsEngine
- US Asset Manager.py
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- test_risk_estimators.py
- FakeResponse
- .prepare
- FMPClient
- WeightTests
- APIAuthorizationError
- run_pipeline
- Corp_FR_Optimization.py
- test_optimizer.py
- RiskFreeCurve
- Any
- stage_fcf
- BKMEstimator
- CLAUDE.md
- numpy
- stage_scoring
- stage_rating
- select_ratings

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

## Communities (26 total, 6 thin omitted)

### Community 0 - "DataFrame"
Cohesion: 0.07
Nodes (16): var_cvar_cornish_fisher(), ConsoleReporter, DashboardBuilder, ImpliedCovarianceBuilder, ImpliedTailModel, _nearest_psd(), OptimizationError, OptimizationResult (+8 more)

### Community 1 - "fmp_client.py"
Cohesion: 0.25
Nodes (3): BaseHTTPClient, FMPClient, _to_float()

### Community 2 - "FactorModelBuilder"
Cohesion: 0.26
Nodes (4): _combine_scores(), FactorModelBuilder, _first_number(), _percentile_score()

### Community 3 - "ImpliedMomentsEngine"
Cohesion: 0.14
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 4 - "US Asset Manager.py"
Cohesion: 0.11
Nodes (10): _fred_last_value_requests(), _clip(), configure_logging(), ExpectedReturnModel, _historical_betas(), _is_configured_key(), _json_float(), main() (+2 more)

### Community 5 - "pipeline_io.py"
Cohesion: 0.07
Nodes (12): atomic_write_json(), _atomic_write_text(), _dumps(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), _warn() (+4 more)

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "test_risk_estimators.py"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 8 - "FakeResponse"
Cohesion: 0.11
Nodes (6): definitions(), main(), _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 9 - ".prepare"
Cohesion: 0.21
Nodes (4): ETFDescriptor, PipelineInputs, RedundancyFilter, UniverseBuilder

### Community 10 - "FMPClient"
Cohesion: 0.19
Nodes (4): export_universe_json(), FMPClient, _json_score(), _json_text()

### Community 12 - "APIAuthorizationError"
Cohesion: 0.19
Nodes (4): APIAuthorizationError, APIError, MarketDataLoader, PolygonClient

### Community 13 - "run_pipeline"
Cohesion: 0.25
Nodes (12): _abort_if_empty(), _banner(), _fmt_pct(), portfolio_summary(), print_funnel(), print_overlay(), print_ranking(), print_refinitiv_instructions() (+4 more)

### Community 14 - "Corp_FR_Optimization.py"
Cohesion: 0.23
Nodes (3): build_html_report(), _check_keys(), _json_safe()

### Community 15 - "test_optimizer.py"
Cohesion: 0.07
Nodes (11): FactorTargetTests, HorizonAlignmentTests, mock_patch, PortfolioConstraintTests, _profile(), RiskContributionTests, _synthetic_inputs(), _tail_inputs() (+3 more)

### Community 16 - "RiskFreeCurve"
Cohesion: 0.18
Nodes (4): build_risk_free_curve(), _fred_last_value_fredapi(), print_curve(), RiskFreeCurve

### Community 18 - "stage_fcf"
Cohesion: 0.20
Nodes (5): fcf_metrics(), _latest(), stage_fcf(), stage_solvency(), _to_float()

### Community 21 - "numpy"
Cohesion: 0.05
Nodes (31): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cornish_fisher_es_gradient() (+23 more)

### Community 22 - "stage_scoring"
Cohesion: 0.22
Nodes (4): cap_weights(), stage_scoring(), stage_weights(), zscore()

### Community 23 - "stage_rating"
Cohesion: 0.25
Nodes (4): rating_bucket(), _rating_rank(), stage_rating(), synthetic_rating()

## Knowledge Gaps
- **18 isolated node(s):** `graphify`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Expected return mu (75% CAPM, 25% historical)`, `Free cash flow screen (increasing or CAGR > 3%)` (+13 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 159 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FMPClient` connect `fmp_client.py` to `US Asset Manager.py`, `FakeResponse`, `FMPClient`, `Corp_FR_Optimization.py`, `Any`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **What connects `graphify`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer` to the rest of the system?**
  _18 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.07219662058371736 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Should `ImpliedMomentsEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.1383399209486166 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Should `US Asset Manager.py` be split into smaller, more focused modules?**
  _Cohesion score 0.11384615384615385 - nodes in this community are weakly interconnected._