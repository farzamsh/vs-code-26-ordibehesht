# idea tedad counterkamtar az adad 20  
"""default haku fast mode with two diffrent tp & sl"""

# Requires
import time
import pandas as pd
import pandas_ta as ta
from functions.pandas_ta_supplementary_libraries import *


# Set parameters
def set_parameters(strategy, df):
    return {}

# Indicators
def farzam_indicators(open, high, low, close, parameters_input):
    """Setting farzam's indicator's parameters"""
    global lenght
    global count
    global in_position
    global long_top
    global long_bot
    global long_diff
    global short_top
    global short_bot
    global short_diff
    global long_trade
    global short_trade
    
    count = 0
    in_position = False
    long_top = 0
    long_bot = 0
    long_diff = 0
    short_top = 0
    short_bot = 0
    short_diff = 0
    long_trade = False
    short_trade = False
    
    stdev20 = ta.stdev(close, 20)*10000/ta.sma(close, 9)
    sma100  = ta.sma(close,100)
    sma500  = ta.sma(close,500)
    lenght = parameters_input['length']
    sma_cond_long= (1000*(sma500 - sma100)/sma500)<parameters_input["long_ma_max"]
    sma_cond_short= (1000*(sma500 - sma100)/sma500)>parameters_input["short_ma_min"]

    def calculate_top(row, high):
        """Calculate top"""
        return highest(high, lenght-row.counter, row.name)
    
    def calculate_bot(row, low):
        """Calculate bot"""
        return lowest(low, lenght-row.counter, row.name)

    
    def calculate_counter(stdev20, reset_stdev, reset_counter_to):
        """Calculate counter"""
        global count
        global lenght
        if stdev20>=reset_stdev:
            count = length - reset_counter_to
        elif count>0:
            count -= 1
        return count
    counter = stdev20.apply(calculate_counter, args=(parameters_input["reset_stdev"],parameters_input["reset_counter_to"],)).rename("counter").reset_index()
    top = counter.apply(calculate_top, args=(high,), axis=1).rename("top")
    bot = counter.apply(calculate_bot, args=(low,), axis=1).rename("bot")
    diff = (top - bot).rename("diffrent_top_bot")

    same_highest_cond = top <= top.shift(4)
    same_lowest_cond = bot >= bot.shift(4)

    entry_long = parameters_input["entry_long"]
    entry_short = parameters_input["entry_short"]
    entry_condition = stdev20 <= parameters_input["entry_stdev"]
    long_entry_cond = (close <= bot + entry_long/10 * diff) & same_lowest_cond & entry_condition & sma_cond_long
    short_entry_cond = (close >= bot + entry_short/10 * diff) & same_highest_cond & entry_condition & sma_cond_short
    conditions = pd.concat([long_entry_cond, short_entry_cond, top, bot, diff, close], axis=1).rename(columns={0: "long_entry_cond", 1: "short_entry_cond", 2: "top", 3: "bot", "close_price": "close"})
    
    def condition_trade(row, take_profit_long,take_profit_short,stop_loss_long,stop_loss_short):
        """Set open trade and close trade"""
        global in_position
        global long_top
        global long_bot
        global long_diff
        global short_top
        global short_bot
        global short_diff
        global long_trade
        global short_trade
        
        

        if row.close >= long_bot+take_profit_long*long_diff and long_trade and in_position:
            strategy.exit(row.name, "exit long", "long")
            in_position = False
            long_top = 0
            long_bot = 0
            long_diff = 0
            long_trade = False
            short_trade = False

        if row.close <= long_bot-stop_loss_long*long_diff and long_trade and in_position:
            strategy.exit(row.name, "exit long", "long")
            in_position = False
            long_top = 0
            long_bot = 0
            long_diff = 0
            long_trade = False
            short_trade = False

        if row.close <= short_top-take_profit_short*short_diff and short_trade and in_position:
            strategy.exit(row.name, "exit short", "short")
            in_position = False
            short_top = 0
            short_bot = 0
            short_diff = 0
            long_trade = False
            short_trade = False

        if row.close >= short_top+stop_loss_short*short_diff and short_trade and in_position:
            strategy.exit(row.name, "exit short", "short")
            in_position = False
            short_top = 0
            short_bot = 0
            short_diff = 0
            long_trade = False
            short_trade = False
        
        if row.long_entry_cond and not in_position:
            strategy.entry(row.name, "long", "long")
            in_position = True
            long_top = row.top
            long_bot = row.bot
            long_diff = row.diffrent_top_bot
            long_trade = True
            short_trade = False
        
        if row.short_entry_cond and not in_position:
            strategy.entry(row.name, "short", "short")
            in_position = True
            short_top = row.top
            short_bot = row.bot
            short_diff = row.diffrent_top_bot
            long_trade = False
            short_trade = True

    trades = conditions.apply(condition_trade, args=(parameters_input["take_profit_long"],parameters_input["stop_loss_long"],parameters_input["take_profit_short"],parameters_input["stop_loss_short"] ), axis=1).rename("trade").reset_index()


    
farzam_indicators(open, high, low, close, parameters_input)



# best parameters
entry_long = [2.36]
entry_short = [7.5]
reset_stdev = [65]
length = [300]
reset_counter_to = [5]
take_profit_long = [1.1]
stop_loss_long  =  [0.9]
take_profit_short = [1.1]
stop_loss_short  =  [1.1] 
entry_stdev = [95]  
long_ma_max  = [1000]
short_ma_min = [-20]

