import pandas as pd
from solution import add_virtual_column


def load_data(file: str) -> pd.DataFrame:
    """
        Loads data from file.
        Returns a dataframe.
    """
    df = pd.read_csv(file)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
       Load and clean sales data from a CSV file.

       Cleaning steps:
       1. Normalize column names.
       2. Remove empty rows, repeated headers and summary rows.
       3. Normalize string values.
       4. Convert numeric columns.
       5. Remove exact duplicates.
       6. Impute missing Unit Price values using Product.
       7. Replace missing Discount values with 0.
       8. Convert Order Date to datetime.

       Returns:
           pd.DataFrame: Cleaned sales data.
    """

    # --------------------------------------------------
    # 1. Normalize column names
    # --------------------------------------------------
    df.columns = df.columns.str.strip()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\s+", "_", regex=True)
    )

    # --------------------------------------------------
    # 2. Normalize string values
    # --------------------------------------------------
    string_columns = [
        "order_id",
        "region",
        "product",
        "quantity",
        "unit_price",
        "discount",
        "order_date"
    ]

    for column in string_columns:
        df[column] = df[column].astype("string").str.strip()

        # Convert empty strings to missing values
        df[column] = df[column].replace("", pd.NA)

    # Normalize region capitalization
    df["region"] = df["region"].str.title()

    # --------------------------------------------------
    # 3. Remove invalid rows
    # --------------------------------------------------
    # Remove completely empty rows
    df = df.dropna(how="all")

    # Remove summary/footer row
    df = df[df["order_id"].str.upper() != "TOTAL"]

    # Remove repeated header rows
    df = df[df["order_id"].str.upper() != "ORDER ID"]

    # --------------------------------------------------
    # 4. Normalize numeric formatting
    # --------------------------------------------------
    # Remove spaces used as thousands separators
    df["quantity"] = (df["quantity"].str.replace(" ", "", regex=False))

    # Normalize decimal separators
    for column in ["unit_price", "discount"]:
        df[column] = (df[column].str.replace(",", ".", regex=False))

    # Convert to numeric
    for column in ["quantity", "unit_price", "discount"]:
        df[column] = pd.to_numeric(df[column],errors="coerce")

    # --------------------------------------------------
    # 5. Convert Order Date
    # --------------------------------------------------
    df["order_date"] = pd.to_datetime(df["order_date"],errors="coerce")

    # --------------------------------------------------
    # 6. Remove exact duplicates
    # --------------------------------------------------
    df = df.drop_duplicates()

    # --------------------------------------------------
    # 7. Impute missing Unit Price values
    # --------------------------------------------------
    price_mapping = (df.groupby("product")["unit_price"].first())

    df["unit_price"] = df["unit_price"].fillna(df["product"].map(price_mapping))

    # --------------------------------------------------
    # 8. Handle missing Discount values
    # --------------------------------------------------
    # Assumption: missing Discount means no discount
    df["discount"] = df["discount"].fillna(0)

    # --------------------------------------------------
    # 9. Reset index and return
    # --------------------------------------------------
    df = df.reset_index(drop=True)

    return df


def save_data(df: pd.DataFrame, file_name: str) -> None:
    """
        Saves dataframe to file.
        Returns csv file.
    """
    df.to_csv(file_name, index=False)


def main(file: str) -> None:
    """
        Main function for orchestration.
    """
    df = load_data(file)

    clean_df = clean_data(df)

    df_revenue = add_virtual_column(clean_df, "quantity * unit_price - discount","revenue")

    revenue_by_region = (df_revenue.groupby("region", as_index=False)["revenue"].sum())

    save_data(revenue_by_region, "revenue_by_region.csv")

    return None


if __name__ == "__main__":
    main(file="sales.csv")