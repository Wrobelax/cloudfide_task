import pandas as pd
import pytest

from solution import add_virtual_column


@pytest.fixture
def sample_df():
    return pd.DataFrame({
        "quantity": [2, 3, 4],
        "unit_price": [10.0, 20.0, 15.0],
        "discount": [1.0, 5.0, 0.0]
    })


def test_addition(sample_df):
    result = add_virtual_column(
        sample_df,
        "quantity + discount",
        "total"
    )

    assert result["total"].tolist() == [3.0, 8.0, 4.0]


def test_subtraction(sample_df):
    result = add_virtual_column(
        sample_df,
        "unit_price - discount",
        "result"
    )

    assert result["result"].tolist() == [9.0, 15.0, 15.0]


def test_multiplication(sample_df):
    result = add_virtual_column(
        sample_df,
        "quantity * unit_price",
        "subtotal"
    )

    assert result["subtotal"].tolist() == [20.0, 60.0, 60.0]


def test_multiple_operations(sample_df):
    result = add_virtual_column(
        sample_df,
        "quantity * unit_price - discount",
        "revenue"
    )

    assert result["revenue"].tolist() == [19.0, 55.0, 60.0]


def test_parentheses(sample_df):
    result = add_virtual_column(
        sample_df,
        "(quantity * unit_price) - discount",
        "revenue"
    )

    assert result["revenue"].tolist() == [19.0, 55.0, 60.0]


def test_original_dataframe_is_not_modified(sample_df):
    original = sample_df.copy()

    add_virtual_column(
        sample_df,
        "quantity * unit_price",
        "subtotal"
    )

    pd.testing.assert_frame_equal(sample_df, original)


def test_missing_column_returns_empty_dataframe(sample_df):
    result = add_virtual_column(
        sample_df,
        "quantity * unknown_column",
        "result"
    )

    assert result.empty


def test_invalid_new_column_name(sample_df):
    result = add_virtual_column(
        sample_df,
        "quantity * unit_price",
        "new column"
    )

    assert result.empty


def test_invalid_role_returns_empty_dataframe(sample_df):
    result = add_virtual_column(
        sample_df,
        "quantity +",
        "result"
    )

    assert result.empty