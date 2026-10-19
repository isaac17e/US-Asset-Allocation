# Graph Report - US-Asset-Allocation  (2026-10-18)

## Corpus Check
- 14 files · ~31,035 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 4, .bak-20261018 1)

## Summary
- 638 nodes · 1357 edges · 30 communities (18 shown, 12 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 28 edges (avg confidence: 0.91)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9ced2a8f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Corp_FR_Optimization.py
- numpy
- DataFrame
- Mean-variance optimization with factor targets
- BKMEstimator
- var_cvar_cornish_fisher
- FakeResponse
- ImpliedMomentsEngine
- check_risk_estimators_sync.py
- Any
- ._profile
- pipeline_io.py
- test_risk_estimators.py
- _tail_inputs
- cornish_fisher_params
- _load_manager
- US Asset Manager.py
- test_optimizer.py
- mock_patch
- RiskProfileTests
- MfikCapTests
- AtomicWriteTests
- cov_ewma_shrunk
- RawBetaTests
- ExportProfileTests
- TailPenaltySolveTests
- cornish_fisher_moments
- WeightTests
- sweep_tail_penalty.py
- mfik_cap_tenor

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
- `market_beta()` --implements--> `Market risk via beta band (market_beta, Blume shrinkage, raw beta for commodities)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `ImpliedTailModel` --implements--> `ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `resolve_risk_free_rate()` --implements--> `RISK_FREE_RATE override (resolve_risk_free_rate)`  [EXTRACTED]
  pipeline_io.py → README.md
- `resolve_risk_profile()` --implements--> `Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile)`  [EXTRACTED]
  pipeline_io.py → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (30 total, 12 thin omitted)

### Community 0 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (35): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), _figure() (+27 more)

### Community 1 - "numpy"
Cohesion: 0.11
Nodes (12): Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), ewma_cov(), ewma_weights(), martin_wagner_excess_return(), nearest_psd(), portfolio_moment_gradients(), portfolio_moments() (+4 more)

### Community 2 - "DataFrame"
Cohesion: 0.05
Nodes (21): beta_band_text(), beta_range_reachable(), BetaPoolFilter, ConsoleReporter, DashboardBuilder, ExpectedReturnModel, _historical_betas(), ImpliedCovarianceBuilder (+13 more)

### Community 3 - "Mean-variance optimization with factor targets"
Cohesion: 0.06
Nodes (36): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), Academic-use disclaimer (+28 more)

### Community 6 - "FakeResponse"
Cohesion: 0.17
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 7 - "ImpliedMomentsEngine"
Cohesion: 0.08
Nodes (8): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ResolveHorizonTests, _first_number(), ImpliedMomentsEngine, _to_float()

### Community 8 - "check_risk_estimators_sync.py"
Cohesion: 0.24
Nodes (5): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Manual risk_estimators.py sync with AM-PM (drift check), definitions(), main()

### Community 9 - "Any"
Cohesion: 0.06
Nodes (16): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), _clip(), _combine_scores(), ETFDescriptor (+8 more)

### Community 10 - "._profile"
Cohesion: 0.19
Nodes (3): FactorTargetTests, PortfolioConstraintTests, RiskProfileSelectionTests

### Community 11 - "pipeline_io.py"
Cohesion: 0.05
Nodes (23): export_universe_json(), atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), _horizon_from_source(), _horizon_number(), horizon_option_window() (+15 more)

### Community 12 - "test_risk_estimators.py"
Cohesion: 0.12
Nodes (6): _load_manager(), MassiveBaseTests, _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 13 - "_tail_inputs"
Cohesion: 0.19
Nodes (4): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailRiskReportTests

### Community 14 - "cornish_fisher_params"
Cohesion: 0.40
Nodes (4): cornish_fisher_domain(), cornish_fisher_params(), a_parametros(), residuo()

### Community 15 - "_load_manager"
Cohesion: 0.24
Nodes (3): ExportHorizonTests, _load_manager(), ManagerHorizonTests

### Community 17 - "test_optimizer.py"
Cohesion: 0.22
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

### Community 25 - "cov_ewma_shrunk"
Cohesion: 0.25
Nodes (4): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ledoit_wolf_constant_correlation()

### Community 29 - "cornish_fisher_moments"
Cohesion: 0.18
Nodes (6): cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_tail(), cornish_fisher_z(), higher_moments_admissible(), standardized_panel()

### Community 34 - "mfik_cap_tenor"
Cohesion: 0.40
Nodes (3): BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), mfik_cap(), mfik_cap_tenor()

## Knowledge Gaps
- **13 isolated node(s):** `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)`, `FRED API`, `Polygon.io options API` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 203 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **12 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `DataFrame` to `US Asset Manager.py`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **What connects `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.050140056022408966 - nodes in this community are weakly interconnected._
- **Why does `to_years()` connect `ImpliedMomentsEngine` to `numpy`, `var_cvar_cornish_fisher`, `pipeline_io.py`, `US Asset Manager.py`, `test_optimizer.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.11333333333333333 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `Mean-variance optimization with factor targets` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.032) - this node is a cross-community bridge._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.051061388410786 - nodes in this community are weakly interconnected._