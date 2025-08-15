import pandas as pd
import streamlit as st
import altair as alt

# --- Load CSV ---
df = pd.read_csv("books.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Fill missing values
df['title'] = df['title'].fillna("Unknown Title")
df['author'] = df['author'].fillna("Unknown Author")
df['yearpublished'] = df['yearpublished'].fillna(0)

# Calculate BookAge
df['bookage'] = (pd.Timestamp.now().year - df['yearpublished']).clip(lower=0)

# --- Streamlit Layout ---
st.set_page_config(page_title="Library Dashboard", layout="wide")
st.title("📚 Library Book Dashboard")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
authors = df['author'].unique()
selected_author = st.sidebar.selectbox("Select an Author:", authors)

min_year = int(df['yearpublished'].min())
max_year = int(df['yearpublished'].max())
year_range = st.sidebar.slider("Select Year Range:", min_year, max_year, (min_year, max_year))

# Apply Sidebar Filters
filtered_df = df[(df['author'] == selected_author) &
                 (df['yearpublished'] >= year_range[0]) &
                 (df['yearpublished'] <= year_range[1])]

# --- Search Box & Sorting ---
search_term = st.text_input("Search for a Book Title:")
if search_term:
    filtered_df = filtered_df[filtered_df['title'].str.contains(search_term, case=False, na=False)]

sort_column = st.selectbox("Sort By:", ['title', 'author', 'yearpublished', 'bookage'])
sort_order = st.radio("Sort Order:", ['Ascending', 'Descending'])
ascending = True if sort_order == 'Ascending' else False
filtered_df = filtered_df.sort_values(by=sort_column, ascending=ascending)

# --- Key Metrics ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Books", len(filtered_df))
col2.metric("Oldest Book Year", int(filtered_df['yearpublished'].min()))
col3.metric("Newest Book Year", int(filtered_df['yearpublished'].max()))
col4.metric("Average Book Age", int(filtered_df['bookage'].mean()))

st.markdown("---")

# --- Filtered Table ---
st.subheader("Filtered Books")
st.dataframe(filtered_df[['title','author','yearpublished','bookage']], height=400)

# --- Charts Section ---
st.subheader("Visual Analytics")
chart_col1, chart_col2 = st.columns(2)

# 1️⃣ Book Ages Chart (Filtered)
bookage_chart = alt.Chart(filtered_df).mark_bar(color="#4CAF50").encode(
    x=alt.X('title:N', sort='-y', title='Book Title'),
    y=alt.Y('bookage:Q', title='Book Age', scale=alt.Scale(domain=[0, filtered_df['bookage'].max()])),
    tooltip=['title', 'author', 'bookage']
).properties(width=350, height=400)
chart_col1.altair_chart(bookage_chart, use_container_width=True)

# 2️⃣ Number of Books per Author (Filtered)
books_per_author_filtered = filtered_df.groupby('author').size().reset_index(name='count')
author_chart = alt.Chart(books_per_author_filtered).mark_bar(color="#2196F3").encode(
    x=alt.X('author:N', sort='-y', title='Author'),
    y=alt.Y('count:Q', title='Number of Books'),
    tooltip=['author', 'count']
).properties(width=350, height=400)
chart_col2.altair_chart(author_chart, use_container_width=True)

# 3️⃣ Total Books Published Per Year (Filtered)
books_per_year_filtered = filtered_df.groupby('yearpublished').size().reset_index(name='count')
year_chart = alt.Chart(books_per_year_filtered).mark_line(point=True, color="#FF5722").encode(
    x=alt.X('yearpublished:O', title='Year Published'),
    y=alt.Y('count:Q', title='Number of Books'),
    tooltip=['yearpublished', 'count']
).properties(width=700, height=400)
st.altair_chart(year_chart, use_container_width=True)
# Switch MySQL to CSV for free deployment
