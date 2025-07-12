import pandas as pd
from sqlalchemy import create_engine


def clean_and_store_data(csv_file_path, db_name='laptops.db', table_name='laptops'):
    """
    Reads data from a CSV file, cleans it, and stores it in an SQLite database.
    """
    try:
        # 1. Read the raw data from the CSV file
        df = pd.read_csv(csv_file_path)
        print("Successfully loaded data from laptops_data.csv")

    except FileNotFoundError:
        print(
            f"Error: The file {csv_file_path} was not found. Please run scraper.py first.")
        return

    # 2. Clean the data
    print("Starting data cleaning process...")

    # --- Clean the 'Price' column ---
    # Remove commas and convert to a numeric type (float)
    # We use .loc to avoid the SettingWithCopyWarning
    df.loc[:, 'Price'] = df['Price'].str.replace(',', '', regex=False)
    # Handle 'N/A' or other non-numeric values by turning them into NaN (Not a Number)
    df.loc[:, 'Price'] = pd.to_numeric(df['Price'], errors='coerce')

    # --- Clean the 'Rating' column ---
    # Convert to a numeric type (float)
    df.loc[:, 'Rating'] = pd.to_numeric(df['Rating'], errors='coerce')

    # --- Handle missing values ---
    # For this project, we will simply drop rows with missing price or name
    df.dropna(subset=['Price', 'Name'], inplace=True)
    # We can fill missing ratings with a default value, e.g., the median rating
    median_rating = df['Rating'].median()
    df['Rating'].fillna(median_rating, inplace=True)

    # Convert data types to be more memory efficient
    df['Price'] = df['Price'].astype(int)
    df['Rating'] = df['Rating'].astype(float)

    print("Data cleaning complete.")
    print("\nCleaned DataFrame sample:")
    print(df.head())
    print(f"\nTotal records after cleaning: {len(df)}")

    # 3. Store the cleaned data in an SQLite database
    print(f"Storing cleaned data into '{db_name}' in table '{table_name}'...")

    # Create a connection to the SQLite database
    # This will create the file 'laptops.db' if it doesn't exist
    engine = create_engine(f'sqlite:///{db_name}')

    # Write the DataFrame to the SQL table
    # `if_exists='replace'` will drop the table first if it exists and create a new one.
    # This is useful for re-running the script with fresh data.
    df.to_sql(table_name, engine, if_exists='replace', index=False)

    print(f"Data successfully stored in '{db_name}'.")


# To run this script directly
if __name__ == "__main__":
    clean_and_store_data('laptops_data.csv')
