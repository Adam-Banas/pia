import pytest

from model import Wallet
import pandas as pd

from test_utils import FakeDataSource

def test_will_throw_on_empty_wallet():
    empty_wallet = Wallet()
    with pytest.raises(Exception):
        empty_wallet.calc_returns(pd.DateOffset(years=5))

def test_single_asset_wallet_will_not_throw():
    wallet = Wallet()
    fake_ds = FakeDataSource()
    wallet.add_asset(fake_ds)
    wallet.calc_returns(pd.DateOffset(years=5))

def test_single_asset_wallet_return_value():
    wallet = Wallet()
    fake_ds = FakeDataSource(yearly_grow=0.1)
    wallet.add_asset(fake_ds)
    
    result_5y = wallet.calc_returns(pd.DateOffset(years=5))
    assert result_5y.iloc[0] == 0.5
    assert result_5y.iloc[-1] < result_5y.iloc[0]

    result_10y = wallet.calc_returns(pd.DateOffset(years=10))
    assert result_10y.iloc[0] == 1.


def test_multi_asset_wallet_will_not_throw():
    wallet = Wallet()
    fake_ds_10percent = FakeDataSource(yearly_grow=0.1)
    wallet.add_asset(fake_ds_10percent)
    fake_ds_5percent = FakeDataSource(yearly_grow=0.05)
    wallet.add_asset(fake_ds_5percent)
    wallet.calc_returns(pd.DateOffset(years=5))

@pytest.mark.parametrize("weights", ((1., 1.), (1., 3.)), ids=['equal_weights', 'weighted'])
def test_multi_asset_wallet_same_periods(weights):
    yearly_grows=(.1, .05)

    wallet = Wallet()
    fake_ds_10percent = FakeDataSource(yearly_grow=yearly_grows[0])
    wallet.add_asset(fake_ds_10percent, weight=weights[0])
    fake_ds_5percent = FakeDataSource(yearly_grow=yearly_grows[1])
    wallet.add_asset(fake_ds_5percent, weight=weights[1])

    def _verify(years):
        result = wallet.calc_returns(pd.DateOffset(years=years))
        assert result.iloc[0] == ( \
            yearly_grows[0] * years * weights[0] + \
            yearly_grows[1] * years * weights[1]) / \
            sum(weights)
        assert result.iloc[-1] < result.iloc[0]

    _verify(5)
    _verify(10)
    _verify(20)

@pytest.mark.parametrize("weights", ((1., 1.), (1., 3.)), ids=['equal_weights', 'weighted'])
def test_multi_asset_wallet_overlapping_periods(weights):
    yearly_grows=(.1, .05)

    late_start_years = 10
    start_year_0 = 1900
    start_year_1 = start_year_0+late_start_years

    wallet = Wallet()
    fake_ds_10percent = FakeDataSource(yearly_grow=yearly_grows[0], start = str(start_year_0))
    wallet.add_asset(fake_ds_10percent, weight=weights[0])
    fake_ds_5percent = FakeDataSource(yearly_grow=yearly_grows[1], start = str(start_year_1))
    wallet.add_asset(fake_ds_5percent, weight=weights[1])

    def _verify(years):
        result = wallet.calc_returns(pd.DateOffset(years=years))
        assert result.iloc[0] == ( \
            ((yearly_grows[0] * years) / (1+yearly_grows[0]*late_start_years)) * weights[0] + \
            yearly_grows[1] * years * weights[1]) / \
            sum(weights)
        assert result.iloc[-1] < result.iloc[0]

    _verify(5)
    _verify(10)
    _verify(20)