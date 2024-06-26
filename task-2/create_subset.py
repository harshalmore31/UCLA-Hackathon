import dask.dataframe as dd
import os
import pandas as pd
df = dd.read_csv('train_data_ads.csv', dtype={'ad_close_list_v001': 'object', 'ad_close_list_v002': 'object', 'ad_close_list_v003': 'object'})

df = df.sample(frac = 0.2, random_state = 10)
df = df.drop(['ad_click_list_v001', 'ad_click_list_v002', 'ad_click_list_v003', 'log_id', 'user_id'], axis = 1)

pos = df[df['label'] == 1]
neg = df[df['label'] == 0]

pos = pos.compute()
neg = neg.compute()

neg['u_newsCatInterestsST'] = neg['u_newsCatInterestsST'].apply(lambda row: 1 if '0' in row.split('^') else 0)
pos['u_newsCatInterestsST'] = pos['u_newsCatInterestsST'].apply(lambda row: 1 if '0' in row.split('^') else 0)

neg.to_csv('final_neg.csv', index=False)
pos.to_csv('final_pos.csv', index=False)