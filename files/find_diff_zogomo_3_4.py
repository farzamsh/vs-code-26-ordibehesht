import os

import mplfinance as mpf
import pandas as pd
import pandas_ta as ta
from strategy_tester.indicator import Indicator
from strategy_tester.pandas_ta_supplementary_libraries import *
from strategy_tester.strategy import Strategy


class Zogomo4(Strategy):
    """
    StrategyTester is a class that tests a strategy.
    StrategyTester can be used to test a strategy in financial markets.
    """
 
    def __init__(strategy, data, long_ent_type, long_close_type, short_ent_type, short_close_type, hl_len, hi_ma_len,
                 sl_input, hma_len, hma2_len, min_profit, constant_stop_loss, src_hma_len, hl_lookback_len,
                 hmac_len) -> None:
        super().__init__()
        strategy.setdata(data)
        strategy.candles_data = strategy.data
        strategy.set_parameters(long_ent_type=long_ent_type, long_close_type=long_close_type,
                                short_ent_type=short_ent_type, short_close_type=short_close_type, hl_len=hl_len,
                                hi_ma_len=hi_ma_len, sl_input=sl_input, hma_len=hma_len, hma2_len=hma2_len,
                                min_profit=min_profit, constant_stop_loss=constant_stop_loss, src_hma_len=src_hma_len,
                                hl_lookback_len=hl_lookback_len, hmac_len=hmac_len)
        strategy.run()

    def indicators(strategy) -> None:
        """ StrategyTester constructor.

        Description:
            If you want to test a strategy, you need to create a StrategyTester object.
            Then you can set the strategy and the data.
            All variables that need to be set are set in the constructor.
        """

        # inputs --------------------------------
        # strategy.long_bool = True
        # strategy.short_bool = True

        hlcc4 = (strategy.high + strategy.low + strategy.close + strategy.close) / 4
        # src_hma = ta.hma(hlcc4, 21)  # check with AA
        # src_hma = Indicator("src_hma", ta.hma, args=(hlcc4, 21))
        src_hma = Indicator("src_hma", ta.hma, args=(hlcc4, strategy.src_hma_len))
        strategy.add(src_hma)
        # src_hma = strategy.low
        # src_hma = strategy.high

        # src_hma = src_hma
        # src_hma = src_hma

        # line drawing --------------------------------
        strategy.shortEntryPrice = -1.0
        strategy.longEntryPrice = -1.0

        # calculation --------------------------------
        # strategy.hl_len = 1008  # variable
        strategy.h_src = strategy.high
        strategy.l_src = strategy.low
        h = highest(strategy.h_src, strategy.hl_len)
        l = lowest(strategy.l_src, strategy.hl_len)
        # strategy.hi_ma_len = 9 # variable
        strategy.highest_ma = ta.sma(h, strategy.hi_ma_len)
        strategy.lowest_ma = ta.sma(l, strategy.hi_ma_len)
        # strategy.sl_input = 500  # variable
        strategy.longSL = 0.0
        strategy.shortSL = 1000000.0

        strategy.hl_diff = strategy.highest_ma - strategy.lowest_ma
        level1 = strategy.lowest_ma + strategy.hl_diff * 236 / 1000
        level2 = strategy.lowest_ma + strategy.hl_diff * 382 / 1000
        level3 = strategy.lowest_ma + strategy.hl_diff * 500 / 1000
        level4 = strategy.lowest_ma + strategy.hl_diff * 618 / 1000
        level5 = strategy.lowest_ma + strategy.hl_diff * 786 / 1000

        # hma_len = 576  # variable
        hma_len = strategy.hma_len
        hma1 = Indicator("hma1", ta.hma, args=(hlcc4, hma_len))

        # hma2_len = 70
        hma2_len = strategy.hma2_len
        hma2 = Indicator("hma2", ta.hma, args=(hlcc4, hma2_len))
        strategy.add(hma1, hma2)

        hmac1 = Indicator("hmac1", ta.hma, args=(hlcc4, strategy.hmac_len))
        hmac2 = Indicator("hmac2", ta.hma, args=(hlcc4, strategy.hmac_len * 2))
        hmac3 = Indicator("hmac3", ta.hma, args=(hlcc4, strategy.hmac_len * 4))
        strategy.add(hmac1, hmac2, hmac3)

        long_ent1 = Indicator("long_ent1", crossover, args=(src_hma, level1), wait=False)
        long_ent2 = Indicator("long_ent2", crossover, args=(src_hma, level2), wait=False)
        long_ent3 = Indicator("long_ent3", crossover, args=(src_hma, level3), wait=False)
        strategy.add(long_ent1, long_ent2, long_ent3)

        long_close1 = Indicator("long_close3", crossunder, args=(src_hma, level3), wait=False)
        long_close2 = Indicator("long_close4", crossunder, args=(src_hma, level4), wait=False)
        long_close3 = Indicator("long_close5", crossunder, args=(src_hma, level5), wait=False)
        strategy.add(long_close1, long_close2, long_close3)

        short_ent1 = Indicator("short_ent3", crossunder, args=(src_hma, level3), wait=False)
        short_ent2 = Indicator("short_ent4", crossunder, args=(src_hma, level4), wait=False)
        short_ent3 = Indicator("short_ent5", crossunder, args=(src_hma, level5), wait=False)
        strategy.add(short_ent1, short_ent2, short_ent3)

        short_close1 = Indicator("short_close1", crossover, args=(src_hma, level1), wait=False)
        short_close2 = Indicator("short_close2", crossover, args=(src_hma, level2), wait=False)
        short_close3 = Indicator("short_close3", crossover, args=(src_hma, level3), wait=False)
        strategy.add(short_close1, short_close2, short_close3)

    def condition(strategy):
        long_ent_types = strategy.long_ent_type
        short_ent_types = strategy.short_ent_type
        long_close_types = strategy.long_close_type
        short_close_types = strategy.short_close_type

        long_ent = False
        long_close = False
        short_ent = False
        short_close = False

        for long_c in long_ent_types:
            if long_c != long_ent_types[0]:
                long_ent = long_ent | strategy.__dict__[f"long_ent{long_c}"]
            else:
                long_ent = strategy.__dict__[f"long_ent{long_c}"]

        for short_c in short_ent_types:
            if short_c != short_ent_types[0]:
                short_ent = short_ent | strategy.__dict__[f"short_ent{short_c}"]
            else:
                short_ent = strategy.__dict__[f"short_ent{short_c}"]
        for long_c in long_close_types:
            if long_c != long_close_types[0]:
                long_close = long_close | strategy.__dict__[f"long_close{long_c}"]
            else:
                long_close = strategy.__dict__[f"long_close{long_c}"]
        for short_c in short_close_types:
            if short_c != short_close_types[0]:
                short_close = short_close | strategy.__dict__[f"short_close{short_c}"]
            else:
                short_close = strategy.__dict__[f"short_close{short_c}"]

        strategy.hma1 = strategy.hma1.round(decimals=2)
        strategy.hma2 = strategy.hma2.round(decimals=2)
        hma2_change_long = strategy.hma2 > strategy.hma2.shift()
        hma2_change_short = strategy.hma2 < strategy.hma2.shift()

        hma_change_long = strategy.hma1 > strategy.hma1.shift()
        hma_change_short = strategy.hma1 < strategy.hma1.shift()

        long_hl_cond = (strategy.highest_ma >= strategy.highest_ma.shift(
            strategy.hl_lookback_len)) & (strategy.lowest_ma >= strategy.lowest_ma.shift(strategy.hl_lookback_len))
        short_hl_cond = (strategy.highest_ma <= strategy.highest_ma.shift(
            strategy.hl_lookback_len)) & (strategy.lowest_ma <= strategy.lowest_ma.shift(strategy.hl_lookback_len))

        hmac_long_entry_cond = (strategy.hmac1 > strategy.hmac1.shift()) & (strategy.hmac2 > strategy.hmac2.shift()) & (
                strategy.hmac3 > strategy.hmac3.shift())
        hmac_short_entry_cond = (strategy.hmac1 < strategy.hmac1.shift()) & (
                strategy.hmac2 < strategy.hmac2.shift()) & (
                                        strategy.hmac3 < strategy.hmac3.shift())

        strategy.pervious_low = 0
        strategy.pervious_high = 0
        longEntryCondition = (
                    long_ent & hma_change_long & hma2_change_long & long_hl_cond & hmac_long_entry_cond).rename(
            "long_ent")
        longCloseCondition = long_close.rename("long_close")
        shortEntryCondition = (
                    short_ent & hma2_change_short & hma_change_short & short_hl_cond & hmac_short_entry_cond).rename(
            "short_ent")
        shortCloseCondition = short_close.rename("short_close")

        strategy.conditions = longEntryCondition, longCloseCondition, shortEntryCondition, shortCloseCondition, strategy.highest_ma.rename(
            "highest_ma"), strategy.lowest_ma.rename("lowest_ma"), strategy.hl_diff.rename(
            "hl_diff"), hma2_change_long.rename("hma2_change_long"), hma2_change_short.rename(
            "hma2_change_short"), hma_change_long.rename("hma_change_long"), hma_change_short.rename("hma_change_short")


    @staticmethod
    def mpf_plot(data, title, date):
        if os.path.exists(f"conditions_chart/{title}_{date}.png"):
            pass
        else:
            mpf.plot(data,
                     type='candle',
                     style='binance',
                     savefig=f"conditions_chart/{title}_{date}.png",
                     title=f"{title}_{date}",
                     figratio=(30, 10))


    def trade_calc(strategy, row):
        # current_candle = strategy.data
        if row.low > strategy.longSL > strategy.pervious_low != 0:
            long_sl = True
        else:
            long_sl = False

        if row.high > strategy.shortSL > strategy.pervious_high != 0:
            short_sl = True
        else:
            short_sl = False
        long_profit = (row.close - strategy.longEntryPrice) * 100 / strategy.longEntryPrice
        long_greedy = (strategy.min_profit <= long_profit <= 5) and row.hma2_change_short
        long_run_away = strategy.longEntryPrice != -1.0 and (0 < long_profit <= 2) and row.hma_change_short
        long_constant_sl = long_profit < strategy.constant_stop_loss * -1

        short_profit = (strategy.shortEntryPrice - row.close) * 100 / strategy.shortEntryPrice
        short_greedy = (strategy.min_profit <= short_profit <= 5) and row.hma2_change_long
        short_constant_sl = short_profit < strategy.constant_stop_loss * -1  # to get closer profits to run-up || 1 must be replaced with avg trade % and 3 with WHAT?!
        short_run_away = strategy.shortEntryPrice != -1.0 and (0 < short_profit <= 2) and row.hma_change_long

        if row.short_close or short_sl or short_run_away or short_greedy or short_constant_sl:
            if strategy.shortEntryPrice != -1.0:
                strategy.exit("short",
                              signal=f'{row.short_close=} {short_sl=} {short_run_away=} {short_greedy=} {short_constant_sl=}')
                strategy.shortEntryPrice = -1.0
                strategy.shortSL = 1000000.0

        if row.short_ent:
            if strategy.shortEntryPrice == -1.0:
                if strategy.longEntryPrice != -1.0:
                    strategy.exit("long")
                    strategy.longEntryPrice = -1.0
                    strategy.longSL = 0

                strategy.entry("short", "short")
                strategy.shortEntryPrice = row.close
                strategy.shortSL = row.highest_ma + row.hl_diff * strategy.sl_input / 1000

        if row.long_close or long_sl or long_run_away or long_greedy or long_constant_sl:
            if strategy.longEntryPrice != -1.0:
                strategy.exit("long",
                              signal=f'{row.long_close=} {long_sl=} {long_run_away=} {long_greedy=} {long_constant_sl=}')
                strategy.longEntryPrice = -1.0
                strategy.longSL = 0

        if row.long_ent:
            if strategy.longEntryPrice == -1.0:
                if strategy.shortEntryPrice != -1.0:
                    strategy.exit("short")
                    strategy.shortEntryPrice = -1.0
                    strategy.shortSL = 1000000.0

                strategy.entry("long", "long")
                strategy.longEntryPrice = row.close
                strategy.longSL = row.lowest_ma - row.hl_diff * strategy.sl_input / 1000

        strategy.pervious_low = row.low
        strategy.pervious_high = row.high
