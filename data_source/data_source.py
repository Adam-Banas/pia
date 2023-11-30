from abc import ABC

import pandas as pd

class DataSource(ABC):
    # TODO: Make this method abstract, the following decorator doesn't work
    # @abstractmethod
    def get_monthly_results(self) -> pd.Series:
        """Needs override."""

    @staticmethod
    def _get_data_dir() -> str:
        import os
        return os.path.dirname(__file__)


class Wig20(DataSource):
    def __init__(self, price_column='Kurs otwarcia'):
        super().__init__()
        self.price_column = price_column

    def get_monthly_results(self) -> pd.Series:
        # TODO: Ensure that no months are missing
        data = pd.read_excel(Wig20._get_data_file(), index_col="Data")
        price = data[self.price_column]
        price.index.name = 'Date'
        price.name = 'Price'
        price.index = pd.to_datetime(price.index)
        result = price.groupby(price.index.to_period("M")).first()

        return result
    
    @staticmethod
    def _get_data_file() -> str:
        return Wig20._get_data_dir() + "/wig20_to_2023-11-06_indeksy.xls"


class SnP500(DataSource):
    def get_monthly_results(self) -> pd.Series:
        # TODO: Implement this. Should return series similar to Wig20:
        # - index name = 'Date', type: pandas.core.indexes.period.PeriodIndex
        # - series name = 'Price'
        # - index values: 'yyyy-mm', price: any price from that month (e.g. the first one)
        # - index values are unique, no months are missing
        # - sorted by index values, ascending order
        raise RuntimeError("Not implemented")



# TODO: Move these UTs to separate file
def _verify(ds):
    # TODO: Test actual data, not only types and names. Ideas:
    # - unique index values
    # - is sorted
    # - no months missing
    price = ds.get_monthly_results()
    assert price.index.name == 'Date'
    assert isinstance(price.index, pd.core.indexes.period.PeriodIndex)
    assert price.name == 'Price'

def test_wig20():
    wig20 = Wig20()
    _verify(wig20)

def test_snp500():
    snp500 = SnP500()
    _verify(snp500)