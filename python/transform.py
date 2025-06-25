
import pandas as pd

def clean_any_csv(file_path, output_path=None):
    """
    Cleans any CSV file by:
    - Removing duplicates
    - Stripping whitespace from all string columns
    - Lowercasing all string columns

    Args:
        file_path (str): Path to the input CSV file.
        output_path (str, optional): Path to save the cleaned CSV file. If None, file is not saved.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    # Load the file
    df = pd.read_csv(file_path)
    original_count = len(df)

    # Remove duplicates
    df = df.drop_duplicates()

    # Clean all object/string-type columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.lower()

    cleaned_count = len(df)

    # Save if path provided
    if output_path:
        df.to_csv(output_path, index=False)

    print(f"File cleaned successfully. Removed {original_count - cleaned_count} duplicate rows.")
    return df

clean_any_csv("data/raw/test.csv","data/processed/output.csv")