from src.base.alphaprototype import AlphaPrototype
from src.run_order_history import run_order_history

from finta import TA
import numpy as np


class RSI_ADX(AlphaPrototype):
    """An rsi and adx model.

    Buy signal:
        - RSI is less than the lower threshold.
        - ADX is higher than the ADX threshold.

    Sell signal:
        - RSI is higher than the upper threshold."""

    def print_full_results(self):
        run_order_history(self.orders, self.all_ticks, self.symbol_data, "rsi_adx", chunks=20)

    def print_results(self, symbol):
        print ("processed", symbol)

    def pre_backtest_calculations(self, value):
        self.ema = TA.EMA(value)
        self.adx = TA.ADX(value)
        self.rsi = TA.RSI(value)

        self.rsi_low = 20
        self.rsi_high = 70
        self.adx_threshold = 25

    def step(self, symbol, data, i):
        if self.rsi[i] < self.rsi_low and self.adx[i] > self.adx_threshold:
            self.buy(symbol, data["close"][i], data["time"][i])
        elif self.rsi[i] > self.rsi_high:
            self.sell(symbol, data["close"][i], data["time"][i])


strat = RSI_ADX("Test", 100, data_root="../../Data/")
strat.run_backtest()
