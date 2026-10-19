# Graph Report - US-Asset-Allocation  (2026-10-19)

## Corpus Check
- 20 files · ~33,856 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 5 file(s) not represented in the graph (top: (none) 4, .bak-20261018 1)

## Summary
- 720 nodes · 1509 edges · 48 communities (32 shown, 16 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 31 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `79f5a01f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Corp_FR_Optimization.py
- risk_estimators.py
- PortfolioOptimizer
- Mean-variance optimization with factor targets
- ndarray
- test_html_reports_browser.py
- FakeResponse
- ImpliedMomentsEngine
- check_risk_estimators_sync.py
- US Asset Manager.py
- ._profile
- pipeline_io.py
- _delta_referencia
- _tail_inputs
- pathlib
- test_horizon.py
- math
- test_optimizer.py
- mock_patch
- FMPClient
- numpy
- DataFrame
- OptimizationResult
- cornish_fisher_moments
- AtomicWriteTests
- beta_range_reachable
- RawBetaTests
- RiskFreeCurve
- Series
- report_pdf.py
- browser_test_helpers.py
- stage_scoring
- cov_ewma_shrunk
- DataFrame
- stage_rating
- build_html_report
- .__init__
- MfikCapTests
- ReportPdfUnitTests
- sweep_tail_penalty.py
- var_cvar_cornish_fisher
- mfik_cap_tenor
- ExportProfileTests
- TailPenaltySolveTests
- stage_fcf
- ewma_cov
- ._solve_qubo_sa
- _QuietHandler

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 27 edges
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
- `resolve_risk_profile()` --implements--> `Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile)`  [EXTRACTED]
  pipeline_io.py → README.md
- `mfik_cap_tenor()` --implements--> `BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor)`  [EXTRACTED]
  risk_estimators.py → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (48 total, 16 thin omitted)

### Community 0 - "Corp_FR_Optimization.py"
Cohesion: 0.27
Nodes (11): _abort_if_empty(), _banner(), _check_keys(), _fmt_pct(), portfolio_summary(), print_curve(), print_funnel(), print_overlay() (+3 more)

### Community 1 - "risk_estimators.py"
Cohesion: 0.14
Nodes (7): Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), martin_wagner_excess_return(), portfolio_moments(), q_to_p_correlation(), q_to_p_vol(), scale_cov()

### Community 2 - "PortfolioOptimizer"
Cohesion: 0.18
Nodes (3): OptimizationError, PortfolioOptimizer, objective()

### Community 3 - "Mean-variance optimization with factor targets"
Cohesion: 0.06
Nodes (36): resolve_risk_free_rate(), Bjerksund-Stensland American option model, Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D, cov_ewma_shrunk (EWMA, Kish ESS, Ledoit-Wolf, nearest PSD) (+28 more)

### Community 4 - "ndarray"
Cohesion: 0.22
Nodes (3): portfolio_moment_gradients(), BKMEstimator, ImpliedTailModel

### Community 5 - "test_html_reports_browser.py"
Cohesion: 0.17
Nodes (7): wait_for_plotly(), AllocationDashboardTests, CorpFixedIncomeHTMLTests, CorpFixedIncomeReportTests, OfflineBrowserTestCase, _synthetic_corporate_inputs(), _write_corporate_report()

### Community 6 - "FakeResponse"
Cohesion: 0.10
Nodes (6): _client(), CorpTolerantClientTests, FakeResponse, TransportTests, _load_manager(), MassiveBaseTests

### Community 7 - "ImpliedMomentsEngine"
Cohesion: 0.12
Nodes (5): annualize(), scale_bkm_moments(), scale_moments(), to_years(), ImpliedMomentsEngine

### Community 8 - "check_risk_estimators_sync.py"
Cohesion: 0.24
Nodes (5): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Manual risk_estimators.py sync with AM-PM (drift check), definitions(), main()

### Community 9 - "US Asset Manager.py"
Cohesion: 0.05
Nodes (21): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), _clip(), _combine_scores(), configure_logging() (+13 more)

### Community 10 - "._profile"
Cohesion: 0.19
Nodes (3): FactorTargetTests, PortfolioConstraintTests, RiskProfileSelectionTests

### Community 11 - "pipeline_io.py"
Cohesion: 0.05
Nodes (20): atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), _horizon_from_source(), _horizon_number(), iso_bogota(), months_to_days() (+12 more)

### Community 12 - "_delta_referencia"
Cohesion: 0.26
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 13 - "_tail_inputs"
Cohesion: 0.19
Nodes (4): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailRiskReportTests

### Community 14 - "pathlib"
Cohesion: 0.21
Nodes (3): launch_browser(), load_playwright(), ReportPdfBrowserTests

### Community 15 - "test_horizon.py"
Cohesion: 0.09
Nodes (5): ExportHorizonTests, _load_manager(), ManagerHorizonTests, OptionWindowTests, ResolveHorizonTests

### Community 16 - "math"
Cohesion: 0.11
Nodes (9): american_call(), american_price(), bs93_phi(), bs_price(), horizon_option_window(), BlackScholesPricingTests, _Frozen, _load_manager() (+1 more)

### Community 17 - "test_optimizer.py"
Cohesion: 0.22
Nodes (3): _reload_manager(), RiskContributionTests, _synthetic_inputs()

### Community 19 - "FMPClient"
Cohesion: 0.14
Nodes (5): FMPClient, _latest(), stage_screener(), stage_solvency(), _to_float()

### Community 20 - "numpy"
Cohesion: 0.20
Nodes (4): build_risk_free_curve(), export_universe_json(), nearest_psd(), _synthetic_dashboard_inputs()

### Community 21 - "DataFrame"
Cohesion: 0.21
Nodes (4): ConsoleReporter, _historical_betas(), ImpliedCovarianceBuilder, _nearest_psd()

### Community 22 - "OptimizationResult"
Cohesion: 0.15
Nodes (6): ExpectedReturnModel, market_beta(), OptimizationResult, PassiveETFAllocationPipeline, PipelineInputs, RedundancyFilter

### Community 23 - "cornish_fisher_moments"
Cohesion: 0.18
Nodes (8): cornish_fisher_domain(), cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_params(), a_parametros(), residuo(), cornish_fisher_tail(), cornish_fisher_z()

### Community 25 - "beta_range_reachable"
Cohesion: 0.17
Nodes (3): beta_band_text(), beta_range_reachable(), BetaPoolFilter

### Community 29 - "report_pdf.py"
Cohesion: 0.16
Nodes (4): default_pdf_path(), export_report_pdf(), main(), ReportExportError

### Community 31 - "stage_scoring"
Cohesion: 0.22
Nodes (4): cap_weights(), stage_scoring(), stage_weights(), zscore()

### Community 32 - "cov_ewma_shrunk"
Cohesion: 0.25
Nodes (4): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ledoit_wolf_constant_correlation()

### Community 33 - "DataFrame"
Cohesion: 0.29
Nodes (4): _overlay_pivot(), print_refinitiv_instructions(), select_ratings(), _selected_ratings()

### Community 34 - "stage_rating"
Cohesion: 0.25
Nodes (4): rating_bucket(), _rating_rank(), stage_rating(), synthetic_rating()

### Community 36 - ".__init__"
Cohesion: 0.29
Nodes (3): higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 41 - "mfik_cap_tenor"
Cohesion: 0.40
Nodes (3): BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), mfik_cap(), mfik_cap_tenor()

### Community 46 - "._solve_qubo_sa"
Cohesion: 0.67
Nodes (3): flip_delta(), violation(), _project_capped_simplex()

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing`, `Linear program for factor target feasibility and relaxation`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 237 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `PortfolioOptimizer` to `US Asset Manager.py`, `._solve_qubo_sa`, `OptimizationResult`, `beta_range_reachable`, `Series`?**
  _High betweenness centrality (0.031) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Solvers: cvxpy, scipy SLSQP, QUBO simulated annealing` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `risk_estimators.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `Mean-variance optimization with factor targets` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `Mean-variance optimization with factor targets` be split into smaller, more focused modules?**
  _Cohesion score 0.058693244739756366 - nodes in this community are weakly interconnected._
- **Why does `ResolveHorizonTests` connect `test_horizon.py` to `ImpliedMomentsEngine`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `FakeResponse` be split into smaller, more focused modules?**
  _Cohesion score 0.10227272727272728 - nodes in this community are weakly interconnected._