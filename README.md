# Sales Data Analysis Pipeline

## Project Overview

This project implements a simple ETL pipeline for processing sales data from `sales.csv`.

The pipeline:
1. Loads raw sales data.
2. Cleans and normalizes the dataset.
3. Calculates revenue for each sales record.
4. Aggregates revenue by region.
5. Exports the results to `revenue_by_region.csv`.

## Project Structure

```text
cloudfide_task/
├── pipeline.py
├── solution.py
├── sales.csv
├── revenue_by_region.csv
├── test_virtual_column.py
├── README.md
└── tests/
    ├── __init__.py
    ├── test_solution.py
    └── test_pipeline.py
```

## Requirements

- Python 3.10+
- pandas
- pytest

## Setup

Clone or download the project.

Create and activate a virtual environment:

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install pandas pytest
```

## Running the Pipeline

Make sure `sales.csv` is located in the project root directory.

Run:

```bash
python pipeline.py
```

The pipeline generates:

```text
revenue_by_region.csv
```

The output contains the total revenue for each region.

Revenue is calculated using:

```text
Revenue = Quantity * Unit Price - Discount
```

## Running Tests

All tests can be executed with one command:

```bash
python -m pytest -v
```

The test suite covers:

- Arithmetic operations in `add_virtual_column()`.
- Multiple operations in a single expression.
- Parentheses and calculation precedence.
- Input DataFrame preservation.
- Invalid column references.
- Data cleaning and normalization.
- Revenue calculation and regional aggregation.
- CSV output generation.

## Data Quality Issues and Cleaning Decisions

The following issues were identified during the exploration of `sales.csv`.

| Issue                                                   |         Number of affected rows | Cleaning decision                                  |
|---------------------------------------------------------|--------------------------------:|----------------------------------------------------|
| Repeated header row                                     |                               1 | Removed                                            |
| Summary/footer row (`TOTAL`)                            |                               1 | Removed                                            |
| Exact duplicate records                                 |                    5 extra rows | Removed using `drop_duplicates()`                  |
| Quantity values with spaces as thousands separators     |                               4 | Spaces removed before numeric conversion           |
| Missing Unit Price values                               | 5 initially; 4 transaction rows | Imputed using the product's unit price             |
| Missing Region values                                   |                               1 | Associated with the `TOTAL` row; removed with it   |
| Missing Product values                                  |                               1 | Associated with the `TOTAL` row; removed with it   |
| Missing Order Date values                               |                               1 | Associated with the `TOTAL` row; removed with it   |
| Missing Discount values                                 |                             963 | Replaced with 0                                    |
| Inconsistent Region capitalization                      |                              10 | Normalized using title case                        |
| Negative Quantity values                                |                               6 | Retained as potential returns or sales corrections |
| Space in the beginning or at the end of the region name |                               5 | Removed using `str.strip()`                        |
| Decimal comma in 'Unit Price'                           |                               7 | Replaced with dot before numerical conversion      |

### Additional Observations

- The `Quantity ` column header contained trailing whitespace. Column names are normalized to lowercase `snake_case`.
- The repeated header row also caused non-numeric values such as `Quantity`, `Unit Price` and `Discount` to appear in data columns. The row is removed before numeric conversion.
- Four valid Quantity values used spaces as thousands separators, for example `1 762`.
- Every product was found to have exactly one unique non-null Unit Price during the initial data exploration.
- Four genuine transaction records had missing Unit Price values. Their prices were imputed using the corresponding product's known price.

## Assumptions

The following assumptions were made where the source data or task requirements were unclear:

1. **Missing Discount values:** A missing Discount is interpreted as no discount and replaced with 0.

2. **Missing Unit Price values:** Each product has a fixed unit price. Missing prices are imputed using the known price for the corresponding product.

3. **Negative quantities:** Negative Quantity values represent potential product returns or sales corrections. They are retained and contribute negatively to revenue.

4. **Exact duplicates:** Exact duplicate records are assumed to be accidental duplicates introduced during data export or collection. Since no unique line-item identifier is available, exact duplicates are removed.

5. **Summary row:** The `TOTAL` row is a summary/footer record and is not treated as an individual transaction.

6. **Revenue calculation:** Discount is treated as a monetary amount applied to the entire transaction line, rather than a percentage or per-unit discount.

7. **Region names:** Differences in capitalization are treated as formatting inconsistencies rather than separate regions.

## Output

The resulting `revenue_by_region.csv` contains:

- `region` – normalized sales region.
- `revenue` – total revenue for that region.

The output is generated by grouping sales records by region and summing their calculated revenue.
