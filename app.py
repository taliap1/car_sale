import pandas as pd
import streamlit as st 
import plotly.express as px 

df = pd.read_csv('vehicles_us.csv')
df['price'] = df['price'].astype('int64')

df['paint_color'] = df['paint_color'].fillna('unknown')
df['is_4wd'] = df['is_4wd'].fillna(0)
df['model_year'] = df['model_year'].fillna(df.groupby('model')['model_year'].transform('median'))
df['odometer'] = df['odometer'].fillna(df.groupby('model_year')['odometer'].transform('median'))
df['cylinders'] = df['cylinders'].fillna(df.groupby('model')['cylinders'].transform('median'))

df['odometer'] = df['odometer'].fillna(0)

st.title ('Vehicle Selection App')
st.subheader ('Filter and choose your ideal vehicle')

st.caption (':blue[Choose your parameters here]')

price_range = st.slider(
    "What is your price range?",
    value= (0,375000)
)

filtered_df = df[df['price'].between(price_range[0], price_range[1]+1)]

include_condition = st.checkbox("Filter by Vehicle Condition")

if include_condition:
    selected_condition = st.selectbox("Select Vehicle Condition", options=filtered_df["condition"].unique())
    filtered_df = filtered_df[filtered_df["condition"] == selected_condition]
    
st.write('Here are your options price distribution by type')


fig1 = px.histogram(filtered_df, x = 'price', color= 'type',nbins = 10, title = 'Distribution of Vehicle Type')
st.plotly_chart(fig1)

st.write('Here are your options with a split by price and model year')

fig2 = px.scatter(filtered_df, x = 'model_year', y = 'price', title = 'Price vs. Model Year', labels = {'model_year': 'Model Year', 'price': 'Price'})
st.plotly_chart(fig2)

st.write('Here is the list of recommended vehicles')
st.dataframe(filtered_df.sample(40))