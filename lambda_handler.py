import json
from datetime import datetime, timedelta
import pandas as pd
import os

os.makedirs('/tmp/data', exist_ok=True)
os.makedirs('/tmp/match_info', exist_ok=True)

def write_csv(filename, content):
    f = open('/tmp/data/' + filename, 'w')
    f.write(content)
    f.close()

def read_csv_as_string(filename):
    f = open(filename, 'r')

    content = ''

    for line in f.readlines():
        content += line.strip() + '\n'

    f.close()
    return content

def handler(event, lambda_context):
    body = json.loads(event['body'])

    write_csv('user.csv', body['user'])
    write_csv('access.csv', body['access'])
    write_csv('clan.csv', body['clan'])
    write_csv('character.csv', body['character'])
    write_csv('character_jelly.csv', body['character_jelly'])
    write_csv('jelly.csv', body['jelly'])

    # Data import
    folder_name = '/tmp/data'
    date_format = "%Y-%m-%d"
    today = datetime.now().strftime(date_format)

    target = (datetime.now() - timedelta(days=4)).strftime(date_format)

    # Managing Constants
    valid_visit_correction = 0.5
    no_visit_correction = 0.1
    initial_jelly_power = 10
    log_jelly_power = 0.4
    user_jelly_valid_cnt = 3

    team_initial_point = [0, 0, 0]

    target = datetime.strptime(target, date_format).date()

    user_filename = folder_name + '/user.csv'
    character_filename = folder_name + '/character.csv'
    character_jelly_filename = folder_name + '/character_jelly.csv'
    access_filename = folder_name + '/access.csv'
    jelly_filename = folder_name + '/jelly.csv'

    user = pd.read_csv(user_filename, low_memory=False)
    character = pd.read_csv(character_filename, low_memory=False)
    character_jelly = pd.read_csv(character_jelly_filename, low_memory=False)
    access = pd.read_csv(access_filename, parse_dates= ['accessed_at'], low_memory=False)
    jelly = pd.read_csv(jelly_filename, low_memory=False)
    
    import os
    os.remove(user_filename)
    os.remove(character_filename)
    os.remove(character_jelly_filename)
    os.remove(access_filename)
    os.remove(jelly_filename)

    # Data Preprocessing
    user = (user[['id', 'clan_id']]
            .rename(columns={'id': 'user_id'})
            .dropna())

    jelly = (jelly[['id', 'grade']])

    character_power = (character_jelly[['character_id', 'jelly_id', 'is_owned', 'exp']]
                    .query('is_owned == 1')
                    .merge(jelly, how = 'left', left_on = 'jelly_id', right_on = 'id')
                    .assign(power=lambda x: x.apply(lambda row: 1 if row['grade'] < 1 else
                                                    (2 if row['grade'] < 2 else
                                                    (4 if row['grade'] < 3 else 6)), axis=1))
                    .assign(power=lambda x: x['power'] * (x['exp'] + initial_jelly_power) ** log_jelly_power)
                    .groupby('character_id')
                    .head(user_jelly_valid_cnt)
                    .groupby('character_id')['power']
                    .sum()
                    .reset_index(name='jelly_power'))

    character = character[['user_id', 'id']].rename(columns={'id': 'character_id'})

    access['date'] = access['accessed_at'].dt.date

    user_visit = (access
            .assign(accessed_at=lambda x: pd.to_datetime(x['accessed_at']) + timedelta(hours=9)) # UTC to KST
            .assign(date=lambda x: x['accessed_at'].dt.date)
            .query('date >= @target')
            .loc[:, ['user_id', 'date']]
            .drop_duplicates()
            .groupby('user_id')
            .size()
            .reset_index(name='valid_visit')
            .assign(valid_visit=lambda x: x['valid_visit'] - valid_visit_correction))

    user_jelly = (user.merge(character, how='left', on='user_id')
                .merge(user_visit, how='left', on='user_id')
                .merge(character_power, how='left', on='character_id')
                .drop('character_id', axis=1)
                .fillna(no_visit_correction))

    # union_clan_match_service
    clan_filename = folder_name + '/clan.csv'
    clan = pd.read_csv(clan_filename)
    
    os.remove(clan_filename)

    clan = clan[['id', 'name']]

    union_list = pd.DataFrame({
        'union_name': ["LUNA", "SOLA", "VEGA"],
        'point': team_initial_point
    })

    clan_jelly = (user_jelly.groupby('clan_id')
                .agg(jelly_composite=('jelly_power', lambda x: (x * user_jelly['valid_visit']).sum()))
                .reset_index()
                .sort_values(by='jelly_composite', ascending=False))

    clan_jelly['union_name'] = None

    for i in range(len(clan_jelly)):
        now_union = union_list.assign(point=pd.to_numeric(union_list['point'])) \
                        .sort_values(by='point').head(1).loc[:, 'union_name'].values[0]

        clan_jelly.iloc[i, 2] = now_union
        union_list.loc[union_list['union_name'] == now_union, 'point'] += clan_jelly.iloc[i, 1]

    union_clan = (clan_jelly.sort_values(by='clan_id')
                .assign(union_id=lambda x: x['union_name'].apply(lambda name: 1 if name == 'SOLA' else (2 if name == 'LUNA' else 3)))
                .merge(clan, left_on='clan_id', right_on='id')
                .loc[:, ['name', 'clan_id', 'jelly_composite', 'union_name', 'union_id']]
                .rename(columns={'clan_id': 'clanId', 'union_id': 'unionId'}))

    match_info = union_clan[['clanId', 'unionId']].astype({'unionId': int, 'clanId': int})

    print(union_clan)
    print(match_info)
    print(union_list)

    print(clan_jelly.merge(clan, left_on = 'clan_id', right_on = 'id').head(30))

    output_directory = '/tmp/match_info'

    match_info_filename = '/tmp/match_info/match_info_' + str(today) + '.csv'
    match_info.to_csv(match_info_filename, index=False, header=['clanId', 'unionId'])
    print(match_info_filename)

    return {
        'statusCode': 200,
        'body': read_csv_as_string(match_info_filename)
    }
