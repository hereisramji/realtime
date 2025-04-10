# Cytometry Data Visualization

A Streamlit-based web application for visualizing simulated cytometry data, comparing Batch Mode and Real-Time Mode processing strategies. The application allows users to customize sample collection schedules and processing parameters while visualizing the impact on various cell populations.

## Features

- **Interactive Sample Schedule**: Customize the sample collection schedule with dates and sample counts
- **Adjustable Processing Parameters**:
  - Batch size for batch mode processing
  - Coefficient of variation for real-time mode
- **Visualization**:
  - Scatter plots for five cell populations
  - Point sizes proportional to sample counts
  - True value reference lines
  - Inter-run variability statistics
- **Summary Statistics**:
  - Mean values
  - Deviation from true values
  - Coefficients of variation
  - Run counts

## Cell Populations

The application simulates data for five cell populations measured by flow cytometry:
- CD3+ (T cells)
- CD19+ (B cells)
- CD14+HLADR- (Monocytes)
- CD14-HLADR-CD11b+CD33+ (e-MDSC)
- CD56+ (NK cells)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

3. Use the sidebar controls to:
   - Modify the sample collection schedule
   - Adjust the batch size
   - Change the real-time mode CV

## Input Format

The sample collection schedule should be entered in the following format:
```
MM/DD/YYYY: count
```

Example:
```
1/1/2025: 4
1/3/2025: 5
1/5/2025: 2
```

## Requirements

- Python 3.8 or higher
- Streamlit 1.28.0 or higher
- Pandas 2.0.0 or higher
- NumPy 1.24.0 or higher
- Matplotlib 3.7.0 or higher
- Seaborn 0.12.0 or higher