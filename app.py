import mysql.connector
import pandas as pd
import streamlit as st
import altair as alt

# ----------------------------
# Connect to MySQL
# ----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="voc1Esaymbran#",
    database="Library"
)

# ----------------------------
# Query the Books table
# ----------------------------
query = """
SELECT Title, Author, YearPublished,
       YEAR(CURDATE()) - YearPublished AS BookAge
FROM Books;
"""
df = pd.read_sql(query, conn)

# ----------------------------
# Streamlit Title
# ----------------------------
st.title("📚 Library Book Dashboard")
st.markdown("Interactive dashboard to explore book data by author and year published.")

# ----------------------------
# Filters
# ----------------------------
# Author filter
authors = df['Author'].unique()
selected_author = st.selectbox("Select an Author:", authors)
filtered_df = df[df['Author'] == selected_author]

# Year range filter
min_year = int(df['YearPublished'].min())
max_year = int(df['YearPublished'].max())
year_range = st.slider("Select Year Range:", min_year, max_year, (min_year, max_year))
filtered_df = filtered_df[(filtered_df['YearPublished'] >= year_range[0]) &
                          (filtered_df['YearPublished'] <= year_range[1])]

# Prevent negative BookAge
filtered_df['BookAge'] = filtered_df['BookAge'].clip(lower=0)

# ----------------------------
# Metrics / KPIs
# ----------------------------
st.subheader("📌 Key Metrics")
col1, col2 = st.columns(2)
col1.metric("Total Books", len(filtered_df))
col2.metric("Average Book Age", round(filtered_df['BookAge'].mean(), 1))

# ----------------------------
# Data Table
# ----------------------------
st.subheader("Filtered Books")
st.dataframe(filtered_df)

# ----------------------------
# Bar Chart for Book Age
# ----------------------------
st.subheader("📊 Book Age Chart")
age_chart = alt.Chart(filtered_df).mark_bar(color='teal').encode(
    x='Title',
    y='BookAge',
    tooltip=['Title', 'BookAge', 'YearPublished']
)
st.altair_chart(age_chart, use_container_width=True)

# ----------------------------
# Number of Books per Author
# ----------------------------
st.subheader("📊 Number of Books per Author")
books_per_author = df.groupby('Author').size().reset_index(name='BookCount')
author_chart = alt.Chart(books_per_author).mark_bar(color='orange').encode(
    x='Author',
    y='BookCount',
    tooltip=['Author', 'BookCount']
)
st.altair_chart(author_chart, use_container_width=True)
