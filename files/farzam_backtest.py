from itertools import count
import pandas
from strategy_tester.strategy import Strategy
from strategy_tester.indicator import Indicator
from strategy_tester.pandas_ta_supplementary_libraries import *
import pandas_ta as ta
import pandas as pd
import numpy as np




class Haku(Strategy):
    def __init__(strategy, data):
        strategy.setdata(data)
        strategy.candles_data = strategy.data
        strategy.long_ma_max = 1000
        strategy.short_ma_min = -20
        strategy.std_len = 20
        strategy.std_src = strategy.close
        strategy.topPer = 300
        strategy.botPer = 300
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
        strategy._counter = 0
        strategy._top = 0
        strategy._bot = 0
        strategy.cond_test_bool = True
        strategy.long_bool_farzam = True
        strategy.short_bool_farzam = True
        strategy.in_position = 0
        strategy.long_id_farzam = "long farzam"
        strategy.short_id_farzam = "short farzam"
        strategy.run()


    def calculate_counter(strategy, stdev20_sma9_cond):
        if stdev20_sma9_cond:
            strategy._counter = strategy.topPer - strategy.reset_counter_to
        elif strategy._counter > 0:
            strategy._counter -= 1
        return strategy._counter

    def calculate_top(strategy, row):
        if strategy.topPer-row.counter > int(row.idx):
            return 0
        return highest(strategy.topSrc.iloc[:int(row.idx)+1], strategy.topPer-row.counter).iat[-1]

    def calculate_bot(strategy, row):
        if strategy.botPer-row.counter > int(row.idx):
            return 0
        return lowest(strategy.botSrc.iloc[:int(row.idx)+1], strategy.botPer-row.counter).iat[-1]

    def indicators(strategy) -> None:
        stdev20 = Indicator("stdev20", ta.stdev, args=(strategy.close, 20), wait=False)
        sma9 = Indicator("sma9", ta.sma, args=(strategy.close, 9), wait=False)
        # strategy.stdev20_ = strategy.stdev20 / strategy.sma9
        sma100 = Indicator("sma100", ta.sma, args=(strategy.close, 100), wait=False)
        sma500 = Indicator("sma500", ta.sma, args=(strategy.close, 500), wait=False)
        strategy.add(stdev20, sma9, sma100, sma500)


    def condition(strategy):
        stdev20_sma9 = strategy.stdev20 * 10000 / strategy.sma9
        strategy.stdev20_sma9_conds = stdev20_sma9.apply(lambda x: x>=strategy.stdev_max_reset)
        strategy.counter = strategy.stdev20_sma9_conds.apply(strategy.calculate_counter)
        strategy.counter = strategy.counter.rename("counter")
        sma_cond_long = (
                1000*(strategy.sma500 - strategy.sma100)/strategy.sma500).apply(lambda x: x < strategy.long_ma_max)
        sma_cond_short = (
                1000*(strategy.sma500 - strategy.sma100)/strategy.sma500).apply(lambda x: x > strategy.short_ma_min)

        strategy.topSrc_botSrc_counter = pd.concat([strategy.topSrc, strategy.botSrc, strategy.counter], axis=1)
        strategy.topSrc_botSrc_counter['idx'] = np.arange(len(strategy.topSrc_botSrc_counter))
        strategy.top = strategy.topSrc_botSrc_counter.apply(strategy.calculate_top, axis=1)
        strategy.bot = strategy.topSrc_botSrc_counter.apply(strategy.calculate_bot, axis=1)
        strategy.diff = strategy.top - strategy.bot
        strategy.top_5 = strategy.top.shift(5)
        strategy.bot_5 = strategy.bot.shift(5)
        same_highest_cond = strategy.top <= strategy.top_5
        same_lowest_cond = strategy.bot >= strategy.bot_5

        
        entry_condition = (strategy.stdev20 * 10000 / strategy.sma9).apply(lambda x: x >= strategy.stdev_max_entry)


        long_entry_cond = (strategy.close <= strategy.bot + strategy.long_entry * strategy.diff
                        ) & same_lowest_cond & entry_condition & sma_cond_long
        short_entry_cond = (strategy.close >= strategy.bot + strategy.short_entry * strategy.diff
                            ) & same_highest_cond & entry_condition & sma_cond_short

        long_exit_tp_cond = (strategy.close >= strategy.long_bot+strategy.take_profit_long*strategy.long_diff)
        long_exit_sl_cond = (strategy.close <= strategy.long_bot-strategy.stop_loss_long*strategy.long_diff)
        short_exit_tp_cond = (strategy.close <= strategy.short_top-strategy.take_profit_short*strategy.short_diff)
        short_exit_sl_cond = (strategy.close >= strategy.short_top+strategy.stop_loss_short*strategy.short_diff)

        strategy.conditions = (long_entry_cond.rename("long_entry"), short_entry_cond.rename("short_entry"),
                                long_exit_tp_cond.rename("long_exit_tp"), long_exit_sl_cond.rename("long_exit_sl"),
                                short_exit_tp_cond.rename("short_exit_tp"), short_exit_sl_cond.rename("short_exit_sl"),
                                strategy.top.rename("top"), strategy.bot.rename("bot"), strategy.diff.rename("diff"))


    def trade_calc(strategy, row):

        if strategy.in_position == 1:
            # close long tp
            if row.long_exit_tp:
                strategy.exit(strategy.long_id_farzam, signal="tp")
                strategy.in_position = 0
                strategy.long_top = 0.0
                strategy.long_bot = 0.0
                strategy.long_diff = 0.0
            # close long sl
            elif row.long_exit_sl:
                strategy.exit(strategy.long_id_farzam, signal="sl")
                strategy.in_position = 0
                strategy.long_top = 0.0
                strategy.long_bot = 0.0
                strategy.long_diff = 0.0

        if strategy.in_position == -1:
            # close short tp
            if row.short_exit_tp:
                strategy.exit(strategy.short_id_farzam, signal="tp")
                strategy.in_position = 0
                strategy.long_top = 0.0
                strategy.long_bot = 0.0
                strategy.long_diff = 0.0
            # close short sl
            if row.short_exit_sl:
                strategy.exit(strategy.short_id_farzam, signal="sl")
                strategy.in_position = 0
                strategy.long_top = 0.0
                strategy.long_bot = 0.0
                strategy.long_diff = 0.0

        if strategy.in_position == 0:
            if row.long_entry:
                strategy.entry(strategy.long_id_farzam, signal="long")
                strategy.in_position = 1
                strategy.long_top = row.top
                strategy.long_bot = row.bot
                strategy.long_diff = row.diff

            elif row.short_entry:
                strategy.entry(strategy.short_id_farzam, signal="short")
                strategy.in_position = -1
                strategy.short_top = row.top
                strategy.short_bot = row.bot
                strategy.short_diff = row.diff



# data = pd.read_json('data.json')
