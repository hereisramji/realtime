import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from typing import Dict, List
from models.schedule import ProcessingRun
from utils.constants import CELL_POPULATIONS, COLORS, PLOT_Y_MARGIN

def create_population_plots(
    batch_runs: List[ProcessingRun],
    realtime_runs: List[ProcessingRun],
    batch_results: Dict[str, np.ndarray],
    realtime_results: Dict[str, np.ndarray]
) -> plt.Figure:
    """Create scatter plots for all cell populations."""
    fig = plt.figure(figsize=(15, 10))
    
    for idx, (pop_id, pop_info) in enumerate(CELL_POPULATIONS.items(), 1):
        ax = plt.subplot(2, 3, idx)
        
        # Plot batch mode points
        batch_x = np.repeat(0.0, len(batch_runs))
        batch_x += np.random.normal(0, 0.05, len(batch_runs))  # Add jitter
        ax.scatter(
            batch_x,
            batch_results[pop_id],
            s=[run.sample_count * 20 for run in batch_runs],
            alpha=0.6,
            color=COLORS['batch'],
            label='Batch Mode'
        )
        
        # Plot real-time mode points
        rt_x = np.repeat(1.0, len(realtime_runs))
        rt_x += np.random.normal(0, 0.05, len(realtime_runs))  # Add jitter
        ax.scatter(
            rt_x,
            realtime_results[pop_id],
            s=[run.sample_count * 20 for run in realtime_runs],
            alpha=0.6,
            color=COLORS['realtime'],
            label='Real-Time Mode'
        )
        
        # Add true value line
        ax.axhline(
            y=pop_info.true_value,
            color=COLORS['true_value'],
            linestyle='--',
            alpha=0.5
        )
        
        # Set labels and title
        ax.set_title(f"{pop_id}\n({pop_info.name})")
        ax.set_xticks([0, 1])
        ax.set_xticklabels(['Batch', 'Real-Time'])
        ax.set_ylabel('Frequency (%)')
        
        # Set y-axis limits
        y_margin = pop_info.true_value * PLOT_Y_MARGIN
        ax.set_ylim(
            pop_info.true_value - y_margin,
            pop_info.true_value + y_margin
        )
        
        # Add CV annotations
        batch_cv = np.std(batch_results[pop_id]) / np.mean(batch_results[pop_id]) * 100
        rt_cv = np.std(realtime_results[pop_id]) / np.mean(realtime_results[pop_id]) * 100
        
        ax.annotate(
            f'Batch CV: {batch_cv:.1f}%\n(n={len(batch_runs)})',
            xy=(0, 1.02),
            xycoords='axes fraction',
            ha='center'
        )
        ax.annotate(
            f'RT CV: {rt_cv:.1f}%\n(n={len(realtime_runs)})',
            xy=(1, 1.02),
            xycoords='axes fraction',
            ha='center'
        )
        
        if idx == 1:  # Add legend to first subplot
            ax.legend(loc='upper right')
    
    plt.tight_layout()
    return fig

def create_summary_table(
    batch_runs: List[ProcessingRun],
    realtime_runs: List[ProcessingRun],
    batch_results: Dict[str, np.ndarray],
    realtime_results: Dict[str, np.ndarray]
) -> pd.DataFrame:
    """Create summary statistics table."""
    data = []
    
    for pop_id, pop_info in CELL_POPULATIONS.items():
        for mode, results, runs in [
            ('Batch', batch_results[pop_id], batch_runs),
            ('Real-Time', realtime_results[pop_id], realtime_runs)
        ]:
            mean_val = np.mean(results)
            cv = np.std(results) / mean_val * 100
            dev = (mean_val - pop_info.true_value) / pop_info.true_value * 100
            
            data.append({
                'Population': pop_id,
                'Mode': mode,
                'Mean (%)': f'{mean_val:.2f}',
                'Deviation (%)': f'{dev:+.2f}',
                'CV (%)': f'{cv:.2f}',
                'Runs': len(runs)
            })
    
    return pd.DataFrame(data) 