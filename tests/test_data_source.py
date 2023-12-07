from data_source import SnP500, Wig20

import pandas as pd
import pytest

DATA_SOURCE_NAMES = [
    "wig20",
    "snp500",
]

def _create_data_source(name):
    if name == "wig20":
        return Wig20()
    if name == "snp500":
        pytest.skip(reason="Data source not implemented")
        return SnP500()


@pytest.mark.parametrize("ds_name", DATA_SOURCE_NAMES)
def test_names(ds_name):
    # if ds_name == "snp500":
    #     pytest.skip(reason="Not implemented")
    ds = _create_data_source(ds_name)
    price = ds.get_monthly_results()

    assert price.index.name == 'Date'
    assert price.name == 'Price'


@pytest.mark.parametrize("ds_name", DATA_SOURCE_NAMES)
def test_index_type(ds_name):
    ds = _create_data_source(ds_name)
    price = ds.get_monthly_results()

    assert isinstance(price.index, pd.core.indexes.period.PeriodIndex)

# TODO: Test actual data, not only types and names. Ideas:
# - unique index values
# - is sorted
# - no months missing
# - data from file (e.g. min / max value)