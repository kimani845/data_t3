import pandas as pd
import re
import numpy as np

def clean_whitespace(value):
    if isinstance(value, str):
        # Remove non-breaking spaces, Unicode spaces, and multiple spaces
        cleaned_value = re.sub(r'[\s\u200b\u200c\u200d\u202f\xa0]+', ' ', value).strip()
   
        return cleaned_value if cleaned_value else np.nan  # Replace empty with NaN
    #strp extras
        
    return value