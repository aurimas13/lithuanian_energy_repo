#!/usr/bin/env python3
"""
Extract Figures and Tables from Jupyter Notebook
Ištraukti Grafikus ir Lenteles iš Jupyter Užrašo

This script extracts all matplotlib figures and pandas dataframes 
from your analysis notebook and saves them to the results directory.
"""

import os
import json
import base64
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import io

def extract_notebook_outputs(notebook_path, output_dir='results'):
    """
    Extract all figures and tables from a Jupyter notebook.
    
    Parameters
    ----------
    notebook_path : str
        Path to the .ipynb file
    output_dir : str
        Base directory for outputs (default: 'results')
    """
    
    # Create output directories
    figures_dir = Path(output_dir) / 'figures'
    tables_dir = Path(output_dir) / 'tables'
    figures_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    # Load notebook
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    figure_count = 0
    table_count = 0
    
    # Iterate through cells
    for cell_idx, cell in enumerate(notebook['cells']):
        if cell['cell_type'] == 'code' and 'outputs' in cell:
            
            # Look for matplotlib figures
            for output_idx, output in enumerate(cell['outputs']):
                
                # Handle different output types
                if 'data' in output:
                    
                    # Extract PNG images
                    if 'image/png' in output['data']:
                        figure_count += 1
                        
                        # Decode base64 image
                        img_data = base64.b64decode(output['data']['image/png'])
                        
                        # Try to determine figure name from cell source
                        fig_name = f'figure_{figure_count:02d}'
                        cell_source = ''.join(cell['source'])
                        
                        # Look for common figure naming patterns
                        if 'hourly' in cell_source and 'imbalance' in cell_source:
                            fig_name = 'hourly_imbalance_patterns'
                        elif 'autocorrelation' in cell_source or 'acf' in cell_source.lower():
                            fig_name = 'imbalance_autocorrelation'
                        elif 'price' in cell_source and 'quantity' in cell_source:
                            fig_name = 'price_quantity_relationship'
                        elif 'cumulative' in cell_source and 'profit' in cell_source:
                            fig_name = 'trading_cumulative_profit'
                        elif 'battery' in cell_source and 'comparison' in cell_source:
                            fig_name = 'battery_strategy_comparison'
                        elif 'elasticity' in cell_source and 'hour' in cell_source:
                            fig_name = 'elasticity_by_hour'
                        elif 'demand' in cell_source and 'temperature' in cell_source:
                            fig_name = 'demand_vs_temperature'
                        
                        # Save figure
                        fig_path = figures_dir / f'{fig_name}.png'
                        with open(fig_path, 'wb') as f:
                            f.write(img_data)
                        
                        print(f"Saved figure: {fig_path}")
                    
                    # Extract HTML tables (from pandas)
                    if 'text/html' in output['data']:
                        html_content = output['data']['text/html']
                        
                        # Check if it's a pandas DataFrame
                        if '<table' in html_content and 'dataframe' in html_content:
                            table_count += 1
                            
                            # Try to parse table name from cell
                            table_name = f'table_{table_count:02d}'
                            cell_source = ''.join(cell['source'])
                            
                            if 'hourly_stats' in cell_source:
                                table_name = 'hourly_imbalance_statistics'
                            elif 'strategy' in cell_source and 'results' in cell_source:
                                table_name = 'trading_strategy_results'
                            elif 'battery' in cell_source and 'comparison' in cell_source:
                                table_name = 'battery_strategy_comparison'
                            elif 'elasticity' in cell_source:
                                table_name = 'demand_elasticity_results'
                            
                            # Note: Can't directly convert HTML to CSV without parsing
                            # This would need additional logic to parse the HTML table
                            print(f"Found table: {table_name} (manual export needed)")

    print(f"\nExtraction complete!")
    print(f"Figures found: {figure_count}")
    print(f"Tables found: {table_count}")
    
    return figure_count, table_count


def save_current_figures(figures_dir='results/figures'):
    """
    Save all currently open matplotlib figures.
    Call this in your notebook after creating plots.
    """
    figures_dir = Path(figures_dir)
    figures_dir.mkdir(parents=True, exist_ok=True)
    
    # Define figure names based on your analysis
    figure_names = {
        1: 'hourly_imbalance_patterns',
        2: 'imbalance_autocorrelation', 
        3: 'price_quantity_relationship',
        4: 'trading_cumulative_profit',
        5: 'trading_monthly_performance',
        6: 'battery_strategy_comparison',
        7: 'battery_daily_profit_distribution',
        8: 'battery_price_spread_analysis',
        9: 'battery_cycle_optimization',
        10: 'demand_vs_price_national',
        11: 'elasticity_by_hour',
        12: 'demand_vs_temperature',
        13: 'elasticity_heterogeneity',
        14: 'demand_response_scenarios',
        15: 'consumer_load_profiles'
    }
    
    # Save all open figures
    for i in plt.get_fignums():
        fig = plt.figure(i)
        fig_name = figure_names.get(i, f'figure_{i:02d}')
        fig_path = figures_dir / f'{fig_name}.png'
        
        fig.savefig(fig_path, dpi=300, bbox_inches='tight', 
                    facecolor='white', edgecolor='none')
        print(f"Saved: {fig_path}")


def save_dataframe_to_csv(df, filename, tables_dir='results/tables'):
    """
    Save a pandas DataFrame to CSV with proper formatting.
    
    Parameters
    ----------
    df : pd.DataFrame
        DataFrame to save
    filename : str
        Name of the CSV file (without extension)
    tables_dir : str
        Directory to save tables
    """
    tables_dir = Path(tables_dir)
    tables_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = tables_dir / f'{filename}.csv'
    
    # Save with UTF-8 BOM for Excel compatibility
    df.to_csv(filepath, index=False, encoding='utf-8-sig', float_format='%.3f')
    print(f"Saved table: {filepath}")


# Example usage in your notebook:
"""
# Add this to your notebook cells after creating figures/tables:

# After creating imbalance statistics
save_dataframe_to_csv(hourly_stats, 'hourly_imbalance_statistics')

# After creating battery comparison
save_dataframe_to_csv(battery_comparison_df, 'battery_strategy_comparison')

# After creating all figures
save_current_figures()

# Or to extract from saved notebook:
extract_notebook_outputs('notebooks/main_analysis.ipynb')
"""

if __name__ == "__main__":
    # If run as script, extract from main analysis notebook
    notebook_path = 'notebooks/main_analysis.ipynb'
    if os.path.exists(notebook_path):
        extract_notebook_outputs(notebook_path)
    else:
        print(f"Notebook not found: {notebook_path}")
        print("Please run this script from the repository root directory.")