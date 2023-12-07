import pandas as pd

from data_source import DataSource

# Replacement for data source,
# To simplify calculation, it just adds yearly / monthly grow with respect to the starting value
class FakeDataSource(DataSource):
    def __init__(self, yearly_grow=0.1, monthly_grow=0., start = '1900', end = '2000'):
        super().__init__()
        self.yearly_grow=yearly_grow
        self.monthly_grow=monthly_grow
        self.start = start
        self.end = end

    def get_monthly_results(self) -> pd.Series:
        initial_value = 1
        idx = pd.period_range(start=self.start, end=self.end, freq='M', name='Date')
        data = [initial_value + i * self.monthly_grow + int(i/12) * self.yearly_grow for i in range(len(idx))]
        return pd.Series(data, index=idx)