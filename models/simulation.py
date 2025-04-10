import numpy as np
from typing import List, Dict
from models.schedule import ProcessingRun
from utils.constants import CELL_POPULATIONS, CV_SCALE_FACTOR

class CytometrySimulation:
    def __init__(self, realtime_cv: float = None):
        """
        Initialize cytometry data simulator.
        
        Args:
            realtime_cv: Overall CV for real-time mode. If None, uses default scale factor.
        """
        self.realtime_cv_scale = (realtime_cv / BATCH_MODE_MEDIAN_CV) if realtime_cv else CV_SCALE_FACTOR
        
    def _generate_values(self, true_value: float, cv: float, n_runs: int) -> np.ndarray:
        """Generate simulated values for a cell population."""
        std_dev = true_value * cv / 100
        return np.random.normal(true_value, std_dev, n_runs)
    
    def simulate_batch_mode(self, runs: List[ProcessingRun]) -> Dict[str, np.ndarray]:
        """Simulate values for batch mode processing."""
        results = {}
        for pop_id, pop_info in CELL_POPULATIONS.items():
            results[pop_id] = self._generate_values(
                pop_info.true_value,
                pop_info.batch_cv,
                len(runs)
            )
        return results
    
    def simulate_realtime_mode(self, runs: List[ProcessingRun]) -> Dict[str, np.ndarray]:
        """Simulate values for real-time mode processing."""
        results = {}
        for pop_id, pop_info in CELL_POPULATIONS.items():
            results[pop_id] = self._generate_values(
                pop_info.true_value,
                pop_info.batch_cv * self.realtime_cv_scale,
                len(runs)
            )
        return results 