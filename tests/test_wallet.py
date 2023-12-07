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
    pytest.skip("Multi-asset wallets are not supported yet")
    fake_ds_10percent = FakeDataSource(yearly_grow=0.1)
    wallet.add_asset(fake_ds_10percent)
    fake_ds_5percent = FakeDataSource(yearly_grow=0.05)
    wallet.add_asset(fake_ds_5percent)
    wallet.calc_returns(pd.DateOffset(years=5))

def test_multi_asset_wallet_return_value():
    wallet = Wallet()
    pytest.skip("Multi-asset wallets are not supported yet")
    fake_ds_10percent = FakeDataSource(yearly_grow=0.1)
    wallet.add_asset(fake_ds_10percent)
    fake_ds_5percent = FakeDataSource(yearly_grow=0.05)
    wallet.add_asset(fake_ds_5percent)
    
    result_5y = wallet.calc_returns(pd.DateOffset(years=5))
    assert result_5y.iloc[0] == 0.375
    assert result_5y.iloc[-1] < result_5y.iloc[0]

    result_10y = wallet.calc_returns(pd.DateOffset(years=10))
    assert result_10y.iloc[0] == 0.75