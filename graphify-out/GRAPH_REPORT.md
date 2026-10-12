# Graph Report - US-Asset-Allocation  (2026-10-12)

## Corpus Check
- 12 files · ~29,750 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 4)

## Summary
- 579 nodes · 1256 edges · 29 communities (19 shown, 10 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d5fa3e7e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- DataFrame
- var_cvar_cornish_fisher
- ImpliedMomentsEngine
- Corp_FR_Optimization.py
- US Asset Manager.py
- pipeline_io.py
- IG corporate bond issuer screening pipeline (run_pipeline)
- _delta_referencia
- FakeResponse
- mfik_cap_tenor
- cornish_fisher_moments
- ._profile
- .__init__
- sweep_tail_penalty.py
- _tail_inputs
- ndarray
- numpy
- APIAuthorizationError
- risk_estimators.py
- test_optimizer.py
- Any
- WeightTests
- mock_patch
- MfikCapTests
- AtomicWriteTests
- RiskProfileTests
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
10. `FactorModelBuilder` - 12 edges

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

## Communities (29 total, 10 thin omitted)

### Community 0 - "DataFrame"
Cohesion: 0.08
Nodes (16): _combine_scores(), ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder, _is_configured_key(), market_beta() (+8 more)

### Community 2 - "ImpliedMomentsEngine"
Cohesion: 0.12
Nodes (6): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine, _to_float()

### Community 3 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (38): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), FMPClient (+30 more)

### Community 4 - "US Asset Manager.py"
Cohesion: 0.12
Nodes (3): portfolio_moment_gradients(), portfolio_moments(), q_to_p_vol()

### Community 5 - "pipeline_io.py"
Cohesion: 0.06
Nodes (18): export_universe_json(), atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), iso_bogota(), normalize_weights(), now_bogota() (+10 more)

### Community 6 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.07
Nodes (27): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer, EWMA correlation with Ledoit-Wolf shrinkage (+19 more)

### Community 7 - "_delta_referencia"
Cohesion: 0.26
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 8 - "FakeResponse"
Cohesion: 0.16
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 10 - "cornish_fisher_moments"
Cohesion: 0.18
Nodes (8): cornish_fisher_domain(), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params(), a_parametros(), residuo(), cornish_fisher_tail(), cornish_fisher_z()

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

### Community 16 - "ndarray"
Cohesion: 0.08
Nodes (9): beta_range_reachable(), BKMEstimator, ImpliedTailModel, OptimizationError, PortfolioOptimizer, flip_delta(), violation(), objective() (+1 more)

### Community 17 - "numpy"
Cohesion: 0.21
Nodes (6): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ewma_cov(), ewma_weights(), ledoit_wolf_constant_correlation()

### Community 18 - "APIAuthorizationError"
Cohesion: 0.14
Nodes (7): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), MarketDataLoader, PolygonClient

### Community 21 - "risk_estimators.py"
Cohesion: 0.13
Nodes (9): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Cornish-Fisher VaR/CVaR (Maillard 2012), Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), martin_wagner_excess_return(), nearest_psd(), q_to_p_correlation() (+1 more)

### Community 26 - "test_optimizer.py"
Cohesion: 0.20
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

### Community 28 - "Any"
Cohesion: 0.10
Nodes (9): beta_band_text(), BetaPoolFilter, _clip(), ETFDescriptor, FactorModelBuilder, _first_number(), FMPClient, _json_float() (+1 more)

## Knowledge Gaps
- **17 isolated node(s):** `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` (+12 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 183 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **10 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.036) - this node is a cross-community bridge._
- **What connects `AM-PM repository (source of risk_estimators copy)`, `Cornish-Fisher VaR/CVaR (Maillard 2012)`, `Portfolio skewness/kurtosis in O(J n) with analytical gradients` to the rest of the system?**
  _17 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.08081632653061224 - nodes in this community are weakly interconnected._
- **Why does `FMPClient` connect `APIAuthorizationError` to `FakeResponse`, `Corp_FR_Optimization.py`, `US Asset Manager.py`, `Any`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Should `ImpliedMomentsEngine` be split into smaller, more focused modules?**
  _Cohesion score 0.12333333333333334 - nodes in this community are weakly interconnected._
- **Why does `PassiveETFAllocationPipeline (ETF allocation pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `US Asset Manager.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05078855920876771 - nodes in this community are weakly interconnected._