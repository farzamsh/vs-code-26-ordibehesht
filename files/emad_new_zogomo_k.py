

short_id = "short"
long_id = "long"

long_bool = True
short_bool = True
close_cond_bool = True
use_stop_loss = True

src_hma_len = 21


long_entry_src = ta.hma(low,src_hma_len)
short_entry_src = ta.hma(high,src_hma_len)

shortEntryPrice = -1.0
shortBarCounter = 0
if shortEntryPrice != -1.0:
    shortBarCounter = shortBarCounter + 1
longEntryPrice = -1.0
longBarCounter = 0
if longEntryPrice != -1.0:
    longBarCounter = longBarCounter + 1
line_y = 500

# calculations ----------------------------------------
hl_len = 1008
h_src = high
l_src = low
h = ta.highest(h_src,hl_len)
l = ta.lowest(l_src,hl_len)
hi_ma_len = 9
highest_ma = ta.sma(h,hi_ma_len)
lowest_ma = ta.sma(l,hi_ma_len)
h_color = color.silver
l_color = color.silver
sl_input = 236
longSL = 0.0
shortSL = 100000.0
hl_diff = highest_ma - lowest_ma
level1 = lowest_ma + hl_diff * 236/ 1000
level2 = lowest_ma + hl_diff * 382/ 1000
level0_5 = (level1 + lowest_ma) / 2
level1_5 = (level1 + level2) / 2
level3 = lowest_ma + hl_diff * 500/ 1000
level4 = lowest_ma + hl_diff * 618/ 1000
level5 = lowest_ma + hl_diff * 786/ 1000
level5_5 = (highest_ma + level5) / 2
level4_5 = (level4 + level5) / 2


long_ent_type = "12"


if long_ent_type == "1":
    long_ent = ta.crossover(long_entry_src,level1)
elif long_ent_type == "2":
    long_ent = ta.crossover(long_entry_src,level2)
elif long_ent_type == "3":
    long_ent = ta.crossover(long_entry_src,level3)
elif long_ent_type == "12":
    long_ent = ta.crossover(long_entry_src,level2) or ta.crossover(long_entry_src,level1) or ta.crossover(long_entry_src,level0_5)
elif long_ent_type == "23":
    long_ent = ta.crossover(long_entry_src,level2) or ta.crossover(long_entry_src,level3)
elif long_ent_type == "123":
    long_ent = ta.crossover(long_entry_src,level2) or ta.crossover(long_entry_src,level1) or ta.crossover(long_entry_src,level3)



long_close_type = "45"
if long_close_type == "3":
    long_close = ta.crossunder(short_entry_src,level3)
elif long_close_type == "4":
    long_close = ta.crossunder(short_entry_src,level4)
elif long_close_type == "5":
    long_close = ta.crossunder(short_entry_src,level5)
elif long_close_type == "34":
    long_close = ta.crossunder(short_entry_src,level3) or ta.crossunder(short_entry_src,level4)
elif long_close_type == "45":
    long_close = ta.crossunder(short_entry_src,level4) or ta.crossunder(short_entry_src,level5)
elif long_close_type == "345":
    long_close = ta.crossunder(short_entry_src,level4) or ta.crossunder(short_entry_src,level5) or ta.crossunder(short_entry_src,level3)


short_ent_type = "45"

if short_ent_type == "3":
    short_ent = ta.crossover(short_entry_src,level3)
elif short_ent_type == "4":
    short_ent = ta.crossover(short_entry_src,level4)
elif short_ent_type == "5":
    short_ent = ta.crossover(short_entry_src,level5)
elif short_ent_type == "34":
    short_ent = ta.crossover(short_entry_src,level3) or ta.crossover(short_entry_src,level4)
elif short_ent_type == "45":
    short_ent = ta.crossover(short_entry_src,level4) or ta.crossover(short_entry_src,level5) or ta.crossover(short_entry_src,level5_5) #or ta.crossover(short_entry_src,level4_5)
elif short_ent_type == "345":
    short_ent = ta.crossover(short_entry_src,level4) or ta.crossover(short_entry_src,level5) or ta.crossover(short_entry_src,level3)


short_close_type = "12"

if short_close_type == "1":
    short_close = ta.crossover(short_entry_src,level1)
elif short_close_type == "2":
    short_close = ta.crossover(short_entry_src,level2)
elif short_close_type == "3":
    short_close = ta.crossover(short_entry_src,level3)
elif short_close_type == "12":
    short_close = ta.crossover(short_entry_src,level2) or ta.crossover(short_entry_src,level1) #or ta.crossover(short_entry_src,level0_5)
elif short_close_type == "23":
    short_close = ta.crossover(short_entry_src,level2) or ta.crossover(short_entry_src,level3)
elif short_close_type == "123":
    short_close = ta.crossover(short_entry_src,level2) or ta.crossover(short_entry_src,level1) or ta.crossover(short_entry_src,level3)





hma_len = 576
hma500 = ta.hma(hlcc4,hma_len)
change_hma_long = hma500 > hma500[1]
change_hma_short = hma500 < hma500[1]

hma2_len = 70
hma2 = ta.hma(hlcc4,hma2_len)
change_hma2_long = hma2 > hma2[1]
change_hma2_short =  hma2 < hma2[1]

hmac_len = input.int(75)
hmac1 = ta.hma(hlcc4,hmac_len)
hmac2 = ta.hma(hlcc4,hmac_len*2)
hmac3 = ta.hma(hlcc4,hmac_len*4)

hmac_long_entry_cond = hmac1 > hmac1[1] and hmac2 > hmac2[1] and hmac3 > hmac3[1]
hmac_short_entry_cond = hmac1 < hmac1[1] and hmac2 < hmac2[1] and hmac3 < hmac3[1]

hl_lookback_len = 500

long_hl_cond = (highest_ma - highest_ma[hl_lookback_len])*100/highest_ma[hl_lookback_len] <= 1 and (lowest_ma - lowest_ma[hl_lookback_len])*100/lowest_ma[hl_lookback_len] <= 1
short_hl_cond = (highest_ma[hl_lookback_len] - highest_ma)*100/highest_ma <= 1 and (lowest_ma[hl_lookback_len] - lowest_ma)*100/lowest_ma <= 1
long_profit = (close - longEntryPrice) * 100 / longEntryPrice
long_run_away = long_profit < 2  and change_hma_short and long_profit > 0
long_greedy = long_profit >= 1 and long_profit <= 5 and (change_hma2_short or (ta.crossunder(long_entry_src,hma2) and long_entry_src<long_entry_src[1])) # to get closer profits to runup 
longStopLossCondition = ta.crossunder(close,longSL) and use_stop_loss
long_swap_from_short = shortEntryPrice != -1.0 and (ta.crossover(long_entry_src,shortEntryPrice))
long_sl_slope = long_profit < 0 and change_hma_short
longEntryCondition = (long_ent or long_swap_from_short) and change_hma_long and change_hma2_long and hmac_long_entry_cond and long_hl_cond
longCloseCondition = long_close or longStopLossCondition or long_run_away or long_greedy

short_profit = (shortEntryPrice - close) * 100 / shortEntryPrice
short_run_away = short_profit > 0 and short_profit < 2 and (change_hma_long)
short_greedy = short_profit >= 1 and short_profit <= 5 and (change_hma2_long or  (ta.crossover(short_entry_src,hma2) and short_entry_src>short_entry_src[1])) #to get closer profits to runup || 1 must be replaced with avg trade %
shortStopLossCondition = ta.crossover(close,shortSL) and use_stop_loss
short_swap_from_long = longEntryPrice != -1.0 and (ta.crossover(short_entry_src,longEntryPrice))
shortEntryCondition = (short_ent or short_swap_from_long) and change_hma_short and change_hma2_short and hmac_short_entry_cond and short_hl_cond
shortCloseCondition = short_close or shortStopLossCondition or short_run_away or short_greedy



