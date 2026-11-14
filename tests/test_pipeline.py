
import pandas as pd

from pipeline import clean_data, main


def create_raw_data():
    return pd.DataFrame([
        ["SO-001", "east", "Keyboard", "2", "89.00", "10.00", "2026-01-01"],
        ["SO-001", "EAST", "Keyboard", "2", "89.00", "10.00", "2026-01-01"],
        ["SO-002", "North", "Mouse", "1 762", "2.00", None, "2026-01-02"],
        ["SO-003", "East", "Keyboard", "1", None, None, "2026-01-03"],
        ["Order ID", "Region", "Product", "Quantity", "Unit Price", "Discount", "Order Date"],
        ["TOTAL", None, None, "1765", None, None, None]
    ], columns=[
        "Order ID",
        "Region",
        "Product",
        "Quantity ",
        "Unit Price",
        "Discount",
        "Order Date"
    ])


def test_clean_data():
    raw_df = create_raw_data()

    result = clean_data(raw_df)

    # Technical rows and duplicate records removed
    assert len(result) == 3

    # Column names normalized
    assert "quantity" in result.columns
    assert "unit_price" in result.columns

    # Region capitalization normalized
    assert set(result["region"]) == {"East", "North"}

    # Quantity converted to integer
    assert pd.api.types.is_integer_dtype(result["quantity"])

    # Thousands separator removed
    assert 1762 in result["quantity"].values

    # Missing discount replaced with zero
    assert result["discount"].isna().sum() == 0

    # Missing price imputed from product mapping
    keyboard_prices = result.loc[
        result["product"] == "Keyboard",
        "unit_price"
    ]

    assert keyboard_prices.isna().sum() == 0
    assert keyboard_prices.nunique() == 1


def test_main_creates_revenue_file(tmp_path, monkeypatch):
    raw_df = create_raw_data()

    input_file = tmp_path / "sales.csv"
    output_file = tmp_path / "revenue_by_region.csv"

    raw_df.to_csv(input_file, index=False)

    monkeypatch.chdir(tmp_path)

    main(str(input_file))

    assert output_file.exists()

    result = pd.read_csv(output_file)

    assert list(result.columns) == ["region", "revenue"]

    expected = {
        "East": 257.0,
        "North": 3524.0
    }

    actual = dict(zip(result["region"], result["revenue"]))

    assert actual == expected