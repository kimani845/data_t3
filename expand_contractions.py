import contractions
import pandas as pd

def expand_contractions(text):
    """Expands contractions in text."""
    if pd.isna(text):
        return text
    return contractions.fix(str(text))
