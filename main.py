import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout='wide',page_title='Startup Analysis')

df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors='coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
#st.dataframe(df)

def load_overall_analysis():
    st.title('Overall Analysis')

    # total invested amount
    total = round(df['amount'].sum())


    # max amount infused in startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]


    # mean amount infused in startup
    mean_fund = df.groupby('startup')['amount'].sum().mean()


    # total funded startup
    num_startups = df['startup'].nunique()

    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + ' Cr')

    with col2:
        st.metric('Max', str(max_funding) + ' Cr')

    with col3:
        st.metric('Average',str(round(mean_fund))+' Cr')

    with col4:
        st.metric('Total startups',num_startups)


    st.header('MoM graph')

    selected_option = st.selectbox('Select Type',['Total','Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()


    temp_df['x_axis'] = temp_df['year'].astype('str') + '-' +temp_df['month'].astype('str')
    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig3)



def load_investors_detail(investor):
    st.title(investor)
    ## loading recent 5 investment of investors -1
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    ## biggest_investment -2
    col1,col2 = st.columns(2)
    with col1:
        big_series = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.subheader('biggest_investment')
           # st.dataframe(big_series)
        fig,ax = plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

    ## biggest_vertical -3
    with col2:
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum()
        st.subheader('Sector Invested in')
        fig1,ax1 = plt.subplots()
        ax1.pie(vertical_series,labels=vertical_series.index)
        st.pyplot(fig1)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index,year_series.values)
    st.pyplot(fig2)



option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup Details')
    st.title('Startup')
else:
    selected_investor = st.sidebar.selectbox('Select Investor',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investors_detail(selected_investor)





