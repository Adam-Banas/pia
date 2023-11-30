from .wallet import Wallet
from data_source import Wig20

import pandas as pd

class Stats:
    def __init__(self, wallet: Wallet, period: pd.DateOffset):
        self._returns = wallet.calc_returns(period)
    
    def max_return(self) -> float:
        return self._returns.max()
    
    def min_return(self) -> float:
        return self._returns.min()
    
    def median_return(self) -> float:
        return self._returns.median()
    
    def percent_gains(self) -> float:
        return (self._returns > 0).sum() / len(self._returns)


def wallet_statistics(wallet: Wallet) -> dict:
    # TODO: Calculate gain/loss statistics:
    # - For different periods (1m/6m/1y/5y/10y/20y)
    wallet = Wallet()
    wallet.add_asset(Wig20())

    return {'5y': Stats(wallet, pd.DateOffset(years=5))}

    
if __name__ == "__main__":
    from data_source import Wig20
    wallet = Wallet()
    wallet.add_asset(Wig20())

    gains = wallet.calc_gains(pd.DateOffset(months=60))
    print(f'gains: {gains}')

    stats = wallet_statistics(wallet)
    stats['5y'].max_gain()