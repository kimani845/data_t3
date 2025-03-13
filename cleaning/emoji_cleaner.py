import re
import pandas as pd

class EmojiCleaner:
    def __init__(self):
        # Pattern to match emojis and other unicode emoticons
        self.emoji_pattern = re.compile(
            "["
            "\U0001F1E0-\U0001F1FF"  # flags (iOS)
            "\U0001F300-\U0001F5FF"  # symbols & pictographs
            "\U0001F600-\U0001F64F"  # emoticons
            "\U0001F680-\U0001F6FF"  # transport & map symbols
            "\U0001F700-\U0001F77F"  # alchemical symbols
            "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
            "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
            "\U0001FA00-\U0001FA6F"  # Chess Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
            "\U00002702-\U000027B0"  # Dingbats
            "\U000024C2-\U0001F251" 
            "]+", flags=re.UNICODE)
    
    def remove_from_text(self, text):
        """Remove emojis from a single text string."""
        if pd.isna(text):
            return text
        return self.emoji_pattern.sub(r'', str(text)).strip()
    
    def remove_from_series(self, series):
        """Remove emojis from a pandas Series."""
        return series.apply(self.remove_from_text)
    
    def remove_from_dataframe(self, dataset, columns=None):
        """Remove emojis from specified DataFrame columns."""
        dataset = dataset.copy()
        
        if columns is None:
            columns = dataset.select_dtypes(include=['object']).columns
            
        for col in columns:
            if col in dataset.columns:
                dataset[col] = self.remove_from_series(dataset[col])
                
        return dataset

