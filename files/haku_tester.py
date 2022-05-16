from strategy_tester.strategy import Strategy
from strategy_tester.indicator import Indicator
from strategy_tester.pandas_ta_supplementary_libraries import *
import pandas_ta as ta


# noinspection PyAttributeOutsideInit
class Haku(Strategy):
    def __init__(strategy, data):
        strategy.setdata(data)
        strategy.candles_data = strategy.data
        strategy.run()

    def indicators(strategy) -> None:
        strategy.std_len = 20
        strategy.std_src = strategy.close
        strategy.topPer = 250
        strategy.botPer = 250
        strategy.topSrc = strategy.high
        strategy.botSrc = strategy.low
        strategy.stdev_max_reset = 65
        strategy.stdev_max_entry = 95
        strategy.reset_counter_to = 5
        strategy.long_top = 0.0
        strategy.long_bot = 0.0
        strategy.long_diff = 0.0
        strategy.short_top = 0.0
        strategy.short_bot = 0.0
        strategy.short_diff = 0.0
        strategy.long_entry = 2.36
        strategy.short_entry = 7.86
        strategy.take_profit_long = 10.7  # 11
        strategy.take_profit_short = 10.7  # 9
        strategy.stop_loss_long = 10.9  # 11
        strategy.stop_loss_short = 10.9  # 11
        strategy.h_lookback_cond = 4
        strategy.l_lookback_cond = 4
        strategy.counter = 0
        strategy.cond_test_bool = True
        strategy.long_bool_farzam = True
        strategy.short_bool_farzam = True
        strategy.long_id_farzam = "long farzam"
        strategy.short_id_farzam = "short farzam"
        strategy.stdev20 = Indicator("stdev", ta.stdev, args=(strategy.close, 20), wait=False)
        strategy.sma20 = Indicator("sma", ta.sma, args=(strategy.close, 20), wait=False)

    def condition(strategy):
        if strategy.counter > 0:
            strategy.counter -= 1
        if strategy.stdev2 * 10000 / strategy.sma20 >= strategy.stdev_max_reset:
            strategy.counter = strategy.topPer - strategy.reset_counter_to

        top = highest(strategy.topSrc, strategy.topPer - strategy.counter)
        bot = lowest(strategy.botSrc, strategy.botPer - strategy.counter)
        diff = top - bot
        same_lowest_cond = bot >= bot[4]
        same_top = top <= top[4]
        long_entry = strategy.close <= bot + strategy.long_entry / 10 * diff and strategy.position_size == 0 and same_lowest_cond and strategy.long_bool_farzam
        short_entry = strategy.close >= bot + strategy.short_entry / 10 * diff and same_top and strategy.short_bool_farzam and strategy.position_size == 0
        long_close = strategy.close >= strategy.long_bot + strategy.take_profit_long * strategy.long_diff / 10 and strategy.position_size > 0
        short_close = strategy.close <= strategy.long_bot - strategy.stop_loss_long * strategy.long_diff / 10 and strategy.position_size > 0
        strategy.conditions = long_entry.rename("long_entry"), short_entry.rename("short_entry"), long_close.rename(
            "long_close"), short_close.rename("short_close")

    def trade_calc(strategy, row):
        close = row.close

        if strategy.stdev20 * 10000 / strategy.sma20 <= strategy.stdev_max_entry:
            if row.long_entry:
                strategy.entry(strategy.long_id_farzam, strategy.long)
                strategy.long_top = strategy.top
                strategy.long_bot = strategy.bot
                strategy.long_diff = strategy.diff

            if row.short_entry:
                strategy.entry(strategy.short_id_farzam, strategy.short)
                strategy.short_top = strategy.top
                strategy.short_bot = strategy.bot
                strategy.short_diff = strategy.diff

        if row.long_close:
            strategy.exit(strategy.long_id_farzam, comment="tp")
            strategy.long_top = 0.0
            strategy.long_bot = 0.0
            strategy.long_diff = 0.0

        if row.short_close:
            strategy.exit(strategy.long_id_farzam, comment="sl")
            strategy.long_top = 0.0
            strategy.long_bot = 0.0
            strategy.long_diff = 0.0

        if row.close <= strategy.short_top - strategy.take_profit_short * strategy.short_diff / 10 and strategy.position_size < 0:
            strategy.exit(strategy.short_id_farzam, comment="tp")
            strategy.short_top = 0.0
            strategy.short_bot = 0.0
            strategy.short_diff = 0.0

        if row.close >= strategy.short_top + strategy.stop_loss_short * strategy.short_diff / 10 and strategy.position_size < 0:
            strategy.exit(strategy.short_id_farzam, comment="sl")
            strategy.short_top = 0.0
            strategy.short_bot = 0.0
            strategy.short_diff = 0.0
