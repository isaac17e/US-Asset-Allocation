# Graph Report - US-Asset-Allocation  (2026-10-14)

## Corpus Check
- 12 files · ~29,200 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 4)

## Summary
- 585 nodes · 1225 edges · 38 communities (21 shown, 17 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 11 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c5d1b85b`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DataFrame
- US Asset Manager.py
- ImpliedMomentsEngine
- Corp_FR_Optimization.py
- pandas
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- test_risk_estimators.py
- FakeResponse
- FMPClient
- RiskFreeCurve
- ._profile
- FactorModelBuilder
- beta_range_reachable
- math
- _tail_inputs
- BKMEstimator
- stage_scoring
- fmp_client.py
- UniverseBuilder
- stage_rating
- numpy
- build_html_report
- RiskProfileTests
- stage_solvency
- stage_fcf
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
3. `FMPClient` - 15 edges
4. `OptimizationResult` - 14 edges
5. `export_portfolio_json()` - 14 edges
6. `ImpliedMomentsEngine` - 13 edges
7. `build_html_report()` - 12 edges
8. `FakeResponse` - 12 edges
9. `FMPClient` - 11 edges
10. `scale_moments()` - 11 edges

## Surprising Connections (you probably didn't know these)
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `export_universe_json()` --calls--> `iso_bogota()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py
- `export_universe_json()` --calls--> `now_bogota()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py
- `export_universe_json()` --calls--> `stamp_bogota()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py
- `export_universe_json()` --calls--> `write_json_files()`  [EXTRACTED]
  Corp_FR_Optimization.py → pipeline_io.py

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (38 total, 17 thin omitted)

### Community 0 - "DataFrame"
Cohesion: 0.06
Nodes (19): ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, ImpliedTailModel, MarketDataLoader, _nearest_psd() (+11 more)

### Community 1 - "US Asset Manager.py"
Cohesion: 0.15
Nodes (5): configure_logging(), _is_configured_key(), main(), PipelineInputs, validate_configuration()

### Community 2 - "ImpliedMomentsEngine"
Cohesion: 0.14
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 3 - "Corp_FR_Optimization.py"
Cohesion: 0.26
Nodes (6): _abort_if_empty(), _check_keys(), print_funnel(), run_pipeline(), select_ratings(), _selected_ratings()

### Community 4 - "pandas"
Cohesion: 0.31
Nodes (9): _banner(), _fmt_pct(), _overlay_pivot(), portfolio_summary(), print_curve(), print_overlay(), print_ranking(), print_refinitiv_instructions() (+1 more)

### Community 5 - "pipeline_io.py"
Cohesion: 0.07
Nodes (15): export_universe_json(), atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), iso_bogota(), normalize_weights(), now_bogota() (+7 more)

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "test_risk_estimators.py"
Cohesion: 0.22
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 8 - "FakeResponse"
Cohesion: 0.11
Nodes (6): definitions(), main(), _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 10 - "RiskFreeCurve"
Cohesion: 0.18
Nodes (3): build_risk_free_curve(), RiskFreeCurve, stage_overlay()

### Community 11 - "._profile"
Cohesion: 0.19
Nodes (3): FactorTargetTests, PortfolioConstraintTests, RiskProfileSelectionTests

### Community 12 - "FactorModelBuilder"
Cohesion: 0.26
Nodes (4): _clip(), _combine_scores(), FactorModelBuilder, _percentile_score()

### Community 13 - "beta_range_reachable"
Cohesion: 0.20
Nodes (3): beta_band_text(), beta_range_reachable(), BetaPoolFilter

### Community 14 - "math"
Cohesion: 0.25
Nodes (5): resolve_risk_free_rate(), _first_number(), _json_float(), market_beta(), _to_float()

### Community 15 - "_tail_inputs"
Cohesion: 0.19
Nodes (4): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailRiskReportTests

### Community 17 - "stage_scoring"
Cohesion: 0.22
Nodes (4): cap_weights(), stage_scoring(), stage_weights(), zscore()

### Community 18 - "fmp_client.py"
Cohesion: 0.16
Nodes (5): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float()

### Community 20 - "stage_rating"
Cohesion: 0.25
Nodes (4): rating_bucket(), _rating_rank(), stage_rating(), synthetic_rating()

### Community 21 - "numpy"
Cohesion: 0.05
Nodes (34): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), average_correlation(), cornish_fisher_domain(), cornish_fisher_es_gradient() (+26 more)

### Community 24 - "stage_solvency"
Cohesion: 0.33
Nodes (3): _latest(), stage_solvency(), _to_float()

### Community 26 - "test_optimizer.py"
Cohesion: 0.22
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

## Knowledge Gaps
- **17 isolated node(s):** `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 192 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **17 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `DataFrame` to `US Asset Manager.py`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **What connects `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.055176890619928594 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `ImpliedMomentsEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.1383399209486166 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Should `pipeline_io.py` be split into smaller, more focused modules?**
  _Cohesion score 0.0700354609929078 - nodes in this community are weakly interconnected._