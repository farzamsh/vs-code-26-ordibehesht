import pandas as pd
import numpy as np


def save_final_df_to_excel(df: pd.DataFrame, excel_file_name):
    def excel_columns(col):
        """ Convert given row and column number to an Excel-style col name. """
        LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        result = []
        while col:
            col, rem = divmod(col - 1, 26)
            result[:0] = LETTERS[rem]
        return ''.join(result)

    def get_df_col_widths(df: pd.DataFrame):
        """ Return Excel-style column widths for a given dataframe. """
        idx_max = max([len(str(s)) for s in df.index.values] + [len(str(df.index.name))])
        return [idx_max] + [max([len(str(s)) for s in df[col].values] + [len(col)]) for col in df.columns]

    with pd.ExcelWriter(excel_file_name, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="noa")
        worksheet = writer.sheets['noa']
        y, x = df.shape
        y += 1  # 1 for the header row
        x += 1  # 1 for the index and column
        # worksheet.conditional_format(f'C2:C{y}', {'type': 'data_bar', 'bar_solid': True})  # count column
        for i in range(1, x + 1):
            worksheet.conditional_format(f'{excel_columns(i)}2:{excel_columns(i)}{y}', {'type': '3_color_scale',
                                                                                        'mid_color': '#00000000'})  # other every column
        # for i, width in enumerate(get_df_col_widths(df)):  # set columns auto fit
        #     worksheet.set_column(i, i, width)
        worksheet.freeze_panes(3, 0)  # Freeze first 2 row
        print(f"{excel_file_name} created")


# long_ent_type = ["1", "2", "3", "12", "23", "123"]  # 0
# long_close_type = ["3", "4", "5", "34", "45", "345"]  # 1
# short_ent_type = ["3", "4", "5", "34", "45", "345"]  # 2
# short_close_type = ["1", "2", "3", "12", "23", "123"]  # 3
# hl_len = [250, 504, 1008]  # 4
# hi_ma_len = [1, 9, 25]  # 5
# sl_input = [0, 500, 1000]  # 6
# hma_len = [288, 576]  # 7
# hma2_len = [21, 70]  # 8
# hma_change_long = [0, 1]  # 9
# hma_change_short = [0, -1]  # 10

import pickle
import pandas as pd

# file_name = 'result_Z5_2021_01'
# file_name = 'result_Zfm_v32_2021_01'
# file_name = 'result_Zfm_v32_full_2021_01'
# file_name = 'result_z4_2021_01_new'
# file_name = 'result_z4_2021-01-01_all'
file_name = 'result_z4_2022-04_test'

df = pd.DataFrame()
with open(f"{file_name}.pkl", "rb") as f:
    a = pickle.load(f)  # objs.append((i, z.backtest(), result, pd.DataFrame(z.list_of_trades())))
    for i in a:
        dic = i[1]
        dic["long_ent_type"] = i[0][0]
        dic["long_close_type"] = i[0][1]
        dic["short_ent_type"] = i[0][2]
        dic["short_close_type"] = i[0][3]
        dic["hl_len"] = i[0][4]
        dic["hi_ma_len"] = i[0][5]
        dic["sl_input"] = i[0][6]
        dic["hma_len"] = i[0][7]
        dic["hma2_len"] = i[0][8]
        dic["min_profit"] = i[0][9]
        dic["constant_stop_loss"] = i[0][10]
        dic["src_hma_len"] = i[0][11]
        dic['hl_lookback_len'] = i[0][12]
        dic['hmac_len'] = i[0][13]
        trades_list_df = i[3]
        trades_list_df["runup_score"] = trades_list_df['profit_percent'] - trades_list_df['run_up']
        trades_list_df['drawdw_score'] = trades_list_df['profit_percent'] - trades_list_df['draw_down']
        trades_list_df['trade_score'] = trades_list_df["runup_score"] + trades_list_df["drawdw_score"]
        trades_list_df['drawup'] = trades_list_df['run_up'] - trades_list_df['draw_down']
        dic["runup_score"] = trades_list_df['runup_score'].sum()
        dic["runup_score_mean"] = trades_list_df['runup_score'].mean()
        dic["drawdw_score"] = trades_list_df['drawdw_score'].sum()
        dic["drawdw_score_mean"] = trades_list_df['drawdw_score'].mean()
        dic['trade_score'] = trades_list_df['trade_score'].sum()
        dic['trade_score_mean'] = trades_list_df['trade_score'].mean()
        dic['runup_sum'] = trades_list_df['run_up'].sum()
        dic['drawup_sum'] = trades_list_df['drawup'].sum()
        # dic["hma_change_long"] = i[0][9]
        # dic["hma_change_short"] = i[0][10]
        for k in i[2]:
            dic[k] = i[2][k]['net_profit_percent']
            # dic['buy_and_hold_return_percent'] = i[2][k]['buy_and_hold_return_percent']
        # df = df.append(pd.DataFrame([dic]), ignore_index=True)
        df = pd.concat([df, pd.DataFrame([dic])])

    for c in df.columns:
        if np.issubdtype(df[c].dtype, np.number):
            df.at['avg', c] = df[c].mean()

    mtrades = a[0][2]  #
    for m in mtrades:
        df.at['return', m] = mtrades[m]['buy_and_hold_return_percent']

df = df.loc[::-1]
print(df)
save_final_df_to_excel(df, f'{file_name}.xlsx')
