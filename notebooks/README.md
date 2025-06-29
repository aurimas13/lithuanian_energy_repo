# Analysis Notebooks / Analizės Užrašai 📓

This directory contains Jupyter notebooks with the complete Lithuanian electricity market analysis for 2024.

Šiame kataloge yra Jupyter užrašai su pilna Lietuvos elektros rinkos analize 2024 metams.

## 📚 Notebook Structure / Užrašų Struktūra

### 🎯 lithuanian_energy_analysis.ipynb
**Complete Analysis / Pilna Analizė**
- Runtime: ~5 minutes / Vykdymo laikas: ~5 minutės
- Memory: ~2GB RAM
- Contains all three analysis parts / Turi visas tris analizės dalis

**Sections / Skyriai:**
1. Data Loading & Preparation / Duomenų Įkėlimas ir Paruošimas
2. Part I - System Imbalance Analysis / I Dalis - Sistemos Disbalanso Analizė
3. Part II - Battery Trading Optimization / II Dalis - Baterijų Prekybos Optimizavimas
4. Part III - Demand Elasticity Study / III Dalis - Paklausos Elastingumo Tyrimas
5. Conclusions & Export / Išvados ir Eksportas

### 📊 01_imbalance_analysis.ipynb
**System Imbalance Deep Dive / Sistemos Disbalanso Detali Analizė**
- Focus: Imbalance patterns and trading strategies
- Outputs: 5 figures, 2 tables
- Key findings: Evening deficits, morning surpluses

### 🔋 02_battery_optimization.ipynb
**Battery Storage Strategies / Baterijų Saugojimo Strategijos**
- Focus: Economic optimization of battery operation
- Outputs: 4 figures, 3 tables
- Key findings: 4.2-year payback, 15.2% ROI

### 📈 03_demand_elasticity.ipynb
**Consumer Behavior Analysis / Vartotojų Elgsenos Analizė**
- Focus: Price responsiveness of electricity demand
- Outputs: 6 figures, 2 tables
- Key findings: -0.23 elasticity, limited DR potential

## 🚀 Running the Notebooks / Užrašų Paleidimas

### Quick Start / Greitas Startas
```bash
# Activate environment / Aktyvuoti aplinką
source venv/bin/activate  # Linux/Mac
# or / arba
venv\Scripts\activate  # Windows

# Start Jupyter / Paleisti Jupyter
jupyter notebook

# Open lithuanian_energy_analysis.ipynb / Atidaryti lithuanian_energy_analysis.ipynb
```

### Requirements / Reikalavimai
- Python 3.8+
- All packages in requirements.txt
- Data extracted from data/data.zip

### Execution Order / Vykdymo Tvarka
1. Run all cells sequentially / Paleisti visas ląsteles iš eilės
2. Wait for each section to complete / Palaukti kol kiekviena dalis baigsis
3. Results auto-save to results/ / Rezultatai automatiškai išsaugomi results/

## 📝 Notebook Features / Užrašų Funkcijos

### Interactive Elements / Interaktyvūs Elementai
- Adjustable parameters in each section
- Real-time plot updates
- Inline documentation

### Output Management / Išvesties Valdymas
- Automatic figure saving to `results/figures/`
- Table export to `results/tables/`
- JSON results in `results/`

### Code Organization / Kodo Organizavimas
- Modular sections for easy modification
- Clear variable naming (English/Lithuanian)
- Comprehensive comments

## 🔧 Customization / Pritaikymas

### Changing Parameters / Parametrų Keitimas
Each notebook has a "Configuration" section where you can modify:
- Analysis periods / Analizės laikotarpiai
- Battery specifications / Baterijų specifikacijos
- Statistical thresholds / Statistiniai slenkščiai
- Visualization styles / Vizualizacijos stiliai

### Adding New Analysis / Naujos Analizės Pridėjimas
1. Copy template from `notebook_template.ipynb`
2. Import required functions from `src/`
3. Follow existing structure
4. Update this README

## 📊 Expected Outputs / Laukiami Rezultatai

### Figures Generated / Sugeneruoti Grafikai
Total: 15 high-resolution plots
- System imbalance patterns (3)
- Price-quantity relationships (2)
- Battery optimization results (4)
- Demand elasticity analysis (6)

### Tables Generated / Sugeneruotos Lentelės
Total: 7 CSV files
- Hourly statistics summary
- Trading strategy results
- Battery strategy comparison
- Elasticity estimates
- Investment analysis
- Demand response scenarios
- Final metrics summary

### Text Reports / Tekstinės Ataskaitos
- `conclusions_lt.txt` - Lithuanian conclusions
- `conclusions_en.txt` - English conclusions
- `final_report.md` - Formatted report

## 🐛 Troubleshooting / Trikčių Šalinimas

### Common Issues / Dažnos Problemos

1. **Memory Error**
   - Solution: Restart kernel and run in sections
   - Sprendimas: Perkrauti branduolį ir vykdyti dalimis

2. **Missing Data Files**
   - Solution: Extract data.zip in data/ directory
   - Sprendimas: Išpakuoti data.zip data/ kataloge

3. **Import Errors**
   - Solution: Ensure venv is activated and packages installed
   - Sprendimas: Įsitikinti kad venv aktyvuota ir paketai įdiegti

4. **Plotting Issues**
   - Solution: Update matplotlib backend settings
   - Sprendimas: Atnaujinti matplotlib backend nustatymus

## 📖 Best Practices / Geriausia Praktika

1. **Before Running / Prieš Paleidžiant**
   - Clear previous outputs / Išvalyti ankstesnes išvestis
   - Check data availability / Patikrinti duomenų prieinamumą
   - Set working directory / Nustatyti darbo katalogą

2. **During Analysis / Analizės Metu**
   - Monitor memory usage / Stebėti atminties naudojimą
   - Save intermediate results / Išsaugoti tarpinius rezultatus
   - Document any changes / Dokumentuoti pakeitimus

3. **After Completion / Po Užbaigimo**
   - Verify all outputs generated / Patikrinti visas išvestis
   - Review log messages / Peržiūrėti log pranešimus
   - Commit results if needed / Commit rezultatus jei reikia

## 🔗 Related Resources / Susiję Ištekliai

- [Data Documentation](../data/README.md)
- [Results Interpretation](../results/README.md)
- [Source Code](../src/)
- [API Reference](../docs/api_reference.md)

---

💡 **Tip**: For faster execution, run individual part notebooks instead of lithuanian_energy_analysis.ipynb  
💡 **Patarimas**: Greitesniam vykdymui, paleiskite atskirus dalių užrašus vietoj lithuanian_energy_analysis.ipynb
