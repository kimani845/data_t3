#!/usr/bin/env python3
import pandas as pd
import numpy as np
import re
import wordninja
import unicodedata
import logging
import os
import sys

# Set up logging to display info messages.
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def standardize_column_names(df):
    # Standardize column names: lowercase, remove spaces, use underscores, and remove non-word characters.
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r'\W', '', regex=True)
    return df

def clean_text(text):
    # Clean a block of text by removing references, HTML, extra spaces, and splitting concatenated words.
    if not isinstance(text, str):
        return text
    # Remove bracketed numbers (e.g., [1])
    text = re.sub(r'\[\d+\]', '', text)
    # Remove HTML tags if present
    text = re.sub(r'<.*?>', '', text)
    # Replace newlines and carriage returns with a space
    text = text.replace('\n', ' ').replace('\r', ' ')
    # Collapse multiple spaces into one
    text = re.sub(r'\s+', ' ', text)
    # Normalize unicode characters
    text = unicodedata.normalize("NFKD", text)
    # Trim whitespace
    text = text.strip()
    # Use WordNinja to split concatenated words
    text = ' '.join(wordninja.split(text))
    return text

def convert_numeric_columns(df):
    # Attempt to convert object-type columns to numeric values where possible.
    for col in df.columns:
        if df[col].dtype == 'object':
            try:
                df[col] = pd.to_numeric(df[col], errors='ignore')
            except Exception as e:
                logging.info(f"Could not convert column {col} to numeric: {e}")
    return df

def clean_dataset(file_path, key_columns, date_columns, output_file, missing_threshold=0.5):
    # Clean the dataset using a series of processing steps.
    try:
        # Load the dataset.
        df = pd.read_csv(file_path)
        logging.info(f"Loaded dataset with shape: {df.shape}")

        # Standardize column names.
        df = standardize_column_names(df)
        logging.info("Standardized column names.")

        # Drop columns with more than the allowed ratio of missing values.
        missing_ratio = df.isnull().mean()
        cols_to_drop = missing_ratio[missing_ratio > missing_threshold].index.tolist()
        if cols_to_drop:
            df.drop(columns=cols_to_drop, inplace=True)
            logging.info(f"Dropped columns with > {missing_threshold*100}% missing values: {cols_to_drop}")

        # If both 'url' and 'links' columns exist, drop the 'links' column.
        if "url" in df.columns and "links" in df.columns:
            df.drop(columns="links", inplace=True)
            logging.info("Dropped 'links' column because both 'url' and 'links' are present in the dataset.")
            # Also update key_columns to remove 'links'
            key_columns = [col for col in key_columns if col != "links"]

        # Drop rows with missing values in key columns.
        initial_rows = df.shape[0]
        df.dropna(subset=key_columns, inplace=True)
        logging.info(f"Dropped {initial_rows - df.shape[0]} rows with missing values in key columns: {key_columns}")

        # Remove duplicate rows based on each key column.
        for col in key_columns:
            if df[col].duplicated().any():
                before = df.shape[0]
                df.drop_duplicates(subset=[col], inplace=True)
                logging.info(f"Removed duplicates in '{col}', dropped {before - df.shape[0]} rows.")

        # Clean text columns: lowercase, trim, and apply text cleaning.
        for col in df.select_dtypes(include='object').columns:
            df[col] = df[col].str.lower().str.strip()
            df[col] = df[col].apply(clean_text)
        logging.info("Cleaned text columns.")

        # Convert date columns to datetime.
        for date_col in date_columns:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
                logging.info(f"Converted '{date_col}' to datetime.")

        # Attempt to convert numeric columns.
        df = convert_numeric_columns(df)
        logging.info("Converted numeric columns where possible.")

        # Replace empty strings with NaN and drop any rows with missing key column values.
        df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
        df.dropna(subset=key_columns, inplace=True)

        # Create output directory if it doesn't exist.
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            logging.info(f"Created output directory: {output_dir}")

        # Save the cleaned dataset.
        df.to_csv(output_file, index=False)
        logging.info(f"Cleaned dataset saved to {output_file} with shape: {df.shape}")

        return df

    except Exception as e:
        logging.error(f"Error cleaning dataset: {e}")
        sys.exit(1)

def main():
    input_file = "input/healthcare_analytics_data.csv"
    output_file = "output/healthcare_cleaned_data.csv"
    key_columns = ["title", "summary", "content", "links", "url"]
    date_columns = [""]
    missing_threshold = 0.5

    clean_dataset(
        file_path=input_file,
        key_columns=key_columns,
        date_columns=date_columns,
        output_file=output_file,
        missing_threshold=missing_threshold
    )
    print("Dataset cleaning complete.")

if __name__ == "__main__":
    main()
