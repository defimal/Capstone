import pandas as pd

def transform_project_data(input_path='data/raw/test.csv', output_path='data/processed/output.csv'):
    # Load raw data
    df = pd.read_csv(input_path)
    print(df)
    # Clean column names
    df.columns = df.columns.str.strip()

    # Strip whitespace from string fields
    df = df.apply(lambda col: col.str.strip() if col.dtype == 'object' else col)

    # Flexible Date Column Handling
    date_col = next((col for col in df.columns if 'date' in col.lower()), None)
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')
        df = df[df[date_col].notnull()]
        df[date_col] = df[date_col].dt.strftime('%Y-%m-%d')

    # Standardize Status and filter
    status_col = next((col for col in df.columns if 'status' in col.lower()), None)
    if status_col:
        df[status_col] = df[status_col].str.lower().str.strip()
        df = df[df[status_col].isin(['thinking'])]  # Only keep rows with 'thinking'

    # Numeric fields (e.g., Budget, TeamSize)
    for col in ['Budget', 'TeamSize']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df = df[df[col].notnull()]
            df[col] = df[col].astype(int)

    # Save to cleaned file
    df.to_csv(output_path, index=False)
    print(f"Transformed data saved to {output_path}")

# Run
if __name__ == "__main__":
    transform_project_data()