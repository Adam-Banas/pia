from abc import ABC

import pandas as pd

class DataSource(ABC):
    # TODO: Make this method abstract, the following decorator doesn't work
    # @abstractmethod
    def get_monthly_results(self) -> pd.Series:
        """Needs override."""
        raise RuntimeError("get_monthly_results not implemented in derived class")

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

if __name__ == "__main__":
    wig20 = Wig20()
    price = wig20.get_monthly_results()

    breakpoint()
    print(f"price: {price}")