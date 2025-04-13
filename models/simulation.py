import numpy as np
from typing import List, Dict
from models.schedule import ProcessingRun
import utils.constants as constants

class CytometrySimulation:
    def __init__(self, batch_cv: float = None, realtime_cv: float = None):
        """
        Initialize cytometry data simulator.
        
        Args:
            batch_cv: Overall CV for batch mode. If None, uses default value.
            realtime_cv: Overall CV for real-time mode. If None, uses default value.
        """
        self.batch_cv = batch_cv if batch_cv is not None else constants.DEFAULT_BATCH_CV
        self.realtime_cv = realtime_cv if realtime_cv is not None else constants.DEFAULT_REALTIME_CV
        self.realtime_cv_scale = self.realtime_cv / self.batch_cv
        
    def _generate_values(self, true_value: float, cv: float, n_runs: int) -> np.ndarray:
        """Generate simulated values for a cell population."""
        std_dev = true_value * cv / 100
        return np.random.normal(true_value, std_dev, n_runs)
    
    def simulate_batch_mode(self, runs: List[ProcessingRun]) -> Dict[str, np.ndarray]:
        """Simulate values for batch mode processing."""
        results = {}
        for pop_id, pop_info in constants.CELL_POPULATIONS.items():
            scaled_cv = (pop_info.batch_cv / constants.DEFAULT_BATCH_CV) * self.batch_cv
            results[pop_id] = self._generate_values(
                pop_info.true_value,
                scaled_cv,
                len(runs)
            )
        return results
    
    def simulate_realtime_mode(self, runs: List[ProcessingRun]) -> Dict[str, np.ndarray]:
        """Simulate values for real-time mode processing."""
        results = {}
        for pop_id, pop_info in constants.CELL_POPULATIONS.items():
            scaled_cv = (pop_info.batch_cv / constants.DEFAULT_BATCH_CV) * self.batch_cv * self.realtime_cv_scale
            results[pop_id] = self._generate_values(
                pop_info.true_value,
                scaled_cv,
                len(runs)
            )
        return results 