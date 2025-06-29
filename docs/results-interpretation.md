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
| IRR | 15.2% | Effective annual return / efektyvus metinis pelningumas |
| LCOE | €67.3/MWh | Cost per MWh cycled / kaina už MWh ciklą |

**Investment Decision Framework / Investicijų Sprendimų Sistema:**
```
If IRR > Cost of Capital (8%) → Invest
If Payback < Target (5 years) → Invest
If NPV > 0 → Invest
All criteria met ✓ → Strong investment case
```

---

## Understanding Elasticity Estimates / Elastingumo Įverčių Supratimas

### 1. Elasticity Interpretation / Elastingumo Interpretavimas

**File**: `demand_elasticity_results.csv`

**What Elasticity Means / Ką Reiškia Elastingumas:**
- **-0.234**: 1% price increase → 0.234% demand decrease
- **Negative**: Normal good (price ↑ → demand ↓)
- **|ε| < 1**: Inelastic demand (necessity)
- **|ε| > 1**: Elastic demand (luxury/substitutable)

**Practical Examples / Praktiniai Pavyzdžiai:**
```
Current price: €70/MWh, Current demand: 1,200 MWh
10% price increase to €77/MWh
→ Demand decreases by 0.234 × 10% = 2.34%
→ New demand: 1,200 × (1 - 0.0234) = 1,172 MWh
→ Demand reduction: 28 MWh
```

### 2. Heterogeneity Analysis / Heterogeniškumo Analizė

**File**: `elasticity_heterogeneity.png`

**Distribution Interpretation / Pasiskirstymo Interpretavimas:**
- **Center**: Most common elasticity / dažniausias elastingumas
- **Width**: Variation across consumers / variacija tarp vartotojų
- **Tails**: Extreme responders / kraštutiniai atsakytojai

**Consumer Categories / Vartotojų Kategorijos:**
| Type | Elasticity | Characteristics |
|------|------------|-----------------|
| Industrial | -0.342 | More flexible, can adjust processes |
| Commercial | -0.198 | Moderate flexibility |
| Small Business | -0.156 | Limited flexibility |

### 3. Demand Response Scenarios / Paklausos Atsako Scenarijai

**File**: `demand_response_scenarios.csv`

**Reading the Table / Lentelės Skaitymas:**
```
Price Signal: 10%
National DR: 280 MWh (2.33%)
Peak DR: 330 MWh (2.75%)
```

**Implementation Guidance / Įgyvendinimo Gairės:**
- **Small signals (5%)**: Easy to implement, low disruption
- **Medium signals (10-15%)**: Requires coordination
- **Large signals (20%+)**: Only for emergencies

---

## Financial Metrics Interpretation / Finansinių Rodiklių Interpretavimas

### 1. Understanding ROI / ROI Supratimas

**Return on Investment Calculation / Investicijų Grąžos Skaičiavimas:**
```
ROI = (Annual Profit - Annual Costs) / Initial Investment × 100%
ROI = (€42,150 - €5,000) / €300,000 × 100% = 12.4%
```

**Benchmarks / Lyginamieji Rodikliai:**
- Risk-free rate: ~3%
- Equity market: ~8-10%
- **This project: 15.2%** ✓ Above market

### 2. NPV Interpretation / NPV Interpretavimas

**Net Present Value / Grynoji Dabartinė Vertė:**
```
NPV = -Initial Investment + Σ(Cash Flow_t / (1+r)^t)
```

**Decision Rule / Sprendimo Taisyklė:**
- NPV > 0: Project creates value / projektas kuria vertę
- NPV < 0: Project destroys value / projektas naikina vertę
- **This project: €178,450** ✓ Strong value creation

### 3. Payback Period Context / Atsipirkimo Laikotarpio Kontekstas

**Comparative Paybacks / Lyginamieji Atsipirkimai:**
| Technology | Typical Payback |
|------------|-----------------|
| Solar PV | 6-8 years |
| Wind | 5-7 years |
| **Battery Storage** | **4.2 years** ✓ |
| Gas Peaker | 10-15 years |

---

## Common Pitfalls / Dažnos Klaidos

### 1. Misinterpreting Confidence Intervals / Pasikliautinumo Intervalų Klaidingas Aiškinimas

❌ **Wrong**: "The value will be between X and Y"  
✓ **Correct**: "We are 95% confident the true mean is between X and Y"

### 2. Assuming Constant Conditions / Pastovių Sąlygų Prielaida

❌ **Wrong**: "Results will be identical in 2025"  
✓ **Correct**: "Results assume 2024 conditions persist"

### 3. Ignoring Risk / Rizikos Ignoravimas

❌ **Wrong**: "Expected profit = guaranteed profit"  
✓ **Correct**: "Expected profit with σ = €X uncertainty"

### 4. Linear Extrapolation / Tiesinė Ekstrapoliacija

❌ **Wrong**: "2× battery = 2× profit"  
✓ **Correct**: "Larger battery may face diminishing returns"

---

## Quick Reference Card / Greitos Nuorodos Kortelė

### Key Numbers to Remember / Svarbūs Skaičiai

| Metric | Value | What It Means |
|--------|-------|---------------|
| -85 MWh | Hour 18 deficit | Best trading hour |
| €86,890 | Trading profit | Annual opportunity |
| 4.2 years | Battery payback | Investment timeline |
| -0.234 | Demand elasticity | Price responsiveness |
| 280 MWh | DR @ 10% price | Peak reduction potential |

### Decision Flowchart / Sprendimų Diagrama

```
Should I invest in battery storage?
├─ Is IRR > 8%? → Yes (15.2%)
├─ Is payback < 5 years? → Yes (4.2)
├─ Is NPV > 0? → Yes (€178k)
└─ Decision: YES, INVEST ✓

Should I implement demand response?
├─ Is |elasticity| > 0.2? → Yes (0.234)
├─ Is peak demand > 1000 MWh? → Yes (1200)
├─ Can achieve 5% reduction? → Yes (140 MWh)
└─ Decision: YES, IMPLEMENT ✓
```

---

## Questions and Support / Klausimai ir Pagalba

For questions about specific results:
- Check the methodology document first
- Review the relevant notebook section
- Contact: aurimas.nausedas@proton.me

Common questions addressed in:
- `docs/methodology.md` - Technical details
- `notebooks/README.md` - How to reproduce
- `CONTRIBUTING.md` - How to improve

---

**Guide Version**: 1.0  
**Last Updated**: 2024-06-29  
**Author**: Aurimas A. Nausėdas# Results Interpretation Guide / Rezultatų Interpretavimo Vadovas 📊

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