from zogomo import Zogomo


def backtest():
    import itertools
    import time
    long_ent_type = ["1", "2", "3", "12", "23", "123"]
    long_close_type = ["3", "4", "5", "34", "45", "345"]
    short_ent_type = ["3", "4", "5", "34", "45", "345"]
    short_close_type = ["1", "2", "3", "12", "23", "123"]

    permutations = itertools.chain(itertools.product(long_ent_type, long_close_type, short_ent_type, short_close_type))
    objs = []
    # count = 0
    import pickle

    for i in permutations:
        # count += 1
        start_time = time.time()
        z = Zogomo(data, i[0], i[1], i[2], i[3])
        result = z.periodic_calc(30)
        # z.add_to_sheet(sheet)
        end_time = time.time()
        print(f"Time: {end_time - start_time}")
        objs.append((i, z.backtest(), result))
        pickle.dump(objs, open("result.pkl", "wb"))


def final_backtest():
    import pandas as pd
    import time
    from zogomo import Zogomo
    data = pd.read_json("data.json")
    data = data[data.date >= "2021-01-01"]
    # from sheet import Sheet

    # sheet = Sheet(strategy_name="zfm1", service_account="service_account.json",
    #               email="emadd.baaa@gmail.com")

    import itertools

    long_ent_type = ["1", "2", "3", "12", "23", "123"]
    long_close_type = ["3", "4", "5", "34", "45", "345"]
    short_ent_type = ["3", "4", "5", "34", "45", "345"]
    short_close_type = ["1", "2", "3", "12", "23", "123"]

    permutations = itertools.chain(itertools.product(long_ent_type, long_close_type, short_ent_type, short_close_type))
    objs = []
    # count = 0
    import pickle

    for i in permutations:
        # count += 1
        start_time = time.time()
        z = Zogomo(data, i[0], i[1], i[2], i[3])
        result = z.periodic_calc(30)
        # z.add_to_sheet(sheet)
        end_time = time.time()
        print(f"Time: {end_time - start_time}")
        objs.append((i, z.backtest(), result))
        pickle.dump(objs, open("result.pkl", "wb"))


def backtest_Z2():
    import pandas as pd
    import time
    import itertools
    import pickle
    from zogomo2 import Zogomo2

    data = pd.read_json("data.json")
    data = data[data.date >= "2022-03-01"]

    long_ent_type = ["1", "2", "3", "12", "23", "123"]  # 0
    long_close_type = ["3", "4", "5", "34", "45", "345"]  # 1
    short_ent_type = ["3", "4", "5", "34", "45", "345"]  # 2
    short_close_type = ["1", "2", "3", "12", "23", "123"]  # 3
    hl_len = [250, 504, 1008]  # 4
    hi_ma_len = [1, 9, 25]  # 5
    sl_input = [0, 500, 1000]  # 6
    hma_len = [288, 576]  # 7
    hma2_len = [21, 70]  # 8
    hma_change_long = [0, 1]  # 9
    hma_change_short = [0, -1]  # 10
    permutations = itertools.chain(
        itertools.product(long_ent_type, long_close_type, short_ent_type, short_close_type, hl_len, hi_ma_len, sl_input,
                          hma_len, hma2_len, hma_change_long, hma_change_short))
    objs = []
    for i in permutations:
        start_time = time.time()
        if i[1] == i[0] or i[3] == i[2]:
            continue
        z = Zogomo2(data, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10])
        result = z.periodic_calc(30)
        end_time = time.time()
        print(f"Time: {end_time - start_time}")
        objs.append((i, z.backtest(), result))
        pickle.dump(objs, open("result_Z2_2021_03.pkl", "wb"))


def backtest_Z3():
    import pandas as pd
    import time
    import itertools
    import pickle
    from zogomo2 import Zogomo2

    data = pd.read_json("data.json")
    data = data[data.date >= "2022-01-01"]

    long_ent_type = ["12"]  # 0
    long_close_type = ["345"]  # 1
    short_ent_type = ["45"]  # 2
    short_close_type = ["123"]  # 3
    hl_len = [250, 1008]  # 4
    hi_ma_len = [1]  # 5
    sl_input = [0, 1000]  # 6
    hma_len = [288, 576]  # 7
    hma2_len = [21, 70]  # 8
    hma_change_long = [0]  # 9
    hma_change_short = [0]  # 10
    long_bool = [True, False]  # 11
    short_bool = [True, False]  # 12
    permutations = itertools.chain(
        itertools.product(long_ent_type, long_close_type, short_ent_type, short_close_type, hl_len, hi_ma_len, sl_input,
                          hma_len, hma2_len, hma_change_long, hma_change_short, long_bool, short_bool))
    objs = []
    list_of_permutaions = list(permutations)
    l = len(list_of_permutaions)
    for i in list_of_permutaions:
        print('remaining: ', l)
        start_time = time.time()
        if i[1] == i[0] or i[3] == i[2]:
            continue
        z = Zogomo2(data, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10], i[11], i[12])
        result = z.periodic_calc(7)
        duration = time.time() - start_time
        print(f"Time: {duration}", 'estimated remaining: ', l * duration)
        l -= 1
        objs.append((i, z.backtest(), result))
        pickle.dump(objs, open("result_Z5_2021_01.pkl", "wb"))


def backtest_Zfm32():
    import pandas as pd
    import time
    import itertools
    import pickle
    from zogomo3 import Zogomo3

    # data = pd.read_json("data.json")
    data = pd.read_json("data_tmp.json")
    data = data[data.date >= "2022-01-01"]

    long_ent_type = ["1", "2", "12"]  # 0
    long_close_type = ["3", "4", "5", "34", "45"]  # 1
    short_ent_type = ["3", "4", "5", "34", "45"]  # 2
    short_close_type = ["1", "2", "12"]  # 3
    hl_len = [250, 1008]  # 4
    hi_ma_len = [9]  # 5
    sl_input = [0, 1000]  # 6
    hma_len = [288, 576]  # 7
    hma2_len = [70]  # 8
    long_bool = [True]  # 11
    short_bool = [True]  # 12
    permutations = itertools.chain(
        itertools.product(long_ent_type, long_close_type, short_ent_type, short_close_type, hl_len, hi_ma_len, sl_input,
                          hma_len, hma2_len, long_bool, short_bool))
    objs = []
    list_of_permutaions = list(permutations)
    l = len(list_of_permutaions)
    for i in list_of_permutaions:
        print('remaining: ', l)
        start_time = time.time()
        if i[1] == i[0] or i[3] == i[2]:
            continue
        z = Zogomo3(data, i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9], i[10])
        result = z.periodic_calc(29)
        duration = time.time() - start_time
        print(f"Time: {duration}", 'estimated remaining minutes: ', (l * duration) / 60)
        l -= 1
        objs.append((i, z.backtest(), result, pd.DataFrame(z.list_of_trades())))
        pickle.dump(objs, open("result_Zfm_v32_full_2021_01.pkl", "wb"))


def backtest_Z4():
    import pandas as pd
    import time
    import itertools
    import pickle
    from zogomo4 import Zogomo4

    # data = pd.read_json("data.json")
    data = pd.read_json("data.json")
    data = data[data.date >= "2022-01-01"]

    long_ent_type = ["12", "123"]  # 0
    long_close_type = ["45", "345"]  # 1
    short_ent_type = ["45", "345"]  # 2
    short_close_type = ["12", "123"]  # 3
    hl_len = [252, 504, 1008]  # 4
    hi_ma_len = [9]  # 5
    sl_input = [0, 500, 1000]  # 6
    hma_len = [288, 576]  # 7
    hma2_len = [35, 70]  # 8
    min_profit = [0.5, 1]  # 9
    constant_stop_loss = [1, 3, 5]  # 10
    src_hma_len = [11, 21]  # 11
    permutations = itertools.chain(
        itertools.product(long_ent_type, long_close_type, short_ent_type, short_close_type, hl_len, hi_ma_len, sl_input,
                          hma_len, hma2_len, min_profit, constant_stop_loss, src_hma_len))
    objs = []
    list_of_permutaions = list(permutations)
    l = len(list_of_permutaions)
    for i in list_of_permutaions:
        print('remaining: ', l)
        start_time = time.time()
        if i[1] == i[0] or i[3] == i[2]:
            continue
        z = Zogomo4(data=data, long_ent_type=i[0], long_close_type=i[1], short_ent_type=i[2], short_close_type=i[3],
                    hl_len=i[4], hi_ma_len=i[5], sl_input=i[6], hma_len=i[7], hma2_len=i[8], min_profit=i[9],
                    constant_stop_loss=i[10], src_hma_len=i[11])
        result = z.periodic_calc(29)
        duration = time.time() - start_time
        print(f"took {duration} seconds! estimated remaining minutes: {(l * duration) / 60}")
        l -= 1
        objs.append((i, z.backtest(), result, pd.DataFrame(z.list_of_trades())))
        pickle.dump(objs, open("result_z4_2021_01.pkl", "wb"))


def backtest_z4_new():
    import pandas as pd
    import time
    import itertools
    import pickle
    from zogomo4 import Zogomo4

    data = pd.read_json("data.json")
    data = data[data.date >= "2022-01-01"]

    long_ent_type = ["12"]  # 0
    long_close_type = ["45"]  # 1
    short_ent_type = ["45"]  # 2
    short_close_type = ["12"]  # 3
    hl_len = [1008]  # 4
    hi_ma_len = [9]  # 5
    sl_input = [1000]  # 6
    hma_len = [576]  # 7
    hma2_len = [70]  # 8
    min_profit = [1]  # 9
    constant_stop_loss = [5]  # 10
    src_hma_len = [21]  # 11
    hl_lookback_len = [500]  # 12
    hmac_len = [75] #13

    permutations = itertools.chain(
        itertools.product(long_ent_type, long_close_type, short_ent_type, short_close_type, hl_len, hi_ma_len, sl_input,
                          hma_len, hma2_len, min_profit, constant_stop_loss, src_hma_len, hl_lookback_len))
    objs = []
    list_of_permutaions = list(permutations)
    l = len(list_of_permutaions)
    for i in list_of_permutaions:
        print('remaining: ', l)
        start_time = time.time()
        if i[1] == i[0] or i[3] == i[2] or i[4] < i[7]:
            continue
        z = Zogomo4(data=data, long_ent_type=i[0], long_close_type=i[1], short_ent_type=i[2], short_close_type=i[3],
                    hl_len=i[4], hi_ma_len=i[5], sl_input=i[6], hma_len=i[7], hma2_len=i[8], min_profit=i[9],
                    constant_stop_loss=i[10], src_hma_len=i[11], hl_lookback_len=i[12])
        result = z.periodic_calc(29)
        duration = time.time() - start_time
        print(f"took {duration} seconds! estimated remaining minutes: {(l * duration) / 60}")
        l -= 1
        objs.append((i, z.backtest(), result, pd.DataFrame(z.list_of_trades())))
        pickle.dump(objs, open("result_z4_2021_01_new.pkl", "wb"))
