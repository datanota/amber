
import os
import openpyxl
import pandas as pd


class DataAccess:
    def __init__(self):
        self.stocks_file = 'amber.xlsx'
        prj_dir = 'amber'
        prj_path = (os.getcwd()).split(prj_dir)[0] + prj_dir
        print(prj_path)
        self.file_path = prj_path + '/data/'

    def get_df_available_stocks_data(self):
        df = self.get_df_stocks_data()
        df = df[df['sold'] == 0]
        df.insert(6, 'pq', df['unit_price'] * df['quantity'])  # unit_price times quantity
        return df

    def get_df_stocks_data(self):
        stocks_df = pd.read_excel(self.file_path + self.stocks_file, sheet_name=0, index_col=None)
        for str_col in ['transaction_id', 'stock_id', 'date', 'ticker']:
            stocks_df[str_col] = stocks_df[str_col].astype('string')
        for float_col in ['unit_price', 'quantity']:
            stocks_df[float_col] = stocks_df[float_col].astype('float')
        updates_df = pd.read_excel(self.file_path + self.stocks_file, sheet_name=1, index_col=None)
        for str_col in ['stock_id', 'ticker', 'updated_date']:
            updates_df[str_col] = updates_df[str_col].astype('string')
        df = pd.merge(stocks_df, updates_df, on=['stock_id', 'ticker'])
        return df


