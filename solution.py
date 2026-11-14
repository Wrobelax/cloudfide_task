import re
import operator

import pandas as pd


def is_valid_column_name(name: str) -> bool:
    """
        Check if name is a valid column name.
        :param name: str
        :return: bool
    """
    return bool(re.fullmatch(r"[A-Za-z_]+\Z", name))


def add_virtual_column(df: pd.DataFrame, role: str, new_column: str) -> pd.DataFrame:
    """
        Add virtual column to dataframe.
        Return empty dataframe if column is not valid.
        :param df: pd.DataFrame
        :param role: str
        :param new_column: str
        :return: pd.DataFrame
    """

    # Validate new column name
    if not is_valid_column_name(new_column):
        return pd.DataFrame()

    # Validate column names in dataframe
    if not all(isinstance(column, str) and is_valid_column_name(column) for column in df.columns):
        return pd.DataFrame()

    # Validate expression format
    if not isinstance(role, str) or not role.strip():
        return pd.DataFrame()

    # Allow only column names, arithmetic operators and parentheses
    pattern = r"[a-zA-Z_]+|[+\-*/()]"

    tokens = re.findall(pattern, role)

    # Remove whitespace and check whether the entire expression
    # consists only of allowed tokens
    if "".join(tokens) != re.sub(r"\s+", "", role):
        return pd.DataFrame()

    # Validate referenced columns
    referenced_columns = {
        token for token in tokens
        if re.fullmatch(r"[A-Za-z_]+\Z", token)
    }

    missing_columns = referenced_columns - set(df.columns)

    if missing_columns:
        return pd.DataFrame()

    # Evaluate expression
    result = df.copy()
    try:
        result[new_column] = result.eval(role, engine="python")
    except SyntaxError:
        return pd.DataFrame()

    return result
