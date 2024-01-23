# Assignment_DS
Question and Answers Dashboard
Initially  cleaned csv file is created using jsonl
The Streamlit application is designed to create a Question and Answers Dashboard using data from a CSV file. 

## Installation

git clone <repository-url>

pip install -r requirements.txt


## Usage

streamlit run your_script.py

## Features

Loads data from a CSV file (data_set.csv) using Pandas.
Provides filter options in the sidebar:
Filter by Yes/No Answer: Allows selecting a specific answer or displaying all.
Row Filters: Allows filtering rows based on specified text in columns like document_title, question_text, etc.

## Data Loading

The data is loaded and cached using Streamlit's @st.cache_data decorator to optimize performance.

## Results Display
Results are displayed in the main section of the dashboard. If no data matches the selected filters, a warning message is shown.
