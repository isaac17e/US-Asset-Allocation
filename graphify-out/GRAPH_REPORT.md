# Graph Report - US-Asset-Allocation  (2026-10-27)

## Corpus Check
- 20 files · ~32,175 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 4 file(s) not represented in the graph (top: (none) 4)

## Summary
- 726 nodes · 1527 edges · 50 communities (29 shown, 21 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 32 edges (avg confidence: 0.9)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `92c8b3e2`
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
- to_years
- Any
- ResolveHorizonTests
- ._profile
- pipeline_io.py
- DataFrame
- _tail_inputs
- check_risk_estimators_sync.py
- _load_manager
- _delta_referencia
- mock_patch
- FMPClient
- os
- BlackScholesPricingTests
- .prepare
- cornish_fisher_moments
- AtomicWriteTests
- beta_range_reachable
- RawBetaTests
- RiskFreeCurve
- .build
- report_pdf.py
- cornish_fisher_params
- stage_scoring
- numpy
- DataFrame
- _rating_rank
- build_html_report
- var_cvar_cornish_fisher
- MassiveBaseTests
- ReportPdfUnitTests
- OptimizationError
- US Asset Manager.py
- ImpliedCovarianceBuilder
- _Frozen
- OptionWindowTests
- stage_fcf
- math
- test_pipeline_io.py
- RiskProfileTests
- RiskFreeRateTests
- WeightTests

## God Nodes (most connected - your core abstractions)
1. `run_pipeline()` - 29 edges
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
- `mfik_cap_tenor()` --implements--> `BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor)`  [EXTRACTED]
  risk_estimators.py → README.md
- `ImpliedTailModel` --implements--> `ImpliedTailModel (Cornish-Fisher marginals, Gaussian copula)`  [EXTRACTED]
  US Asset Manager.py → README.md
- `_client()` --calls--> `FMPClient`  [EXTRACTED]
  tests/test_fmp_client.py → fmp_client.py
- `resolve_risk_profile()` --implements--> `Risk profile selection (--risk-profile / RISK_PROFILE, resolve_risk_profile)`  [EXTRACTED]
  pipeline_io.py → README.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Corporate bond issuer screening funnel** — readme_risk_free_curve, readme_solvency_screen, readme_fcf_screen, readme_synthetic_rating, readme_composite_credit_score, readme_weighting_schemes, readme_minimum_required_yield [EXTRACTED 1.00]
- **ETF allocation pipeline phases (universe, factors, moments/covariance, optimization)** — readme_hybrid_universe, readme_factor_loading_matrix_b, readme_covariance_drd, readme_expected_return_mu, readme_mean_variance_optimization [EXTRACTED 1.00]
- **risk_estimators library components** — readme_covariance_ewma_shrunk, readme_q_to_p_correction, readme_portfolio_moments, readme_cornish_fisher, readme_svix_martin_wagner [EXTRACTED 1.00]

## Communities (50 total, 21 thin omitted)

### Community 0 - "Corp_FR_Optimization.py"
Cohesion: 0.25
Nodes (12): _abort_if_empty(), _banner(), build_risk_free_curve(), _check_keys(), _fmt_pct(), portfolio_summary(), print_curve(), print_funnel() (+4 more)

### Community 1 - "risk_estimators.py"
Cohesion: 0.12
Nodes (9): Portfolio skewness/kurtosis in O(J n) with analytical gradients, SVIX / Martin-Wagner expected return (experimental, disabled), martin_wagner_excess_return(), mfik_cap(), mfik_cap_tenor(), nearest_psd(), portfolio_moment_gradients(), q_to_p_correlation() (+1 more)

### Community 2 - "PortfolioOptimizer"
Cohesion: 0.22
Nodes (4): OptimizationResult, PassiveETFAllocationPipeline, PortfolioOptimizer, objective()

### Community 3 - "Mean-variance optimization with factor targets"
Cohesion: 0.06
Nodes (37): resolve_risk_free_rate(), Bjerksund-Stensland American option model, BKM horizon scaling to 60 days and MFIK cap (mfik_cap_tenor), Bakshi-Kapadia-Madan (BKM) model-free implied moments, Composite Credit Score, Cornish-Fisher VaR/CVaR (Maillard 2012), IG corporate bond issuer screening pipeline (run_pipeline), Covariance Sigma = D R D (+29 more)

### Community 4 - "ndarray"
Cohesion: 0.21
Nodes (5): BKMEstimator, ImpliedTailModel, flip_delta(), violation(), _project_capped_simplex()

### Community 5 - "test_html_reports_browser.py"
Cohesion: 0.08
Nodes (13): collect_page_errors(), install_offline_route(), launch_browser(), load_playwright(), wait_for_plotly(), AllocationDashboardTests, CorpFixedIncomeHTMLTests, CorpFixedIncomeReportTests (+5 more)

### Community 6 - "FakeResponse"
Cohesion: 0.19
Nodes (4): _client(), CorpTolerantClientTests, FakeResponse, TransportTests

### Community 7 - "to_years"
Cohesion: 0.22
Nodes (4): annualize(), scale_bkm_moments(), scale_moments(), to_years()

### Community 8 - "Any"
Cohesion: 0.05
Nodes (19): APIAuthorizationError, APIError, BaseHTTPClient, FMPClient, _to_float(), _clip(), _combine_scores(), ETFDescriptor (+11 more)

### Community 10 - "._profile"
Cohesion: 0.11
Nodes (7): ExportProfileTests, FactorTargetTests, PortfolioConstraintTests, _reload_manager(), RiskContributionTests, RiskProfileSelectionTests, _synthetic_inputs()

### Community 11 - "pipeline_io.py"
Cohesion: 0.17
Nodes (11): atomic_write_json(), _atomic_write_text(), _cli_risk_profile(), _dumps(), _horizon_from_source(), _horizon_number(), months_to_days(), resolve_horizon_days() (+3 more)

### Community 13 - "_tail_inputs"
Cohesion: 0.14
Nodes (5): OneSidedPenaltyTests, _tail_inputs(), TailModelTests, TailPenaltySolveTests, TailRiskReportTests

### Community 14 - "check_risk_estimators_sync.py"
Cohesion: 0.24
Nodes (5): US Asset Allocation README, AM-PM repository (source of risk_estimators copy), Manual risk_estimators.py sync with AM-PM (drift check), definitions(), main()

### Community 15 - "_load_manager"
Cohesion: 0.24
Nodes (3): ExportHorizonTests, _load_manager(), ManagerHorizonTests

### Community 16 - "_delta_referencia"
Cohesion: 0.26
Nodes (4): _delta_referencia(), LedoitWolfEwmaTests, _retornos_normales(), _retornos_shock_covid()

### Community 18 - "mock_patch"
Cohesion: 0.15
Nodes (4): HorizonAlignmentTests, MfikCapTests, mock_patch, mock_stub()

### Community 19 - "FMPClient"
Cohesion: 0.14
Nodes (5): FMPClient, _latest(), stage_screener(), stage_solvency(), _to_float()

### Community 20 - "os"
Cohesion: 0.22
Nodes (6): export_universe_json(), iso_bogota(), normalize_weights(), now_bogota(), stamp_bogota(), export_portfolio_json()

### Community 21 - "BlackScholesPricingTests"
Cohesion: 0.29
Nodes (3): BlackScholesPricingTests, _load_manager(), _outcome()

### Community 22 - ".prepare"
Cohesion: 0.25
Nodes (3): ExpectedReturnModel, PipelineInputs, RedundancyFilter

### Community 23 - "cornish_fisher_moments"
Cohesion: 0.15
Nodes (7): cornish_fisher_es_gradient(), cornish_fisher_moments(), cornish_fisher_tail(), cornish_fisher_z(), higher_moments_admissible(), rescale_panel(), standardized_panel()

### Community 25 - "beta_range_reachable"
Cohesion: 0.17
Nodes (3): beta_band_text(), beta_range_reachable(), BetaPoolFilter

### Community 29 - "report_pdf.py"
Cohesion: 0.10
Nodes (9): default_pdf_path(), export_report_pdf(), main(), _QuietHandler, ReportExportError, load_manager(), main(), configure_logging() (+1 more)

### Community 30 - "cornish_fisher_params"
Cohesion: 0.40
Nodes (4): cornish_fisher_domain(), cornish_fisher_params(), a_parametros(), residuo()

### Community 31 - "stage_scoring"
Cohesion: 0.22
Nodes (4): cap_weights(), stage_scoring(), stage_weights(), zscore()

### Community 32 - "numpy"
Cohesion: 0.21
Nodes (6): average_correlation(), cov_ewma_shrunk(), effective_sample_size(), ewma_cov(), ewma_weights(), ledoit_wolf_constant_correlation()

### Community 33 - "DataFrame"
Cohesion: 0.40
Nodes (3): _overlay_pivot(), print_refinitiv_instructions(), select_ratings()

### Community 34 - "_rating_rank"
Cohesion: 0.17
Nodes (8): effective_solvency_limits(), rating_bucket(), _rating_rank(), _selected_ratings(), stage_rating(), synthetic_rating(), validate_rating_selection(), _worst_selected_rating()

### Community 46 - "math"
Cohesion: 0.21
Nodes (7): american_call(), american_price(), bs93_phi(), bs_price(), horizon_option_window(), _json_float(), market_beta()

## Knowledge Gaps
- **13 isolated node(s):** `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model`, `Academic-use disclaimer`, `Free cash flow screen (increasing or CAGR > 3%)` (+8 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 240 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **21 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `PortfolioOptimizer` connect `PortfolioOptimizer` to `ndarray`, `OptimizationError`, `US Asset Manager.py`, `DataFrame`, `beta_range_reachable`?**
  _High betweenness centrality (0.030) - this node is a cross-community bridge._
- **What connects `Portfolio skewness/kurtosis in O(J n) with analytical gradients`, `SVIX / Martin-Wagner expected return (experimental, disabled)`, `Bjerksund-Stensland American option model` to the rest of the system?**
  _13 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `risk_estimators.py` be split into smaller, more focused modules?**
  _Cohesion score 0.125 - nodes in this community are weakly interconnected._
- **Why does `IG corporate bond issuer screening pipeline (run_pipeline)` connect `Mean-variance optimization with factor targets` to `Corp_FR_Optimization.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `Mean-variance optimization with factor targets` be split into smaller, more focused modules?**
  _Cohesion score 0.05555555555555555 - nodes in this community are weakly interconnected._
- **Why does `ResolveHorizonTests` connect `ResolveHorizonTests` to `test_optimizer.py`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **Should `test_html_reports_browser.py` be split into smaller, more focused modules?**
  _Cohesion score 0.08108108108108109 - nodes in this community are weakly interconnected._