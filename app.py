import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')
df = preprocessor.preprocess(df,region_df)
st.sidebar.title("Olympics Analysis")
st.sidebar.image('https://e7.pngegg.com/pngimages/1020/402/png-clipart-2024-summer-olympics-brand-circle-area-olympic-rings-olympics-logo-text-sport.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally','Overall Analysis','Country-wise Analysis','Athlete wise Analysis')
)




if user_menu == 'Medal Tally':

    st.sidebar.header("Medal Tally")
    year,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",year)
    selected_country = st.sidebar.selectbox("Select country",country)
    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year=='Overall' and selected_country=='Overall':
        st.title('Overall Tally')
    if selected_year=='Overall' and selected_country!='Overall':
        st.title('Overall ' + selected_country + ' Tally Over the Years')
    if selected_year!='Overall' and  selected_country=='Overall':
        st.title('Overall  medal tally of countries in the year ' + str(selected_year))
    if selected_year!='Overall' and selected_country!='Overall':
        st.title('Medall tally of '+ selected_country+' in the year '+ str(selected_year))
    st.dataframe(medal_tally)
if user_menu == 'Overall Analysis':
    editions = df['Year'].unique().shape[0]-1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("Editions")
        st.title(editions)
    with col2:
        st.header("Hosts")
        st.title(editions)
    with col3:
        st.header("Sports")
        st.title(sports)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("Events")
        st.title(events)
    with col2:
        st.header("Nations")
        st.title(nations)
    with col3:
        st.header("Athletes")
        st.title(athletes)
    nations_over_time = helper.participating_nations_over_time(df)
    fig = px.line(nations_over_time,x="Edition",y="No of Countries")
    st.title('Participating Nations Overtime')
    st.plotly_chart(fig)

    events_over_time = helper.events_over_time(df)
    fig = px.line(events_over_time,x='Edition',y='Event')
    st.title('Events over the Year')
    st.plotly_chart(fig)

    athletes_over_time = helper.athlete_over_time(df)
    fig = px.line(athletes_over_time, x='Edition', y='No of Athletes')
    st.title('Athlete Count over the years')
    st.plotly_chart(fig)

    st.title('No of Events over time(Every Sport)')
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year','Sport','Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0),annot=True)
    st.pyplot(fig)

    st.title("Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a sport',sport_list)
    x = helper.most_sucessful(df,selected_sport)
    x.reset_index()
    st.table(x)
if user_menu == 'Country-wise Analysis':
    st.title('Country-wise Analysis')
    country_list = list(df['region'].unique())
    country_list = [str(x) for x in country_list]
    country_list.sort()
    selected_country = st.selectbox('Select country',country_list)
    country_df = helper.yearwise_medal_tally(df,selected_country)
    st.title(selected_country + " medal tally over the years")
    fig = px.line(country_df,x='Year',y='Medal')
    st.plotly_chart(fig)

    st.title(selected_country+'-Sport Analysis')
    pt = helper.country_event_heatmap(df,selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.title("Top 10 athletes of "+ selected_country)
    st.table(top10_df)

if user_menu == "Athlete wise Analysis":
    athlete_df = df.drop_duplicates(subset=['Name','region'])

    x2 = athlete_df[athlete_df['Medal']=='Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal']=='Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal']=='Bronze']['Age'].dropna()
    x1 = athlete_df['Age'].dropna()

    fig = ff.create_distplot([x1,x2,x3,x4],['Overall age','Gold Medalist','Silver Medalist','Bronze Medalist'],show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport']==sport]
        x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x,name,show_hist=False,show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    selected_sport = st.selectbox('Select a sport',sport_list)
    temp_df = helper.weight_y_height(df, selected_sport)
    fig,ax = plt.subplots(figsize=(10,10))
    ax = sns.scatterplot(x=temp_df['Weight'],y=temp_df['Height'],hue=temp_df['Medal'])
    st.pyplot(fig)

    st.title('Men vs Women participation over the years')
    final = helper.men_women(df)
    fig = px.line(final,x='Year',y=['Male','Female'])
    st.plotly_chart(fig)
  