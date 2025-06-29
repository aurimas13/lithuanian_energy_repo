# Data Dictionary / Duomenų Žodynas 📖

Complete variable definitions for all datasets used in the Lithuanian electricity market analysis.

Pilni kintamųjų apibrėžimai visiems Lietuvos elektros rinkos analizėje naudojamiems duomenų rinkiniams.

## Table of Contents / Turinys

1. [Raw Data Files / Neapdoroti Duomenų Failai](#raw-data-files--neapdoroti-duomenų-failai)
2. [Calculated Variables / Apskaičiuoti Kintamieji](#calculated-variables--apskaičiuoti-kintamieji)
3. [Output Variables / Išvesties Kintamieji](#output-variables--išvesties-kintamieji)
4. [Statistical Measures / Statistiniai Matai](#statistical-measures--statistiniai-matai)

---

## Raw Data Files / Neapdoroti Duomenų Failai

### 1. balancing_market_data.xlsx

| Column / Stulpelis | Type / Tipas | Description / Aprašymas | Unit / Vienetas | Range / Intervalas |
|-------------------|--------------|-------------------------|-----------------|-------------------|
| timestamp | datetime | Hour start time EET/EEST / Valandos pradžios laikas | YYYY-MM-DD HH:MM | 2024-01-01 00:00 to 2024-12-31 23:00 |
| quantity_MWh | float | System imbalance volume / Sistemos disbalanso kiekis | MWh | [-500, 500] |
| | | Negative = deficit (undersupply) / Neigiamas = trūkumas | | |
| | | Positive = surplus (oversupply) / Teigiamas = perteklius | | |
| price_EUR_MWh | float | Imbalance settlement price / Disbalanso atsiskaitymo kaina | EUR/MWh | [-500, 1000] |

**Data Quality Notes / Duomenų Kokybės Pastabos:**
- Missing values: <0.1% (interpolated)
- Outliers: Removed using IQR method (1.5×IQR)
- Time gaps: None (complete hourly series)

### 2. day_ahead_prices.xlsx

| Column / Stulpelis | Type / Tipas | Description / Aprašymas | Unit / Vienetas | Range / Intervalas |
|-------------------|--------------|-------------------------|-----------------|-------------------|
| timestamp | datetime | Delivery hour / Pristatymo valanda | YYYY-MM-DD HH:MM | 2024-01-01 00:00 to 2024-12-31 23:00 |
| price_EUR_MWh | float | Day-ahead market clearing price / Paros prekybos biržos kaina | EUR/MWh | [0, 500] |
| | | Nord Pool LT bidding zone / Nord Pool LT prekybos zona | | Typically 20-150 |

### 3. meteorological_data.xlsx

| Column / Stulpelis | Type / Tipas | Description / Aprašymas | Unit / Vienetas | Range / Intervalas |
|-------------------|--------------|-------------------------|-----------------|-------------------|
| time | datetime | Measurement hour / Matavimo valanda | YYYY-MM-DD HH:MM | 2024-01-01 00:00 to 2024-12-31 23:00 |
| avg_temperature | float | Lithuania average temperature / Lietuvos vidutinė temperatūra | °C | [-30, 35] |
| | | Population-weighted average / Svertinis vidurkis pagal gyventojus | | |
| avg_ghi | float | Average global horizontal irradiance / Vidutinė horizontali saulės spinduliuotė | W/m² | [0, 1000] |
| | | Clear sky maximum ~1000 / Giedro dangaus maksimumas ~1000 | | |

### 4. national_consumption.xls

| Column / Stulpelis | Type / Tipas | Description / Aprašymas | Unit / Vienetas | Range / Intervalas |
|-------------------|--------------|-------------------------|-----------------|-------------------|
| timestamp | datetime | Consumption hour / Suvartojimo valanda | YYYY-MM-DD HH:MM | 2024-01-01 00:00 to 2024-12-31 23:00 |
| demand_MWh | float | Total national electricity consumption / Bendras nacionalinis elektros suvartojimas | MWh | [600, 2000] |
| | | Measured at transmission level / Matuojama perdavimo lygmenyje | | |
| | | Includes losses / Įskaitant nuostolius | | |

### 5. object_level_consumption (Parquet)

| Column / Stulpelis | Type / Tipas | Description / Aprašymas | Unit / Vienetas | Range / Intervalas |
|-------------------|--------------|-------------------------|-----------------|-------------------|
| consumptionTime | datetime | Measurement timestamp / Matavimo laiko žyma | YYYY-MM-DD HH:MM | 2024-01-01 00:00 to 2024-12-31 23:00 |
| amount | float | Hourly electricity consumption / Valandinis elektros suvartojimas | kWh | [0, 10000] |
| objectNumber | int | Anonymized consumer ID / Anonimizuotas vartotojo ID | - | [1, 111] |
| | | Business customers only / Tik verslo klientai | | |

---

## Calculated Variables / Apskaičiuoti Kintamieji

### Time-based Features / Laiko Požymiai

| Variable / Kintamasis | Formula | Description / Aprašymas | Range / Intervalas |
|----------------------|---------|-------------------------|-------------------|
| hour | timestamp.hour | Hour of day / Paros valanda | [0, 23] |
| date | timestamp.date | Calendar date / Kalendorinė data | 2024-01-01 to 2024-12-31 |
| weekday | timestamp.weekday | Day of week / Savaitės diena | [0, 6] (Mon=0, Sun=6) |
| month | timestamp.month | Month / Mėnuo | [1, 12] |
| quarter | timestamp.quarter | Quarter / Ketvirtis | [1, 4] |
| is_weekend | weekday >= 5 | Weekend indicator / Savaitgalio indikatorius | {0, 1} |
| is_peak | hour in [17,18,19,20] | Peak hours indicator / Piko valandų indikatorius | {0, 1} |

### Transformed Variables / Transformuoti Kintamieji

| Variable / Kintamasis | Formula | Description / Aprašymas | Purpose / Tikslas |
|----------------------|---------|-------------------------|-------------------|
| log_price | ln(price) | Natural log of price / Natūrinis kainos logaritmas | Elasticity estimation |
| log_demand | ln(demand) | Natural log of demand / Natūrinis paklausos logaritmas | Constant elasticity |
| log_consumption | ln(consumption) | Natural log of consumption / Natūrinis suvartojimo logaritmas | Panel regression |
| price_spread | max(price) - min(price) | Daily price spread / Dienos kainų skirtumas | Battery profitability |
| lag_quantity | quantity.shift(1) | Previous hour imbalance / Ankstesnės valandos disbalansas | Autoregression |
| lag_price | price.shift(1) | Previous hour price / Ankstesnės valandos kaina | Trading signals |

---

## Output Variables / Išvesties Kintamieji

### Statistical Results / Statistiniai Rezultatai

| Variable / Kintamasis | Description / Aprašymas | Interpretation / Interpretacija |
|----------------------|-------------------------|--------------------------------|
| mean_imbalance | Average hourly imbalance / Vidutinis valandinis disbalansas | >0: typical surplus, <0: typical deficit |
| std_imbalance | Standard deviation of imbalance / Disbalanso standartinis nuokrypis | Higher = more volatility |
| ci95_low | Lower 95% confidence bound / Žemutinė 95% pasikliautinumo riba | True mean likely above this |
| ci95_high | Upper 95% confidence bound / Viršutinė 95% pasikliautinumo riba | True mean likely below this |
| is_significant | Statistical significance flag / Statistinio reikšmingumo žymė | TRUE if CI doesn't include 0 |

### Financial Metrics / Finansiniai Rodikliai

| Variable / Kintamasis | Formula | Description / Aprašymas | Unit / Vienetas |
|----------------------|---------|-------------------------|-----------------|
| position_MWh | Trading algorithm output | Trading position / Prekybos pozicija | MWh |
| cashflow_EUR | position × price | Hourly profit/loss / Valandinis pelnas/nuostolis | EUR |
| cumulative_profit | Σ(cashflow) | Running total P&L / Kaupiamasis P&L | EUR |
| annual_profit | Σ(daily_profit) | Total yearly profit / Bendras metinis pelnas | EUR |
| roi_pct | (profit - costs) / investment × 100 | Return on investment / Investicijų grąža | % |
| payback_years | investment / annual_cashflow | Simple payback period / Paprastas atsipirkimo laikotarpis | years |
| npv | -CAPEX + Σ(CF/(1+r)^t) | Net present value / Grynoji dabartinė vertė | EUR |
| irr | Rate where NPV = 0 | Internal rate of return / Vidinė grąžos norma | % |

### Elasticity Measures / Elastingumo Matai

| Variable / Kintamasis | Description / Aprašymas | Typical Values / Tipinės Reikšmės |
|----------------------|-------------------------|-----------------------------------|
| price_elasticity | ∂ln(Q)/∂ln(P) | -0.05 to -0.5 for electricity |
| std_error | Standard error of elasticity / Elastingumo standartinė paklaida | ±0.02 to ±0.10 |
| r_squared | Model fit measure / Modelio tinkamumo matas | 0.3 to 0.6 typical |
| temp_coefficient | ∂ln(Q)/∂T | ~0.02 (2% per °C) |

---

## Statistical Measures / Statistiniai Matai

### Descriptive Statistics / Aprašomoji Statistika

| Measure / Matas | Formula | Use Case / Naudojimo Atvejis |
|----------------|---------|------------------------------|
| Mean | Σx/n | Central tendency / Centrinė tendencija |
| Median | 50th percentile | Robust central measure / Atsparus centrinis matas |
| Std Dev | √(Σ(x-μ)²/n) | Variability / Kintamumas |
| Skewness | E[(X-μ)³]/σ³ | Distribution shape / Pasiskirstymo forma |
| Kurtosis | E[(X-μ)⁴]/σ⁴ | Tail heaviness / Uodegų svoris |

### Test Statistics / Testo Statistikos

| Test / Testas | Null Hypothesis / Nulinė Hipotezė | Decision Rule / Sprendimo Taisyklė |
|--------------|-----------------------------------|-----------------------------------|
| t-test | μ = 0 | Reject if |t| > t_critical |
| Kruskal-Wallis | Distributions equal / Pasiskirstymai lygūs | Reject if p < 0.05 |
| Ljung-Box | No autocorrelation / Nėra autokoreliacijos | Reject if p < 0.05 |
| Breusch-Pagan | Homoskedasticity / Homoskedastiškumas | Reject if p < 0.05 |

---

## Data Quality Flags / Duomenų Kokybės Žymės

| Flag / Žymė | Meaning / Reikšmė | Action / Veiksmas |
|-------------|-------------------|-------------------|
| validated | Data verified by source / Duomenys patikrinti šaltinio | Use as-is / Naudoti kaip yra |
| estimated | Value estimated, not measured / Reikšmė įvertinta, ne išmatuota | Use with caution / Naudoti atsargiai |
| interpolated | Missing value filled / Trūkstama reikšmė užpildyta | Check sensitivity / Tikrinti jautrumą |
| outlier_removed | Extreme value excluded / Kraštutinė reikšmė pašalinta | Document in results / Dokumentuoti rezultatuose |

---

**Dictionary Version**: 2.0  
**Last Updated**: 2024-06-29  
**Maintained by**: Aurimas A. Nausėdas

For questions about specific variables, see the relevant notebook section or contact the maintainer.
