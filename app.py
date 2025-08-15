import pandas as pd
import streamlit as st
import altair as alt

# Load CSV
df = pd.read_csv("books.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Fill missing values
df['title'] = df['title'].fillna("Unknown Title")
df['author'] = df['author'].fillna("Unknown Author")
df['yearpublished'] = df['yearpublished'].fillna(0)

# Calculate BookAge
df['bookage'] = (pd.Timestamp.now().year - df['yearpublished']).clip(lower=0)

# --- Streamlit UI ---
st.set_page_config(page_title="Library Dashboard", layout="wide")
st.title("📚 Library Book Dashboard")

# Key Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", len(df))
col2.metric("Oldest Book Year", int(df['yearpublished'].min()))
col3.metric("Newest Book Year", int(df['yearpublished'].max()))
col4.metric("Average Book Age", int(df['bookage'].mean()))

st.markdown("---")

# Filters
authors = df['author'].unique()
selected_author = st.selectbox("Select an Author:", authors)
filtered_df = df[df['author'] == selected_author]

min_year = int(df['yearpublished'].min())
max_year = int(df['yearpublished'].max())
year_range = st.slider("Select Year Range:", min_year, max_year, (min_year, max_year))
filtered_df = filtered_df[(filtered_df['yearpublished'] >= year_range[0]) &
                          (filtered_df['yearpublished'] <= year_range[1])]

# Display table
st.subheader("Filtered Books")
st.dataframe(filtered_df[['title','author','yearpublished','bookage']], height=400)

# --- Charts ---

# 1️⃣ Book Ages Chart (Altair)
st.subheader("Book Ages")
bookage_chart = alt.Chart(filtered_df).mark_bar(color="#4CAF50").encode(
    x=alt.X('title:N', sort='-y', title='Book Title'),
    y=alt.Y('bookage:Q', title='Book Age'),
    tooltip=['title', 'author', 'bookage']
).properties(width=700, height=400)
st.altair_chart(bookage_chart, use_container_width=True)

# 2️⃣ Number of Books per Author
st.subheader("Number of Books per Author")
books_per_author = df.groupby('author').size().reset_index(name='count')
author_chart = alt.Chart(books_per_author).mark_bar(color="#2196F3").encode(
    x=alt.X('author:N', sort='-y', title='Author'),
    y=alt.Y('count:Q', title='Number of Books'),
    tooltip=['author', 'count']
).properties(width=700, height=400)
st.altair_chart(author_chart, use_container_width=True)
# 3️⃣ Total Books Published Per Year
st.subheader("Total Books Published Per Year")
books_per_year = df.groupby('yearpublished').size().reset_index(name='count')

year_chart = alt.Chart(books_per_year).mark_line(point=True, color="#FF5722").encode(
    x=alt.X('yearpublished:O', title='Year Published'),
    y=alt.Y('count:Q', title='Number of Books'),
    tooltip=['yearpublished', 'count']
).properties(width=700, height=400)

st.altair_chart(year_chart, use_container_width=True)
# Switch MySQL to CSV for free deployment
