from summa import summarizer
import pandas as pd

def generate_summary(text):
    """Generate a summary of the given text using Summa."""
    summary = summarizer.summarize(text)
    return summary if summary else text
'''
def fill_missing_summaries(dataset, content_col="content", summary_col="summary"):
  
    dataset[summary_col] = dataset.apply(
        lambda row: generate_summary(row[content_col]) 
        if pd.isna(row[summary_col]) or row[summary_col].strip() == "" 
        else row[summary_col],
        axis=1
    )
    return dataset
'''