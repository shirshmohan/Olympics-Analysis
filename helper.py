import numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team','NOC','Games','Year','City','Event','Medal','Sport'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver']+medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype(int)
    medal_tally['Silver'] = medal_tally['Silver'].astype(int)
    medal_tally['Bronze'] = medal_tally['Bronze'].astype(int)
    return medal_tally

def country_year_list(df):
    year = df['Year'].unique().tolist()
    country = np.unique(df['region'].dropna().values).tolist()
    year.sort()
    country.sort()
    year.insert(0,'Overall')
    country.insert(0,'Overall')
    return year,country

def fetch_medal_tally(df,year,country):
    medal_df = df.drop_duplicates(subset=['Team','NOC','Year','City','Sport','Event','Medal'])
    if year=='Overall' and country=='Overall':
        temp_df = medal_df
    if year=='Overall' and country !='Overall':
        temp_df = medal_df[medal_df['region']==country]
    if year!='Overall' and country !='Overall':
        temp_df = medal_df[(medal_df['Year']==year) &  (medal_df['region']==country)]
    if year!='Overall' and country =='Overall':
        temp_df = medal_df[medal_df['Year']==year]
    x = temp_df.groupby('region').sum()[['Gold','Silver','Bronze']].sort_values('Gold',ascending=False).reset_index()
    x['Total'] = x['Gold']+x['Silver']+x['Bronze']
    return x

def participating_nations_over_time(df):
    nations_over_time = df.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
    nations_over_time = nations_over_time.sort_values('Year').reset_index()
    nations_over_time = nations_over_time.drop('index', axis=1)
    nations_over_time = nations_over_time.rename(columns={'Year':'Edition','count':'No of Countries'})
    return nations_over_time
def events_over_time(df):
    events_over_time = df.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()
    events_over_time = events_over_time.sort_values('Year')
    events_over_time = events_over_time.rename(columns={'Year': 'Edition', 'count': 'Event'})
    return events_over_time
def athlete_over_time(df):
    athletes_over_time = df.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index()
    athletes_over_time = athletes_over_time.sort_values('Year')
    athletes_over_time = athletes_over_time.rename(columns={'Year': 'Edition', 'count': 'No of Athletes'})
    return athletes_over_time

def most_sucessful(df,sport):
    temp_df = df.dropna(subset='Medal')
    temp_df.head()

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]
    merge_df = temp_df['Name'].value_counts().reset_index().head(15).merge(df,left_on='Name',right_on='Name',how='left')
    return merge_df[['Name','count','region','Sport']].drop_duplicates(['Name'])

def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset='Medal')
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == country]
    return new_df.groupby('Year').count()['Medal'].reset_index()

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_df = temp_df[temp_df['region'] == 'India']
    pt = new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)
    return pt

def most_successful_countrywise(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region']==country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(df,left_on='Name',right_on='Name',how='left')[['Name','count','Sport']]

    return x.drop_duplicates(subset=['Name'])

def weight_y_height(df,sport):
    athlete_df = df.drop_duplicates(subset=['region','Name'])
    athlete_df['Medal'].fillna('No Medal',inplace=True)
    temp_df = athlete_df
    if sport != 'Overall':
        temp_df = athlete_df[athlete_df['Sport']==sport]
    return temp_df
def men_women(df):
    athlete_df = df.drop_duplicates(subset=['region','Name'])
    men = athlete_df[athlete_df['Sex']== 'M'].groupby('Year')['Name'].count().reset_index()
    women = athlete_df[athlete_df['Sex']=='F'].groupby('Year')['Name'].count().reset_index()
    final = men.merge(women,on='Year',how='left')
    final.rename(columns={'Name_x':'Male','Name_y':'Female'},inplace=True)
    final.fillna(0,inplace=True)
    return final