from typing import Dict, List, NamedTuple

class CellPopulation(NamedTuple):
    name: str
    true_value: float
    batch_cv: float

# Cell population configurations
CELL_POPULATIONS = {
    'CD3+': CellPopulation('T cells', 45.0, 0.4),
    'CD19+': CellPopulation('B cells', 7.0, 9.4),
    'CD14+HLADR-': CellPopulation('Monocytes', 8.0, 16.4),
    'CD14-HLADR-CD11b+CD33+': CellPopulation('e-MDSC', 0.5, 44.7),
    'CD56+': CellPopulation('NK cells', 7.0, 7.7)
}

# Default schedule as a list of tuples (date, count)
DEFAULT_SCHEDULE = [
    ('1/1/2025', 4),
    ('1/3/2025', 5),
    ('1/5/2025', 2),
    ('1/7/2025', 2),
    ('1/12/2025', 2),
    ('1/17/2025', 4),
    ('1/21/2025', 5),
    ('1/24/2025', 1),
    ('1/27/2025', 5),
    ('1/29/2025', 5),
    ('1/31/2025', 9)
]

# Processing parameters
DEFAULT_BATCH_SIZE = 20
DEFAULT_REALTIME_CV = 7.21
DEFAULT_BATCH_CV = 4.56
CV_SCALE_FACTOR = DEFAULT_REALTIME_CV / DEFAULT_BATCH_CV

# Visualization settings
COLORS = {
    'batch': 'blue',
    'realtime': 'orange',
    'true_value': 'red'
}

PLOT_Y_MARGIN = 0.1  # ±10% around true value 