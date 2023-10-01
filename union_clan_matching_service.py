import pandas as pd
from datetime import datetime, timedelta

# Data import
folder_name = '0922'
today = '2023-09-22'
target = '2023-09-18'

user_filename = f'{folder_name}/user.csv'
character_filename = f'{folder_name}/character.csv'
character_jelly_filename = f'{folder_name}/character_jelly.csv'
access_filename = f'{folder_name}/access.csv'

user = pd.read_csv(user_filename, low_memory=False)
character = pd.read_csv(character_filename, low_memory=False)
character_jelly = pd.read_csv(character_jelly_filename, low_memory=False)
access = pd.read_csv(access_filename, low_memory=False)

# Data Preprocessing
user = (user[['id', 'clan_id']]
        .rename(columns={'id': 'user_id'})
        .dropna())

character_power = (character_jelly[['character_id', 'jelly_id', 'is_owned', 'exp']]
                   .query('is_owned == 1')
                   .assign(power=lambda x: x.apply(lambda row: 1 if row['jelly_id'] <= 1003 else
                                                   (2 if row['jelly_id'] <= 1008 else
                                                   (4 if row['jelly_id'] <= 1012 else 6)), axis=1))
                   .assign(power=lambda x: x['power'] * (x['exp'] + 10) ** (1 / 2))
                   .groupby('character_id')
                   .head(3)
                   .groupby('character_id')['power']
                   .sum()
                   .reset_index(name='jelly_power'))

character = character[['user_id', 'id']].rename(columns={'id': 'character_id'})

access['accessed_at'] = pd.to_datetime(access['accessed_at']) + timedelta(hours=9)
access['date'] = access['accessed_at'].dt.date
user_visit = (access.query('accessed_at >= @target')
              .drop_duplicates(subset=['user_id', 'date'])
              .groupby('user_id')
              .size()
              .sub(0.9)
              .reset_index(name='valid_visit'))

user_jelly = (user.merge(character, how='left', on='user_id')
              .merge(user_visit, how='left', on='user_id')
              .merge(character_power, how='left', on='character_id')
              .fillna(0.5))

# union_clan_match_service

clan_filename = f'{folder_name}/clan.csv'
clan = pd.read_csv(clan_filename)

clan = clan[['id', 'name']]

union_list = pd.DataFrame({
    'union_name': ["LUNA", "SOLA", "VEGA"],
    'point': [0, 0, 0]
})

clan_jelly = (user_jelly.groupby('clan_id')
              .agg(jelly_composite=('jelly_power', 'sum'))
              .reset_index()
              .sort_values(by='jelly_composite', ascending=False))

for i in range(len(clan_jelly)):
    now_union = union_list.sort_values(by='point').head(1)['union_name'].values[0]
    clan_jelly.at[i, 'union_name'] = now_union
    union_list.loc[union_list['union_name'] == now_union, 'point'] += clan_jelly.at[i, 'jelly_composite']

union_clan = (clan_jelly.sort_values(by='clan_id')
              .assign(union_id=lambda x: x['union_name'].apply(lambda name: 1 if name == 'SOLA' else (2 if name == 'LUNA' else 3)))
              .merge(clan, left_on='clan_id', right_on='id')
              .loc[:, ['name', 'clan_id', 'jelly_composite', 'union_name', 'union_id']]
              .rename(columns={'name': 'clanId', 'union_id': 'unionId'}))

match_info = union_clan[['clanId', 'unionId']].astype({'unionId': int})

print(union_clan)
print(match_info) # 완성

# write csv (아래 부분은 필요 없음)
import os
# 'match_info' 디렉터리가 존재하지 않는 경우 생성
output_directory = 'match_info'
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

match_info_filename = f'match_info/match_info_{folder_name}.csv'
match_info.to_csv(match_info_filename, index=False, header=['clanId', 'unionId'])