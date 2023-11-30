from data_source import DataSource

import pandas as pd

class Wallet():
    def __init__(self):
        super().__init__()
        self.assets = []
        self.weights = []

    def add_asset(self, ds: DataSource, weight: float = 1.) -> None:
        self.assets.append(ds)
        self.weights.append(weight)

    @staticmethod
    def _add_period(series: pd.Series, period: pd.DateOffset):
        series.index = series.index.to_timestamp() - period
        series = series.groupby(series.index.to_period("M")).first()
        return series

    @staticmethod
    def _calc_gains(asset: DataSource, period: pd.DateOffset) -> pd.Series:
        price = asset.get_monthly_results()
        price_after_period = Wallet._add_period(price.copy(), period)

        diffs = price_after_period - price
        diffs = diffs[diffs.notnull()]

        return diffs

    def calc_gains(self, period: pd.DateOffset) -> pd.Series:
        if len(self.assets) == 0:
            raise RuntimeError("No assets defined for this wallet")
        
        # TODO: Implement
        if len(self.assets) > 1:
            raise RuntimeError("Calculation of gains for more than one asset not implemented")
        
        return Wallet._calc_gains(self.assets[0], period)
    

def wallet_statistics(wallet: Wallet):
    # TODO: Calculate gain/loss statistics:
    # - For different periods (1m/6m/1y/5y/10y/20y)
    # - Best/worst/median gain
    # - % of loss, % of gains
    pass


    
if __name__ == "__main__":
    from data_source import Wig20
    wallet = Wallet()
    wallet.add_asset(Wig20())

    gains = wallet.calc_gains(pd.DateOffset(months=60))
    print(f'gains: {gains}')