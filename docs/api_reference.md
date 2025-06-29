# API Reference / API Nuoroda 📚

Complete documentation of all functions used in the Lithuanian electricity market analysis.

Pilna visų Lietuvos elektros rinkos analizėje naudojamų funkcijų dokumentacija.

## Table of Contents / Turinys

1. [Data Loading Functions / Duomenų Įkėlimo Funkcijos](#data-loading-functions--duomenų-įkėlimo-funkcijos)
2. [Data Processing Functions / Duomenų Apdorojimo Funkcijos](#data-processing-functions--duomenų-apdorojimo-funkcijos)
3. [Imbalance Analysis Functions / Disbalanso Analizės Funkcijos](#imbalance-analysis-functions--disbalanso-analizės-funkcijos)
4. [Battery Optimization Functions / Baterijų Optimizavimo Funkcijos](#battery-optimization-functions--baterijų-optimizavimo-funkcijos)
5. [Elasticity Analysis Functions / Elastingumo Analizės Funkcijos](#elasticity-analysis-functions--elastingumo-analizės-funkcijos)
6. [Visualization Functions / Vizualizacijos Funkcijos](#visualization-functions--vizualizacijos-funkcijos)
7. [Utility Functions / Pagalbinės Funkcijos](#utility-functions--pagalbinės-funkcijos)

---

## Data Loading Functions / Duomenų Įkėlimo Funkcijos

### `load_all_data(data_dir: str) -> dict`

Load all data files from the specified directory.

Įkelti visus duomenų failus iš nurodyto katalogo.

**Parameters / Parametrai:**
- `data_dir` (str): Path to data directory / Kelias į duomenų katalogą

**Returns / Grąžina:**
- `dict`: Dictionary containing all dataframes / Žodynas su visais dataframes

**Example / Pavyzdys:**
```python
data = load_all_data('data/')
balancing_df = data['balancing']
prices_df = data['prices']
```

### `standardize_columns(df: pd.DataFrame) -> pd.DataFrame`

Standardize column names across different data sources.

Standartizuoti stulpelių pavadinimus skirtinguose duomenų šaltiniuose.

**Parameters / Parametrai:**
- `df` (pd.DataFrame): Input dataframe / Įvesties dataframe

**Returns / Grąžina:**
- `pd.DataFrame`: Dataframe with standardized columns / Dataframe su standartizuotais stulpeliais

**Column Mappings / Stulpelių Atitikmenys:**
- Various price columns → `price_EUR_MWh`
- Various quantity columns → `quantity_MWh`
- Various time columns → `timestamp`

---

## Data Processing Functions / Duomenų Apdorojimo Funkcijos

### `clean_timeseries(df: pd.DataFrame, freq: str = 'H') -> pd.DataFrame`

Clean and regularize time series data.

Išvalyti ir reguliarizuoti laiko eilučių duomenis.

**Parameters / Parametrai:**
- `df` (pd.DataFrame): Raw time series data / Neapdoroti laiko eilučių duomenys
- `freq` (str): Frequency string / Dažnio eilutė (default: 'H' for hourly)

**Returns / Grąžina:**
- `pd.DataFrame`: Cleaned time series / Išvalytos laiko eilutės

**Processing Steps / Apdorojimo Žingsniai:**
1. Sort by timestamp / Rūšiuoti pagal laiko žymą
2. Set timestamp as index / Nustatyti laiko žymą kaip indeksą
3. Resample to regular frequency / Perdaryti į reguliarų dažnį
4. Forward fill missing values (max 2) / Užpildyti trūkstamas reikšmes

### `remove_outliers(series: pd.Series, method: str = 'IQR', threshold: float = 1.5) -> pd.Series`

Remove outliers from a series using specified method.

Pašalinti išskirtis iš serijos naudojant nurodytą metodą.

**Parameters / Parametrai:**
- `series` (pd.Series): Input data / Įvesties duomenys
- `method` (str): Method to use / Naudojamas metodas ('IQR' or 'zscore')
- `threshold` (float): Threshold parameter / Slenksčio parametras

**Returns / Grąžina:**
- `pd.Series`: Series without outliers / Serija be išskirčių

**Methods / Metodai:**
- **IQR**: Remove points outside Q1 - threshold×IQR, Q3 + threshold×IQR
- **zscore**: Remove points with |z-score| > threshold

---

## Imbalance Analysis Functions / Disbalanso Analizės Funkcijos

### `analyze_hourly_patterns(df: pd.DataFrame) -> pd.DataFrame`

Analyze system imbalance patterns by hour of day.

Analizuoti sistemos disbalanso modelius pagal paros valandą.

**Parameters / Parametrai:**
- `df` (pd.DataFrame): Balancing data with columns ['timestamp', 'quantity_MWh']

**Returns / Grąžina:**
- `pd.DataFrame`: Hourly statistics with columns:
  - `mean`: Average imbalance / Vidutinis disbalansas
  - `std`: Standard deviation / Standartinis nuokrypis
  - `count`: Number of observations / Stebėjimų skaičius
  - `ci95_low`: Lower 95% CI / Žemutinė 95% PI riba
  - `ci95_high`: Upper 95% CI / Viršutinė 95% PI riba
  - `is_significant`: Statistical significance / Statistinis reikšmingumas

### `calculate_autocorrelation(series: pd.Series, nlags: int = 48) -> dict`

Calculate ACF and PACF for time series.

Apskaičiuoti ACF ir PACF laiko eilutėms.

**Parameters / Parametrai:**
- `series` (pd.Series): Time series data / Laiko eilučių duomenys
- `nlags` (int): Number of lags / Vėlavimų skaičius

**Returns / Grąžina:**
- `dict`: Dictionary with keys:
  - `acf`: Autocorrelation values / Autokoreliacijos reikšmės
  - `pacf`: Partial autocorrelation values / Dalinės autokoreliacijos reikšmės
  - `ljung_box`: Ljung-Box test results / Ljung-Box testo rezultatai

### `analyze_price_quantity_relationship(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResults`

Analyze the relationship between imbalance price and quantity.

Analizuoti ryšį tarp disbalanso kainos ir kiekio.

**Parameters / Parametrai:**
- `df` (pd.DataFrame): Data with columns ['price_EUR_MWh', 'quantity_MWh']

**Returns / Grąžina:**
- `RegressionResults`: OLS regression results object

**Model Specification / Modelio Specifikacija:**
```
Price = β₀ + β₁ × Quantity + ε
```

### `develop_trading_strategy(df: pd.DataFrame, confidence_level: float = 0.75) -> pd.DataFrame`

Develop and backtest a trading strategy based on imbalance patterns.

Sukurti ir ištestuoti prekybos strategiją pagal disbalanso modelius.

**Parameters / Parametrai:**
- `df` (pd.DataFrame): Historical balancing data / Istoriniai balansavimo duomenys
- `confidence_level` (float): Confidence level for signals / Pasikliautinumo lygis signalams

**Returns / Grąžina:**
- `pd.DataFrame`: DataFrame with additional columns:
  - `position_MWh`: Trading position / Prekybos pozicija
  - `cashflow_EUR`: Hourly profit/loss / Valandinis pelnas/nuostolis
  - `cumulative_profit`: Cumulative P&L / Kaupiamasis P&L

---

## Battery Optimization Functions / Baterijų Optimizavimo Funkcijos

### `battery_heuristic_strategy(prices_df: pd.DataFrame, capacity_mwh: float = 2, power_mw: float = 1, cycles_per_day: int = 2, efficiency: float = 0.92) -> pd.DataFrame`

Implement heuristic battery operation strategy.

Įgyvendinti euristinę baterijų veikimo strategiją.

**Parameters / Parametrai:**
- `prices_df` (pd.DataFrame): Day-ahead prices / Kitos dienos kainos
- `capacity_mwh` (float): Battery energy capacity / Baterijos energijos talpa
- `power_mw` (float): Battery power rating / Baterijos galios įvertinimas
- `cycles_per_day` (int): Maximum daily cycles / Maksimalus dienos ciklų skaičius
- `efficiency` (float): Round-trip efficiency / Apskritimo efektyvumas

**Returns / Grąžina:**
- `pd.DataFrame`: Daily results with columns:
  - `date`: Date / Data
  - `profit`: Daily profit / Dienos pelnas
  - `charge_hours`: Charging hours / Krovimo valandos
  - `discharge_hours`: Discharging hours / Iškrovimo valandos

### `battery_perfect_forecast(prices_df: pd.DataFrame, capacity_mwh: float = 2, power_mw: float = 1, cycles_per_day: int = 2, efficiency: float = 0.92) -> pd.DataFrame`

Optimize battery operation with perfect price forecast.

Optimizuoti baterijos veikimą su tobula kainų prognoze.

**Parameters / Parametrai:**
- Same as `battery_heuristic_strategy`

**Returns / Grąžina:**
- Same structure as `battery_heuristic_strategy` with optimal scheduling

### `battery_flexible_optimization(prices_df: pd.DataFrame, capacity_mwh: float = 2, power_mw: float = 1, max_cycles_per_day: int = 2, efficiency: float = 0.92) -> pd.DataFrame`

Flexible battery optimization allowing variable daily cycles.

Lanksti baterijų optimizacija leidžianti kintamus dienos ciklus.

**Additional Features / Papildomos Funkcijos:**
- Variable cycles per day / Kintami ciklai per dieną
- Annual optimization / Metinė optimizacija
- MILP formulation / MILP formuluotė

---

## Elasticity Analysis Functions / Elastingumo Analizės Funkcijos

### `estimate_national_elasticity(df: pd.DataFrame) -> dict`

Estimate national-level price elasticity of demand.

Įvertinti nacionalinio lygio paklausos kainos elastingumą.

**Parameters / Parametrai:**
- `df` (pd.DataFrame): Data with columns ['timestamp', 'demand_MWh', 'price_EUR_MWh', 'avg_temperature']

**Returns / Grąžina:**
- `dict`: Results dictionary with keys:
  - `elasticity`: Price elasticity coefficient / Kainos elastingumo koeficientas
  - `std_error`: Standard error / Standartinė paklaida
  - `r_squared`: Model R² / Modelio R²
  - `model`: Full regression results / Pilni regresijos rezultatai

**Model Specification / Modelio Specifikacija:**
```
ln(Demand) = α + β₁×ln(Price) + β₂×Temperature + Controls + ε
```

### `analyze_object_heterogeneity(panel_df: pd.DataFrame) -> pd.DataFrame`

Analyze elasticity heterogeneity across consumer objects.

Analizuoti elastingumo heterogeniškumą tarp vartotojų objektų.

**Parameters / Parametrai:**
- `panel_df` (pd.DataFrame): Panel data with columns ['objectNumber', 'timestamp', 'amount', 'price_EUR_MWh']

**Returns / Grąžina:**
- `pd.DataFrame`: Object-level elasticities with columns:
  - `object_id`: Object identifier / Objekto identifikatorius
  - `elasticity`: Estimated elasticity / Įvertintas elastingumas
  - `std_error`: Standard error / Standartinė paklaida
  - `n_obs`: Number of observations / Stebėjimų skaičius
  - `avg_consumption`: Average consumption / Vidutinis suvartojimas

### `calculate_demand_response_potential(elasticity: float, base_demand: float, price_scenarios: list) -> pd.DataFrame`

Calculate potential demand response under different price scenarios.

Apskaičiuoti potencialų paklausos atsaką esant skirtingiems kainų scenarijams.

**Parameters / Parametrai:**
- `elasticity` (float): Price elasticity of demand / Paklausos kainos elastingumas
- `base_demand` (float): Baseline demand in MWh / Bazinė paklausa MWh
- `price_scenarios` (list): List of price increase percentages / Kainų padidėjimo procentų sąrašas

**Returns / Grąžina:**
- `pd.DataFrame`: DR potential for each scenario

---

## Visualization Functions / Vizualizacijos Funkcijos

### `plot_hourly_imbalance(hourly_stats: pd.DataFrame, save_path: str = None)`

Plot average hourly imbalance with confidence intervals.

Nubraižyti vidutinį valandinį disbalansą su pasikliautinumo intervalais.

**Parameters / Parametrai:**
- `hourly_stats` (pd.DataFrame): Output from `analyze_hourly_patterns()`
- `save_path` (str): Optional path to save figure / Neprivalomas kelias išsaugoti paveikslėlį

### `plot_trading_performance(strategy_df: pd.DataFrame, save_path: str = None)`

Plot cumulative trading strategy performance.

Nubraižyti kaupiamąjį prekybos strategijos rezultatą.

**Parameters / Parametrai:**
- `strategy_df` (pd.DataFrame): Output from `develop_trading_strategy()`
- `save_path` (str): Optional save path / Neprivalomas išsaugojimo kelias

### `plot_battery_comparison(results_dict: dict, save_path: str = None)`

Compare different battery operation strategies.

Palyginti skirtingas baterijų veikimo strategijas.

**Parameters / Parametrai:**
- `results_dict` (dict): Dictionary with strategy names as keys and results as values
- `save_path` (str): Optional save path / Neprivalomas išsaugojimo kelias

### `plot_elasticity_distribution(elasticity_df: pd.DataFrame, save_path: str = None)`

Plot distribution of elasticities across objects.

Nubraižyti elastingumo pasiskirstymą tarp objektų.

---

## Utility Functions / Pagalbinės Funkcijos

### `calculate_metrics(y_true: np.array, y_pred: np.array) -> dict`

Calculate various performance metrics.

Apskaičiuoti įvairius veiklos rodiklius.

**Returns / Grąžina:**
- `dict`: Dictionary with metrics:
  - `mae`: Mean Absolute Error
  - `rmse`: Root Mean Square Error
  - `mape`: Mean Absolute Percentage Error
  - `r2`: R-squared

### `convert_to_serializable(obj: Any) -> Any`

Convert numpy/pandas objects to JSON-serializable format.

Konvertuoti numpy/pandas objektus į JSON serializuojamą formatą.

**Handles / Apdoroja:**
- `np.integer` → `int`
- `np.floating` → `float`
- `np.ndarray` → `list`
- `pd.Timestamp` → `str`

### `create_results_summary(results_dict: dict, output_path: str)`

Create a formatted summary of all analysis results.

Sukurti formatuotą visų analizės rezultatų santrauką.

**Parameters / Parametrai:**
- `results_dict` (dict): Dictionary containing all results / Žodynas su visais rezultatais
- `output_path` (str): Path to save summary / Kelias išsaugoti santrauką

---

## Error Handling / Klaidų Valdymas

All functions implement consistent error handling:

Visos funkcijos įgyvendina nuoseklų klaidų valdymą:

```python
try:
    result = function_call()
except ValueError as e:
    logger.error(f"Value error in {function_name}: {e}")
    raise
except Exception as e:
    logger.error(f"Unexpected error in {function_name}: {e}")
    return None
```

---

## Type Hints / Tipų Užuominos

All functions use Python type hints for clarity:

Visos funkcijos naudoja Python tipų užuominas aiškumui:

```python
from typing import Dict, List, Tuple, Optional, Union

def example_function(
    data: pd.DataFrame,
    threshold: float = 0.5,
    method: Optional[str] = None
) -> Union[pd.DataFrame, None]:
    ...
```

---

**API Version**: 1.0  
**Last Updated**: 2024-06-29  
**Author**: Aurimas A. Nausėdas