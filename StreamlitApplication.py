import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    data = pd.read_csv(
        './results/data_set.csv')
    return data


df = load_data()

columns = df.columns

st.sidebar.header('Filter Options')

selected_yes_no_answer = st.sidebar.selectbox('Select Yes/No Answer', ['All'] + df['yes_no_answer'].unique().tolist())

filtered_df = df.copy()

if selected_yes_no_answer != 'All':
    filtered_df = filtered_df[filtered_df['yes_no_answer'] == selected_yes_no_answer]

st.sidebar.header('Row Filters')
row_filters = {}
for column in ['document_title', 'question_text', 'short_answer1', 'short_answer2', 'short_answer3', 'short_answer4',
               'short_answer5', 'short_answer6']:
    row_filters[column] = st.sidebar.text_input(f'Filter rows where {column} contains:', '')

for column, filter_value in row_filters.items():
    if filter_value:
        filtered_df = filtered_df[filtered_df[column].str.contains(filter_value, case=False, na=False)]

st.title('Question and Answers Dashboard')

if not filtered_df.empty:
    st.subheader('Results')
    st.write(filtered_df)
else:
    st.warning('No data matching the selected filters.')
