import streamlit as st
import pandas as pd
import requests

def get_iso(id):
    country = []
    man_url = f'https://fantasy.premierleague.com/api/entry/{id}/'
    man_data = requests.get(man_url).json()
    iso3 = man_data['player_region_iso_code_long']
    iso2 = man_data['player_region_iso_code_short']
    if iso2 == 'EN':
        iso2 = 'gb-eng'
    elif iso2 == 'NN':
        iso2 = 'gb-nir'
    elif iso2 == 'S1':
        iso2 = 'gb-sct'
    elif iso2 == 'WA':
        iso2 = 'gb-wls'
    country.append(iso3)
    country.append(iso2)
    return country
    


#there are 2 pages for this league
json_url_1 = 'https://fantasy.premierleague.com/api/leagues-classic/2579/standings/?page_standings=1'
json_url_2 = 'https://fantasy.premierleague.com/api/leagues-classic/2579/standings/?page_standings=2'


data1 = requests.get(json_url_1).json()
results1 = data1['standings']['results']
data2 = requests.get(json_url_2).json()
results2 = data2['standings']['results']

league_name = data1['league']['name']
last_update = data1['last_updated_data']

# combine into 1 dataframe
results = results1 + results2

df = pd.json_normalize(results)
df['iso3'] = ''
df['iso2'] = ''

# loop through each manager to get country
for index, row in df.iterrows():
    country = []
    country = get_iso(row['entry'])
    df.at[index, 'iso3'] = country[0]
    df.at[index, 'iso2'] = country[1].lower()

df['flag'] = 'https://raw.githubusercontent.com/lipis/flag-icons/main/flags/4x3/' + df['iso2'] + '.svg'
app_df = df[['rank', 'flag', 'iso3', 'entry_name', 'player_name', 'event_total', 'total']]

# display to app
st.header(league_name)
st.markdown(f"*Last updated: {last_update}*")

st.dataframe(
    app_df,
    hide_index=True,
    height = 60*35,
    column_config = {
        "flag":st.column_config.ImageColumn(
            "flag",
            width="small"
        )
    }
)


# page 1 add to results, page 2 append to results list
# pd.json_normalize
# loop through all teams to get country and add to df
# format table and add flags


# flags
# https://github.com/joielechong/iso-country-flags-svg-collection/tree/master/svg/country-4x3
# https://github.com/lipis/flag-icons/tree/main/flags/4x3


# fpl manager api https://fantasy.premierleague.com/api/entry/244507/