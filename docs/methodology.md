### 4. Demand Response Quantification / Paklausos Atsako Kiekybinis Įvertinimas

**Scenario Analysis**:
```python
def calculate_dr_potential(elasticity, base_demand, price_increase_pct):
    """
    Calculate demand response using constant elasticity formula
    ΔQ/Q = ε × ΔP/P
    """
    demand_change_pct = elasticity * price_increase_pct
    demand_reduction_mwh = base_demand * abs(demand_change_pct) / 100
    return demand_reduction_mwh
```

**Peak Shaving Potential**:
- Base peak demand: 1,200 MWh (17-20h average)
- Price signals tested: 5%, 10%, 15%, 20%
- Elasticity applied: -0.234 (national) to -0.342 (industrial)

---

## Validation & Robustness / Validavimas ir Patikimumas

### 1. Cross-Validation / Kryžminis Validavimas

**Time Series Split Validation**:
```python
from sklearn.model_selection import TimeSeriesSplit

tscv = TimeSeriesSplit(n_splits=5)
scores = []

for train_idx, test_idx in tscv.split(data):
    train_data = data.iloc[train_idx]
    test_data = data.iloc[test_idx]
    
    # Train model on train_data
    # Evaluate on test_data
    scores.append(evaluation_metric)
```

### 2. Sensitivity Analysis / Jautrumo Analizė

**Parameters Tested**:
- Battery efficiency: ±5%
- Price volatility: ±20%
- Elasticity estimates: ±1 standard error
- Discount rate: 6-10%

**Monte Carlo Simulation** (1,000 iterations):
```python
results = []
for i in range(1000):
    # Perturb parameters
    efficiency = np.random.normal(0.92, 0.02)
    volatility_factor = np.random.uniform(0.8, 1.2)
    
    # Recalculate metrics
    profit = calculate_profit(prices * volatility_factor, efficiency)
    results.append(profit)

# Calculate confidence intervals
ci_low, ci_high = np.percentile(results, [2.5, 97.5])
```

### 3. Robustness Checks / Patikimumo Patikrinimai

1. **Alternative Specifications**:
   - Non-linear price-quantity relationships
   - Time-varying elasticities
   - Different outlier treatments

2. **Subsample Analysis**:
   - Weekdays vs weekends
   - Summer vs winter
   - High vs low price periods

3. ****Risk Management**:
- Position size: 1 MWh (minimal market impact)
- Stop-loss: Exit if cumulative loss > €10,000
- Maximum exposure: 4 hours per day

---

## Part II: Battery Storage Optimization / Baterijų Saugojimo Optimizavimas

### 1. Battery Technical Specifications / Techninės Specifikacijos

| Parameter | Value | Unit |
|-----------|-------|------|
| Power Capacity | 1 | MW |
| Energy Capacity | 2 | MWh |
| Round-trip Efficiency | 92 | % |
| Max Cycles/Day | 2 | cycles |
| Depth of Discharge | 90 | % |
| Degradation | 0 | % (ignored) |

### 2. Optimization Strategies / Optimizavimo Strategijos

#### A. Heuristic Strategy / Euristinė Strategija

**Algorithm**: Daily pattern-based operation
```python
def heuristic_strategy(prices_day):
    # Find 2 cheapest hours for charging
    charge_hours = prices_day.nsmallest(2).index
    
    # Find 2 most expensive hours for discharging
    discharge_hours = prices_day.nlargest(2).index
    
    # Calculate profit
    revenue = sum(prices_day[discharge_hours]) * efficiency
    cost = sum(prices_day[charge_hours]) / efficiency
    
    return revenue - cost
```

#### B. Perfect Forecast Strategy / Tobulos Prognozės Strategija

**Optimization Problem**:
```
maximize Σ(p_t × d_t × η - p_t × c_t / η)
subject to:
    c_t + d_t ≤ 1           ∀t  (mutual exclusion)
    Σc_t ≤ 2                    (max charge cycles)
    Σd_t ≤ 2                    (max discharge cycles)
    SOC_t = SOC_{t-1} + c_t - d_t
    0 ≤ SOC_t ≤ 2          ∀t  (capacity limits)
    c_t, d_t ∈ {0,1}       ∀t  (binary decisions)
```

#### C. Flexible Annual Strategy / Lanksti Metinė Strategija

**Mixed Integer Linear Programming (MILP)**:
```python
from pulp import *

prob = LpProblem("BatteryOptimization", LpMaximize)

# Decision variables
charge = LpVariable.dicts("charge", hours, 0, 1, LpBinary)
discharge = LpVariable.dicts("discharge", hours, 0, 1, LpBinary)
soc = LpVariable.dicts("soc", hours, 0, 2, LpContinuous)

# Objective function
prob += lpSum([
    discharge[t] * price[t] * efficiency - 
    charge[t] * price[t] / efficiency 
    for t in hours
])

# Constraints
for t in hours:
    # State of charge dynamics
    prob += soc[t] == soc[t-1] + charge[t] - discharge[t]
    
    # Can't charge and discharge simultaneously
    prob += charge[t] + discharge[t] <= 1
    
# Daily cycle limits (flexible)
for day in days:
    day_hours = [h for h in hours if h.date() == day]
    prob += lpSum([charge[h] for h in day_hours]) <= 2
    prob += lpSum([discharge[h] for h in day_hours]) <= 2
```

### 3. Financial Analysis / Finansinė Analizė

**Net Present Value (NPV)**:
```
NPV = -CAPEX + Σ(CF_t / (1+r)^t)
```
Where:
- CAPEX = €300,000
- CF_t = Annual cash flow (revenue - O&M)
- r = 8% (discount rate)
- t = years (1-10)

**Internal Rate of Return (IRR)**:
Solved numerically where NPV = 0

**Levelized Cost of Energy (LCOE)**:
```
LCOE = (CAPEX + Σ(O&M_t/(1+r)^t)) / Σ(E_t/(1+r)^t)
```

---

## Part III: Demand Elasticity Estimation / Paklausos Elastingumo Vertinimas

### 1. Econometric Model / Ekonometrinis Modelis

**Log-log specification for constant elasticity**:
```
ln(D_t) = α + β₁×ln(P_t) + β₂×T_t + β₃×Hour_t + β₄×Weekday_t + ε_t
```

Where:
- D_t = Electricity demand (MWh)
- P_t = Electricity price (EUR/MWh)
- T_t = Temperature (°C)
- Hour_t = Hour fixed effects
- Weekday_t = Day of week fixed effects
- β₁ = Price elasticity of demand

### 2. Estimation Methods / Vertinimo Metodai

#### A. National Level / Nacionalinis Lygis

**OLS with Heteroskedasticity-Robust Standard Errors**:
```python
# Log transformation
analysis_df['log_demand'] = np.log(analysis_df['demand_MWh'])
analysis_df['log_price'] = np.log(analysis_df['price_EUR_MWh'])

# Regression
X = sm.add_constant(analysis_df[[
    'log_price', 'avg_temperature', 'hour', 'weekday'
]])
y = analysis_df['log_demand']

model = sm.OLS(y, X).fit(cov_type='HC3')
```

#### B. Object Level Panel Analysis / Objektų Lygio Panelinė Analizė

**Fixed Effects Model**:
```
ln(D_{it}) = α_i + β₁×ln(P_t) + β₂×T_t + γ×X_{it} + ε_{it}
```

Where:
- i = object index
- α_i = object-specific fixed effect
- X_{it} = time-varying controls

**Estimation**:
```python
from linearmodels import PanelOLS

panel_data = panel_df.set_index(['object_id', 'timestamp'])
model = PanelOLS(
    panel_data['log_consumption'],
    panel_data[['log_price', 'temperature']],
    entity_effects=True
).fit()
```

### 3. Heterogeneity Analysis / Heterogeniškumo Analizė

**Quantile Regression** to capture elasticity distribution:
```python
import statsmodels.formula.api as smf

# Estimate elasticity at different quantiles
quantiles = [0.1, 0.25, 0.5, 0.75, 0.9]
results = []

for q in quantiles:
    qr_model = smf.quantreg(
        'log_consumption ~ log_price + temperature', 
        data=panel_df
    ).fit(q=q)
    results.append({
        'quantile': q,
        'elasticity': qr_model.params['log_price']
    })
```

###- **H₀**: Imbalance distributions are identical across quarters
- **Result**: p = 0.082 → Fail to reject H₀ (patterns stable across year)

### 3. Autocorrelation Analysis / Autokoreliacijos Analizė

**Methods**:
- **ACF (Autocorrelation Function)**: Measures linear dependence between observations
- **PACF (Partial ACF)**: Measures direct dependence removing intermediate lags

```python
# ACF/PACF Analysis
acf_values = sm.tsa.acf(imbalance_series, nlags=48)
pacf_values = sm.tsa.pacf(imbalance_series, nlags=48)

# Ljung-Box test for autocorrelation
lb_stat, lb_pvalue = sm.stats.acorr_ljungbox(imbalance_series, lags=24)
```

**Key Findings**:
- Significant autocorrelation up to lag 24 (daily cycle)
- PACF cuts off after lag 1-2 suggesting AR(2) process
- Ljung-Box test: p < 0.001 (significant serial correlation)

### 4. Price-Quantity Relationship / Kainos-Kiekio Santykis

**Linear Regression Model**:
```
Price_t = β₀ + β₁ × Imbalance_t + ε_t
```

**Estimation Method**: Ordinary Least Squares (OLS) with HAC standard errors

```python
X = sm.add_constant(balancing_df['quantity_MWh'])
y = balancing_df['price_EUR_MWh']
model = sm.OLS(y, X).fit(cov_type='HAC', cov_kwds={'maxlags': 24})
```

**Results**:
- β₁ = -0.784 (SE: 0.089, p < 0.001)
- R² = 0.156
- **Interpretation**: 1 MWh increase in system surplus → €0.78 price decrease

### 5. Trading Strategy Development / Prekybos Strategijos Kūrimas

**Strategy Logic**:
1. Identify high-probability imbalance hours
2. Take speculative positions when conditions align
3. Settle at imbalance price

**Decision Rules**:
```python
def trading_signal(hour, lag_imbalance, lag_price):
    # Evening deficit signal
    if hour in [17, 18, 19, 20] and lag_imbalance < 0:
        return -1  # Create shortage (sell)
    
    # Night surplus signal  
    elif hour in [2, 3, 4, 5] and lag_imbalance > 0:
        return 1   # Create surplus (buy)
    
    else:
        return 0   # No position
```

**Risk Management**:# Detailed Methodology / Detali Metodologija 🔬

## Table of Contents / Turinys

1. [Overview / Apžvalga](#overview--apžvalga)
2. [Data Collection & Preparation / Duomenų Rinkimas ir Paruošimas](#data-collection--preparation--duomenų-rinkimas-ir-paruošimas)
3. [Part I: System Imbalance Analysis / Sistemos Disbalanso Analizė](#part-i-system-imbalance-analysis--sistemos-disbalanso-analizė)
4. [Part II: Battery Storage Optimization / Baterijų Saugojimo Optimizavimas](#part-ii-battery-storage-optimization--baterijų-saugojimo-optimizavimas)
5. [Part III: Demand Elasticity Estimation / Paklausos Elastingumo Vertinimas](#part-iii-demand-elasticity-estimation--paklausos-elastingumo-vertinimas)
6. [Validation & Robustness / Validavimas ir Patikimumas](#validation--robustness--validavimas-ir-patikimumas)

---

## Overview / Apžvalga

This document provides a comprehensive technical description of the methodologies employed in the Lithuanian electricity market analysis. The analysis follows rigorous econometric and optimization techniques to ensure robust and reproducible results.

Šis dokumentas pateikia išsamų techninį Lietuvos elektros rinkos analizėje naudotų metodologijų aprašymą. Analizė seka griežtas ekonometrines ir optimizavimo technikas, užtikrinant patikimus ir atkartojamus rezultatus.

### Research Questions / Tyrimų Klausimai

1. **RQ1**: Are there systematic patterns in electricity system imbalances that can be exploited for profit?
2. **RQ2**: What is the optimal operation strategy for grid-scale battery storage in Lithuania?
3. **RQ3**: How responsive is electricity demand to price changes, and what is the demand response potential?

### Analytical Framework / Analitinė Sistema

```
Data Sources → Data Cleaning → Statistical Analysis → Optimization → Validation
     ↓              ↓                ↓                    ↓             ↓
  Raw Files    Standardization   Hypothesis Tests    Strategies    Backtesting
```

---

## Data Collection & Preparation / Duomenų Rinkimas ir Paruošimas

### 1. Data Sources / Duomenų Šaltiniai

| Dataset | Source | Frequency | Period | Records |
|---------|--------|-----------|--------|---------|
| System Imbalance | Litgrid | Hourly | 2024-01-01 to 2024-12-31 | 8,784 |
| Day-ahead Prices | Nord Pool | Hourly | 2024-01-01 to 2024-12-31 | 8,784 |
| Weather Data | LHMT | Hourly | 2024-01-01 to 2024-12-31 | 8,784 |
| National Demand | Litgrid | Hourly | 2024-01-01 to 2024-12-31 | 8,784 |
| Object Consumption | Energy Cos | Hourly | 2024-01-01 to 2024-12-31 | 974,424 |

### 2. Data Cleaning Process / Duomenų Valymo Procesas

```python
# Standardization pipeline
def clean_data(df):
    # 1. Handle missing values
    df = df.interpolate(method='linear', limit=2)
    
    # 2. Remove outliers (IQR method)
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    df = df[~((df < (Q1 - 1.5 * IQR)) | (df > (Q3 + 1.5 * IQR)))]
    
    # 3. Ensure temporal consistency
    df = df.sort_values('timestamp')
    df = df.set_index('timestamp').asfreq('H')
    
    return df
```

### 3. Feature Engineering / Požymių Inžinerija

Created temporal features for enhanced analysis:
- `hour`: Hour of day (0-23)
- `day_of_week`: Day of week (0-6)
- `month`: Month (1-12)
- `quarter`: Quarter (1-4)
- `is_weekend`: Binary weekend indicator
- `is_peak`: Peak hours indicator (17-20h)

---

## Part I: System Imbalance Analysis / Sistemos Disbalanso Analizė

### 1. Hourly Pattern Detection / Valandinių Modelių Aptikimas

**Methodology**: Group-wise statistical analysis with confidence intervals

```python
# Calculate hourly statistics
hourly_stats = balancing_df.groupby('hour')['quantity_MWh'].agg([
    'mean', 'std', 'count'
])

# 95% Confidence Intervals
hourly_stats['ci95_low'] = hourly_stats['mean'] - 1.96 * hourly_stats['std'] / np.sqrt(hourly_stats['count'])
hourly_stats['ci95_high'] = hourly_stats['mean'] + 1.96 * hourly_stats['std'] / np.sqrt(hourly_stats['count'])

# Statistical significance test
significant = (hourly_stats['ci95_low'] > 0) | (hourly_stats['ci95_high'] < 0)
```

**Statistical Tests Applied**:
- **Null Hypothesis (H₀)**: Mean imbalance = 0 for each hour
- **Alternative (H₁)**: Mean imbalance ≠ 0
- **Test**: One-sample t-test for each hour
- **Significance Level**: α = 0.05

### 2. Temporal Stability Testing / Laiko Stabilumo Testavimas

**Kruskal-Wallis Test** for quarterly differences:
```python
kw_stat, p_value = stats.kruskal(
    *[df[df['quarter']==q]['quantity_MWh'] for q in range(1,5)]
)
```

- **H₀**: Imbalance distributions are identical across quarters
- **Result**: p = 0.082 → Fail to reject H₀ (patterns stable across year)# Detailed Methodology / Detali Metodologija 🔬

## Table of Contents / Turinys

1. [Overview / Apžvalga](#overview--apžvalga)
2. [Data Collection & Preparation / Duomenų Rinkimas ir Paruošimas](#data-collection--preparation--duomenų-rinkimas-ir-paruošimas)
3. [Part I: System Imbalance Analysis / Sistemos Disbalanso Analizė](#part-i-system-imbalance-analysis--sistemos-disbalanso-analizė)
4. [Part II: Battery Storage Optimization / Baterijų Saugojimo Optimizavimas](#part-ii-battery-storage-optimization--baterijų-saugojimo-optimizavimas)
5. [Part III: Demand Elasticity Estimation / Paklausos Elastingumo