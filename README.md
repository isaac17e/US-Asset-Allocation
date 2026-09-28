# US Asset Allocation

Herramientas en Python para construir portafolios de inversión sobre el mercado estadounidense con datos de mercado en vivo. El repositorio tiene dos pipelines independientes y un módulo de estimadores de riesgo compartido:

| Archivo | Qué hace |
|---|---|
| [`US Asset Manager.py`](US%20Asset%20Manager.py) | Asignación de activos con **ETFs**: arma el universo, estima factores, momentos implícitos de opciones y covarianza, y optimiza los pesos según un perfil de inversión. |
| [`Corp_FR_Optimization.py`](Corp_FR_Optimization.py) | Selección de un portafolio de **renta fija corporativa Investment Grade (USD)**: filtra emisores por solvencia, flujo de caja y rating, los rankea y calcula el rendimiento mínimo exigido por plazo. |
| [`risk_estimators.py`](risk_estimators.py) | Librería de estimadores de riesgo (covarianza EWMA + Ledoit-Wolf, corrección Q→P, momentos de portafolio, Cornish-Fisher). La usa `US Asset Manager.py`. |

Cada script se ejecuta de principio a fin, imprime tablas en consola y genera un reporte HTML interactivo con Plotly.

---

## 1. `US Asset Manager.py` — Asignación pasiva con ETFs

Pipeline orquestado por la clase `PassiveETFAllocationPipeline`, organizado en fases:

### Fase 0 · Universo híbrido
- **Lista maestra** de ~50 ETFs (`MASTER_ETF_LIST`): índices core de EE. UU., factores/estilos, sectores, megatendencias, internacionales, commodities, renta fija y real estate.
- **Candidatos dinámicos** desde el screener de FMP (NYSE, NASDAQ, AMEX), filtrados por volumen en dólares (≥ USD 1 M diarios) y excluyendo ETFs apalancados o inversos.
- Descarga de precios ajustados (3 años) y **eliminación de réplicas**: un ETF dinámico se descarta si su correlación con uno ya incluido es ≥ 0.985.

### Fase 1 · Matriz de cargas factoriales **B**
Para cada ETF se calcula un score entre 0 y 1 en cinco factores:

| Factor | Cómo se mide |
|---|---|
| Value | Earnings yield y book yield de los 10 principales holdings |
| Growth | Crecimiento de ingresos y de EPS de los holdings |
| Momentum | Retorno 12-1 meses |
| Quality | ROE y ROIC de los holdings |
| LowVol | Volatilidad realizada de 252 días (invertida) |

Los fundamentales se agregan ponderando por el peso de cada holding y se convierten en percentiles dentro del universo. Si falta un dato, el factor queda neutral (0.5).

### Fase 2 · Momentos, covarianza y retorno esperado
- **Momentos implícitos (BKM)**: con la cadena de opciones de Polygon (vencimientos de 30 a 90 días) se estiman la volatilidad, la asimetría y la curtosis implícitas libres de modelo (MFIV, MFIS, MFIK) con Bakshi, Kapadia y Madan (2003). La volatilidad implícita de cada strike se obtiene invirtiendo el modelo americano de Bjerksund-Stensland, se interpola con un spline y los resultados se llevan a un horizonte de 60 días. El dividend yield se lee por ticker desde FMP. Si no hay opciones disponibles, se usan momentos históricos.
- **Covarianza**: Σ = D·R·D, donde
  - **D** son las volatilidades implícitas ajustadas de medida Q (riesgo neutral) a medida P (física) para descontar la prima de riesgo de varianza;
  - **R** es la correlación histórica EWMA (vida media de 120 días) con shrinkage de Ledoit-Wolf hacia correlación constante.
  - También existe un modo `beta` (modelo de un factor contra SPY).
- **Retorno esperado μ**: 75 % CAPM (rf 4 % + β · prima de 5 %) y 25 % media histórica.

### Fase 3 · Optimización
Maximiza la utilidad media-varianza

```
max  μᵀw − ½·λ·wᵀΣw
s.a. Σw = 1,   0 ≤ w ≤ w_max,   Bᵀw ≥ targets factoriales
```

Los parámetros dependen del perfil elegido:

| Perfil | λ | w_max | Targets mínimos |
|---|---|---|---|
| Conservador | 8 | 15 % | Value 0.45 · Quality 0.55 · LowVol 0.70 |
| Crecimiento | 4 | 20 % | Growth 0.60 · Momentum 0.45 · Quality 0.55 |
| Momentum/Agresivo | 2 | 25 % | Growth 0.55 · Momentum 0.70 |

Antes de optimizar, un programa lineal verifica que los targets sean alcanzables y, si no lo son, los relaja lo mínimo necesario. Hay tres solvers disponibles, y opcionalmente se comparan entre sí:
- `cvxpy`: programación cuadrática (por defecto);
- `scipy`: SLSQP;
- `qubo_sa`: formulación QUBO con 5 bits por activo, resuelta con *simulated annealing*.

### Fases 4 y 5 · Salidas
- En consola: composición del universo, ETFs descartados, factores, momentos, μ, pesos óptimos, exposición factorial deseada vs. lograda, métricas (retorno, volatilidad, Sharpe, N efectivo) y la comparación de solvers.
- `portfolio_dashboard.html`: gráfico de asignación, radar de factores, dispersión riesgo-retorno y comparación de peso vs. contribución al riesgo.

---

## 2. `Corp_FR_Optimization.py` — Portafolio de bonos corporativos IG

Pipeline de screening de emisores en seis fases (`run_pipeline`):

1. **Curva libre de riesgo**: nodos CMT del Tesoro (1M a 30Y) desde FRED, interpolados con PCHIP.
2. **Screening y solvencia**: empresas de EE. UU. con market cap ≥ USD 10 bn, excluyendo servicios financieros. Se exige Deuda/EBITDA ≤ 3.0x y EBITDA/Intereses ≥ 2.5x.
3. **Free cash flow**: FCF estrictamente creciente **o** CAGR a 3 años > 3 % (configurable como `AND`).
4. **Rating**: solo grado de inversión (AAA a BBB-). Se usa el rating de FMP como aproximación, y `MANUAL_RATING_OVERRIDES` permite reemplazarlo por calificaciones reales de agencia.
5. **Composite Credit Score**: `0.40·Z(Cobertura) + 0.30·Z(−Deuda/EBITDA) + 0.30·Z(CAGR FCF)`, con Z-scores winsorizados a ±3. Se seleccionan los 15 mejores.
6. **Ponderación y Yield Target**:
   - dos esquemas de pesos: Equal Weight y Credit-Score Weight (con tope de 15 % por emisor), sobre un nocional de USD 10 M;
   - **rendimiento mínimo exigido** para plazos de 3, 5 y 10 años: `Rf(t) + spread por rating + prima por plazo + ajuste por score`.

**Salidas**: embudo de screening, ranking, pesos, tabla de yield targets, un checklist para buscar las emisiones concretas en **Refinitiv Workspace** (criterio de compra: YTW ≥ Target y OAS ≥ spread mínimo) y el reporte `reporte_portafolio_renta_fija.html`.

---

## 3. `risk_estimators.py` — Estimadores de riesgo

Módulo sin dependencias de red. Es una copia del módulo homónimo del repositorio AM-PM y debe mantenerse sincronizado con él.

1. **Covarianza**: EWMA, tamaño de muestra efectivo de Kish y shrinkage de Ledoit-Wolf (2003) hacia correlación constante (`cov_ewma_shrunk`), además de la proyección a la matriz semidefinida positiva más cercana.
2. **Corrección Q → P**: de la volatilidad implícita (prima de riesgo de varianza) y de la correlación implícita (prima de riesgo de correlación).
3. **Momentos de portafolio**: asimetría y curtosis del portafolio calculadas sobre un panel de escenarios en O(J·n), sin construir los tensores de co-momentos, junto con sus gradientes analíticos.
4. **Cornish-Fisher**: control de admisibilidad (K ≥ 1 + S²) e inversión momentos → parámetros según Maillard (2012), para obtener VaR/CVaR monótonos y consistentes.
5. **SVIX / Martin-Wagner**: retorno esperado a partir de varianzas implícitas. *Experimental y desactivado*: la fórmula aún no se ha verificado contra el paper.

---

## Requisitos

Python 3.10 o superior y:

```bash
pip install numpy pandas scipy requests plotly cvxpy tabulate fredapi
```

`cvxpy`, `tabulate` y `fredapi` son opcionales: si faltan, los scripts usan SciPy, `pandas.to_string` y la API REST de FRED, respectivamente.

### API keys

| Variable | Servicio | Usada por |
|---|---|---|
| `FMP_API_KEY` | [Financial Modeling Prep](https://financialmodelingprep.com) | Ambos scripts (obligatoria) |
| `POLYGON_API_KEY` | [Polygon.io](https://polygon.io): snapshot de opciones | `US Asset Manager.py` (opcional; sin ella se usan momentos históricos) |
| `FRED_API_KEY` | [FRED](https://fred.stlouisfed.org/docs/api/api_key.html) | `Corp_FR_Optimization.py` (obligatoria) |

Algunos endpoints de FMP (holdings de ETFs, estados financieros, ratings) dependen del plan contratado. Si un endpoint no está disponible, el script lo desactiva y continúa con valores neutrales o de respaldo.

## Uso

```bash
export FMP_API_KEY="..."
export POLYGON_API_KEY="..."
export FRED_API_KEY="..."

python "US Asset Manager.py"        # genera portfolio_dashboard.html
python Corp_FR_Optimization.py      # genera reporte_portafolio_renta_fija.html
```

Todos los parámetros (perfil de inversión, solver, umbrales de screening, pesos del score, spreads por rating, etc.) están en el bloque de configuración al inicio de cada archivo.

## Aviso

Este código tiene fines académicos y de investigación. No constituye asesoría de inversión. En particular, los ratings de FMP son un proxy cuantitativo y no reemplazan las calificaciones de S&P, Moody's o Fitch.
