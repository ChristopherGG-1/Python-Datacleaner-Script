import pandas as pd
import argparse

# To run in CLI, python clean_data.py raw_data.csv cleaned_data.csv


def load_data(file_path: str) -> pd.DataFrame:
    """Load CSV data into a DataFrame."""
    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare raw data for analysis/modeling."""

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Standardize column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # Clean email column
    if "email" in df.columns:
        df["email"] = df["email"].astype(str).str.lower().str.strip()
        df = df[df["email"].str.contains("@", na=False)]

    # Clean name column
    if "name" in df.columns:
        df["name"] = df["name"].astype(str).str.strip().str.title()

    # Clean state column
    if "state" in df.columns:
        df["state"] = df["state"].astype(str).str.strip().str.upper()

    # Clean age column
    if "age" in df.columns:
        df["age"] = pd.to_numeric(df["age"], errors="coerce")
        df["age"] = df["age"].fillna(df["age"].median())
        df = df[(df["age"] > 0) & (df["age"] < 100)]

    # Convert date columns
    for col in df.columns:
        if "date" in col:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    return df


def save_data(df: pd.DataFrame, output_path: str) -> None:
    """Save cleaned DataFrame to CSV."""
    df.to_csv(output_path, index=False)


def main():
    parser = argparse.ArgumentParser(description="Clean raw CSV data using pandas.")
    parser.add_argument("input", help="Path to raw input CSV file")
    parser.add_argument("output", help="Path to save cleaned CSV file")

    args = parser.parse_args()

    df = load_data(args.input)
    cleaned_df = clean_data(df)
    save_data(cleaned_df, args.output)

    print(f"Cleaned data saved to {args.output}")
    print(f"Rows after cleaning: {len(cleaned_df)}")
    print(f"Columns: {list(cleaned_df.columns)}")


if __name__ == "__main__":
    main()