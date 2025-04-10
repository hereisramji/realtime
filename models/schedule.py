from dataclasses import dataclass
from datetime import datetime
from typing import List, Tuple, Optional
import pandas as pd

@dataclass
class ProcessingRun:
    date: datetime
    sample_count: int
    accumulated_count: int

class SampleSchedule:
    def __init__(self, schedule_data: List[Tuple[str, int]]):
        """
        Initialize a sample schedule from a list of (date, count) tuples.
        
        Args:
            schedule_data: List of tuples containing (date_str, sample_count)
        """
        self.raw_schedule = schedule_data
        self.df = self._create_dataframe()
        
    def _create_dataframe(self) -> pd.DataFrame:
        """Convert raw schedule data to a pandas DataFrame with proper date parsing."""
        df = pd.DataFrame(self.raw_schedule, columns=['date', 'samples'])
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        return df
    
    @property
    def total_samples(self) -> int:
        """Get total number of samples in the schedule."""
        return self.df['samples'].sum()
    
    def get_realtime_runs(self) -> List[ProcessingRun]:
        """Generate processing runs for real-time mode."""
        runs = []
        accumulated = 0
        
        for _, row in self.df.iterrows():
            accumulated += row['samples']
            runs.append(ProcessingRun(
                date=row['date'],
                sample_count=row['samples'],
                accumulated_count=accumulated
            ))
        
        return runs
    
    def get_batch_runs(self, batch_size: int) -> List[ProcessingRun]:
        """Generate processing runs for batch mode with given batch size."""
        runs = []
        accumulated = 0
        current_batch = 0
        
        for _, row in self.df.iterrows():
            current_batch += row['samples']
            accumulated += row['samples']
            
            if current_batch >= batch_size:
                runs.append(ProcessingRun(
                    date=row['date'],
                    sample_count=current_batch,
                    accumulated_count=accumulated
                ))
                current_batch = 0
        
        # Handle remaining samples if any
        if current_batch > 0:
            runs.append(ProcessingRun(
                date=self.df.iloc[-1]['date'],
                sample_count=current_batch,
                accumulated_count=accumulated
            ))
        
        return runs
    
    @classmethod
    def validate_schedule_input(cls, schedule_text: str) -> Optional[List[Tuple[str, int]]]:
        """
        Validate schedule input text and convert to list of tuples.
        Returns None if validation fails.
        """
        try:
            schedule_data = []
            for line in schedule_text.strip().split('\n'):
                date_str, count_str = line.split(':')
                date_str = date_str.strip()
                count = int(count_str.strip())
                
                # Validate date format
                datetime.strptime(date_str, '%m/%d/%Y')
                
                if count <= 0:
                    return None
                    
                schedule_data.append((date_str, count))
            
            return schedule_data
        except (ValueError, TypeError):
            return None 