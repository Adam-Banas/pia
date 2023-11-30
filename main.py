import matplotlib.pyplot as plt
import pandas as pd

from data_source import Wig20
from model import Wallet, wallet_statistics

# config:
years = 5

# code:
wallet = Wallet()
wallet.add_asset(Wig20())

stats_5y = wallet_statistics(wallet)['5y']

def as_percent(val):
    return f"{round(val, 3) * 100}%"

# breakpoint()
# TODO: When was the max / min / median return?
print(f"min return: {as_percent(stats_5y.min_return())}")
print(f"max return: {as_percent(stats_5y.max_return())}")
print(f"median return: {as_percent(stats_5y.median_return())}")
print(f"percent of gains: {as_percent(stats_5y.percent_gains())}")