1. **Start with**: `final_report.md` for executive summary / pradėti nuo vykdomosios santraukos
2. **Then review**: Key figures in `results/figures/` / tada peržiūrėti pagrindinius grafikus
3. **For details**: Examine CSV tables / detalėms nagrinėti CSV lenteles
4. **For integration**: Use JSON files / integracijai naudoti JSON failus

---

## Interpreting System Imbalance Results / Sistemos Disbalanso Rezultatų Interpretavimas

### 1. Hourly Imbalance Patterns Figure / Valandinių Disbalanso Modelių Grafikas

**File**: `hourly_imbalance_patterns.png`

**What to Look For / Į Ką Atkreipti Dėmesį:**
- **Positive values**: System surplus (generation > demand) / sistemos perteklius
- **Negative values**: System deficit (generation < demand) / sistemos trūkumas
- **Error bars**: 95% confidence intervals / 95% pasikliautinumo intervalai
- **Bars not crossing zero**: Statistically significant imbalance / statistiškai reikšmingas disbalansas

**Interpretation Example / Interpretavimo Pavyzdys:**
```
Hour 18: -85.3 MWh (CI: -135.4, -35.2)
→ Evening peak consistently shows ~85 MWh deficit
→ 95% confident the true deficit is between 35-135 MWh
→ Trading opportunity: anticipate shortage, position accordingly
```

### 2. Imbalance Statistics Table / Disbalanso Statistikos Lentelė

**File**: `hourly_imbalance_statistics.csv`

**Key Columns / Pagrindiniai Stulpeliai:**
- `mean_imbalance_mwh`: Average for that hour / vidurkis tai valandai
- `std_imbalance_mwh`: Volatility measure / nepastovumo matas
- `is_significant`: Statistical significance flag / statistinio reikšmingumo žymė

**Decision Rules / Sprendimų Taisyklės:**
```python
if is_significant and mean_imbalance < -50:
    action = "Strong sell signal (expect deficit)"
elif is_significant and mean_imbalance > 50:
    action = "Strong buy signal (expect surplus)"
else:
    action = "No clear signal"
```

### 3. Autocorrelation Plots / Autokoreliacijos Grafikai

**File**: `imbalance_autocorrelation.png`

**Reading ACF/PACF / ACF/PACF Skaitymas:**
- **Blue area**: Statistical significance bounds / statistinio reikšmingumo ribos
- **Bars outside blue**: Significant correlation at that lag / reikšminga koreliacija tam vėlavimui
- **ACF decay pattern**: Indicates time series properties / rodo laiko eilučių savybes

**Practical Implications / Praktinės Pasekmės:**
- Lag 1 correlation = 0.65 → Yesterday's pattern influences today
- Lag 24 correlation = 0.45 → Daily cycle exists
- Use for forecasting: AR(2) or ARMA(2,1) models recommended

---

## Reading Battery Optimization Results / Baterijų Optimizavimo Rezultatų Skaitymas

### 1. Strategy Comparison Chart / Strategijų Palyginimo Diagrama

**File**: `battery_strategy_comparison.png`

**Understanding the Bars / Stulpelių Supratimas:**
- **Height**: Annual profit in EUR / metinis pelnas EUR
- **Color intensity**: Implementation complexity / įgyvendinimo sudėtingumas
- **Error bars**: Sensitivity to parameter changes / jautrumas parametrų pokyčiams

**Strategy Characteristics / Strategijų Charakteristikos:**

| Strategy | Profit | Complexity | Risk | Best For |
|----------|--------|------------|------|----------|
| Heuristic | €35,420 | Low | Low | Quick implementation |
| Perfect | €42,150 | Medium | Medium | Benchmark comparison |
| Flexible | €43,890 | High | Low | Maximum returns |

### 2. Daily Profit Distribution / Dienos Pelno Pasiskirstymas

**File**: `battery_daily_profit_distribution.png`

**Histogram Interpretation / Histogramos Interpretavimas:**
- **Peak location**: Most common daily profit / dažniausias dienos pelnas
- **Spread**: Profit variability / pelno kintamumas
- **Left tail**: Loss days (rare but important) / nuostolingos dienos
- **Right tail**: Exceptional profit days / išskirtinio pelno dienos

**Risk Metrics / Rizikos Rodikliai:**
```
Mean daily profit: €115.48
Standard deviation: €45.23
5% VaR: -€12.50 (5% chance of losing more)
95% percentile: €198.75 (5% chance of earning more)
```

### 3. Investment Analysis Table / Investicijų Analizės Lentelė

**File**: `investment_analysis.csv`

**Key Financial Metrics / Pagrindiniai Finansiniai Rodikliai:**

| Metric | Value | Interpretation |
|--------|-------|----------------|
| Simple Payback | 4.2 years | Time to recover investment / investicijos atsipirkimo laikas |
| NPV @ 8% | €178,450 | Present value of profits / dabartinė pelno vertė |
| IRR | 15.2% | Effective annual return / ef# Results Interpretation Guide / Rezultatų Interpretavimo Vadovas 📊

This guide explains how to interpret the outputs from the Lithuanian electricity market analysis.

Šis vadovas paaiškina, kaip interpretuoti Lietuvos elektros rinkos analizės rezultatus.

## Table of Contents / Turinys

1. [Understanding the Outputs / Rezultatų Supratimas](#understanding-the-outputs--rezultatų-supratimas)
2. [Interpreting System Imbalance Results / Sistemos Disbalanso Rezultatų Interpretavimas](#interpreting-system-imbalance-results--sistemos-disbalanso-rezultatų-interpretavimas)
3. [Reading Battery Optimization Results / Baterijų Optimizavimo Rezultatų Skaitymas](#reading-battery-optimization-results--baterijų-optimizavimo-rezultatų-skaitymas)
4. [Understanding Elasticity Estimates / Elastingumo Įverčių Supratimas](#understanding-elasticity-estimates--elastingumo-įverčių-supratimas)
5. [Financial Metrics Interpretation / Finansinių Rodiklių Interpretavimas](#financial-metrics-interpretation--finansinių-rodiklių-interpretavimas)
6. [Common Pitfalls / Dažnos Klaidos](#common-pitfalls--dažnos-klaidos)

---

## Understanding the Outputs / Rezultatų Supratimas

### File Types and Their Purpose / Failų Tipai ir Jų Paskirtis

| File Type | Location | Purpose | Key Information |
|-----------|----------|---------|-----------------|
| `.png` figures | `results/figures/` | Visual insights | Patterns, trends, relationships |
| `.csv` tables | `results/tables/` | Detailed metrics | Exact values, statistics |
| `.json` results | `results/` | Structured data | Machine-readable results |
| `.txt` reports | `results/` | Narrative conclusions | Summary and recommendations |
| `.md` report | `results/` | Formatted report | Executive presentation |

### Reading Priority / Skaitymo Prioritetas

1. **Start with**: `final_report.md` for executive summary / pradėti nuo vykdomosios santraukos
2.