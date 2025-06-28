
# Lithuanian Energy Market Analysis (2024)

A fully reproducible project for the **uzduotis.pdf** assignment – from data to deploy‑as‑website.

## Quick start

```bash
git clone <repo-url>
cd lithuanian_energy_repo
conda env create -f env/environment.yml
conda activate lithuanian-energy-env
jupyter lab
```

## Run as dashboard

```bash
voila notebooks/lithuanian_energy_analysis.ipynb
```

## Static HTML site

```bash
./scripts/build_html.sh
python -m http.server -d docs
```

## Further reading

* Nord Pool – Pricing mechanics  
* Litgrid – Lithuanian TSO data  
* ENTSO‑E Transparency Platform  
* Lietuvos Energetikos Agentūra statistics
