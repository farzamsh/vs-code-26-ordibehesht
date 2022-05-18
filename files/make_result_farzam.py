# make result farzam 
import pandas as pd
import numpy as np
import pandas_ta as ta
from farzam_backtest import *


data = pd.read_json("data.json")
data = data[data.date >= "2022-01-01"]

f = Haku(data)
print(f.backtest())
