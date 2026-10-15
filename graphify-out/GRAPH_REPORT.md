# Graph Report - US-Asset-Allocation  (2026-10-15)

## Corpus Check
- 13 files · ~30,712 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 4)

## Summary
- 638 nodes · 1329 edges · 40 communities (22 shown, 18 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 14 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `da109897`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Corp_FR_Optimization.py
- numpy
- DataFrame
- IG corporate bond issuer screening pipeline (run_pipeline)
- .cover_band
- US Asset Manager.py
- test_horizon.py
- ImpliedMomentsEngine
- fmp_client.py
- Any
- ._profile
- pipeline_io.py
- test_risk_estimators.py
- _tail_inputs
- cornish_fisher_moments
- Mean-variance optimization with factor targets
- test_optimizer.py
- mock_patch
- Bakshi-Kapadia-Madan (BKM) model-free implied moments
- UniverseBuilder
- FactorModelBuilder
- .prepare
- MfikCapTests
- AtomicWriteTests
- cov_ewma_shrunk
- RawBetaTests
- ExportProfileTests
- TailPenaltySolveTests
- .__init__
- WeightTests
- sweep_tail_penalty.py
- .__init__
- mfik_cap_tenor

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 26 edges
2. `PortfolioOptimizer` - 17 edges
3. `FMPClient` - 15 edges
4. `OptimizationResult` - 14 edges
5. `export_portfolio_json()` - 14 edges
6. `ImpliedMomentsEngine` - 13 edges
7. `FMPClient` - 13 edges
8. `ResolveHorizonTests` - 12 edges
9. `FakeResponse` - 12 edges
10. `build_html_report()` - 12 edges

## Surprising Connections (you probably didn't know these)
- `market_beta()` --implements--> `Market risk via beta band (market_beta, Blume shrinkage, raw beta for commodities)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `ImpliedTailModel` --implements--> `ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `resolve_risk_profile()` --implements--> `Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile)`  [EXTRACTED]
  pipeline_io.py → README.md
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `mfik_cap_tenor()` --implements--> `BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor)`  [EXTRACTED]
  risk_estimators.py → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (40 total, 18 thin omitted)

### Community 0 - "Corp_FR_Optimization.py"
Cohesion: 0.05
Nodes (35): _abort_if_empty(), _banner(), build_html_report(), build_risk_free_curve(), cap_weights(), _check_keys(), fcf_metrics(), _figure() (+27 more)

### Community 1 - "numpy"
Cohesion: 0.12
Nodes (11): Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), ewma_cov(), ewma_weights(), martin_wagner_excess_return(), nearest_psd(), portfolio_moment_gradients(), portfolio_moments() (+3 more)

### Community 2 - "DataFrame"
Cohesion: 0.06
Nodes (17): var_cvar_cornish_fisher(), beta_range_reachable(), ConsoleReporter, DashboardBuilder, ImpliedCovarianceBuilder, ImpliedTailModel, _nearest_psd(), OptimizationError (+9 more)

### Community 3 - "IG corporate bond issuer screening pipeline (run_pipeline)"
Cohesion: 0.09
Nodes (21): resolve_risk_free_rate(), Composite Credit Score, IG corporate bond issuer screening pipeline (run_pipeline), Academic-use disclaimer, Expected return mu (75% CAPM, 25% historical), Factor loading matrix B (Value, Growth, Momentum, Quality), Free cash flow screen (increasing or CAGR > 3%), Financial Modeling Prep (FMP) API (+13 more)

### Community 5 - "US Asset Manager.py"
Cohesion: 0.13
Nodes (7): configure_logging(), ExpectedReturnModel, _first_number(), _historical_betas(), _json_float(), main(), _to_float()

### Community 6 - "test_horizon.py"
Cohesion: 0.08
Nodes (8): _client(), CorpTolerantClientTests, FakeResponse, TransportTests, ExportHorizonTests, _load_manager(), ManagerHorizonTests, OptionWindowTests

### Community 7 - "ImpliedMomentsEngine"
Cohesion: 0.07
Nodes (7): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ResolveHorizonTests, BKMEstimator, ImpliedMomentsEngine

### Community 8 - "fmp_client.py"
Cohesion: 0.09
Nodes (10): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Manual risk_estimators.py sync with AM-PM (drift check) (+2 more)

### Community 10 - "._profile"
Cohesion: 0.19
Nodes (3): FactorTargetTests, PortfolioConstraintTests, RiskProfileSelectionTests

### Community 11 - "pipeline_io.py"
Cohesion: 0.05
Nodes (21): export_universe_json(), atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), _horizon_from_source(), _horizon_number(), horizon_option_window() (+13 more)

### Community 12 - "test_risk_estimators.py"
Cohesion: 0.24
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 13 - "_tail_inputs"
Cohesion: 0.19
Nodes (4): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailRiskReportTests

### Community 14 - "cornish_fisher_moments"
Cohesion: 0.18
Nodes (8): cornish_fisher_domain(), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params(), a_parametros(), residuo(), cornish_fisher_tail(), cornish_fisher_z()

### Community 15 - "Mean-variance optimization with factor targets"
Cohesion: 0.22
Nodes (8): Cornish-Fisher VaR/CVaR (Maillard 2012), Investment profiles (Conservador, Crecimiento, Momentum/Agresivo), Mean-variance optimization with factor targets, Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile), Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing, Tail penalty (USE_TAIL_PENALTY, one-sided ES_CF - ES_Gaussian, SLSQP), Final portfolio tail-risk measure (Gaussian vs Cornish-Fisher VaR/CVaR), Linear program for factor target feasibility and relaxation

### Community 17 - "test_optimizer.py"
Cohesion: 0.22
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

### Community 19 - "Bakshi-Kapadia-Madan (BKM) model-free implied moments"
Cohesion: 0.25
Nodes (7): Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD), EWMA correlation with Ledoit-Wolf shrinkage, ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula), Polygon.io options API

### Community 21 - "FactorModelBuilder"
Cohesion: 0.26
Nodes (4): _clip(), _combine_scores(), FactorModelBuilder, _percentile_score()

### Community 22 - ".prepare"
Cohesion: 0.17
Nodes (4): market_beta(), MarketDataLoader, PipelineInputs, RedundancyFilter

### Community 25 - "cov_ewma_shrunk"
Cohesion: 0.25
Nodes (4): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ledoit_wolf_constant_correlation()

### Community 29 - ".__init__"
Cohesion: 0.29
Nodes (3): higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 32 - ".__init__"
Cohesion: 0.29
Nodes (3): _is_configured_key(), PolygonClient, validate_configuration()

### Community 34 - "mfik_cap_tenor"
Cohesion: 0.40
Nodes (3): BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), mfik_cap(), mfik_cap_tenor()

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 209 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `DataFrame` to `US Asset Manager.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Corp_FR_Optimization.py` be split into smaller, more focused modules?**
  _Cohesion score 0.050140056022408966 - nodes in this community are weakly interconnected._
- **Why does `to_years()` connect `ImpliedMomentsEngine` to `numpy`, `DataFrame`, `US Asset Manager.py`, `test_horizon.py`, `test_optimizer.py`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Should `numpy` be split into smaller, more focused modules?**
  _Cohesion score 0.1225296442687747 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `IG corporate bond issuer screening pipeline (run_pipeline)` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **Should `DataFrame` be split into smaller, more focused modules?**
  _Cohesion score 0.06103286384976526 - nodes in this community are weakly interconnected._