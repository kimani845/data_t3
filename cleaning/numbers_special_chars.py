import re
import numpy as np

def remove_numeric_special(value):
    if isinstance(value, str):
        # Remove if value contains ONLY numbers & special characters
        if re.fullmatch(r"[\d\W]+", value):  
            return np.nan  # Convert to NaN for removal
    return value 