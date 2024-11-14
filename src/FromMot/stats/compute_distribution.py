from typing import List, Dict
import pandas as pd
from src.FromMot.text_processing import reverse_word_if_hebrew

def compute_distribution(df: pd.DataFrame, columns: List[str]) -> Dict[str, pd.DataFrame]:
    distribution = {}

    for column in columns:
        if column in df.columns and df[column].notna().any():
            counts = df[column].value_counts(dropna=False, sort=True)
            percentages = (counts / counts.sum()) * 100
            distribution[column] = pd.DataFrame({
                'Count': counts,
                'Percentage': percentages.round(2)
            })
            print(f"Computed distribution for column: {column}")
        else:
            print(f"Column '{column}' not found in DataFrame or contains only NaN values.")
    return distribution
