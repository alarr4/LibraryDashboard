import pandas as pd
import streamlit as st

# Load CSV
df = pd.read_csv("books.csv")

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Fill missing values
df['title'] = df['title'].fillna("Unknown Title")
df['author'] = df['author'].fillna("Unknown Author")
df['yearpublished'] = df['yearpublished'].fillna(0)

# Calculate BookAge and clip at 0
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

# Charts
st.subheader("Book Ages")
st.bar_chart(filtered_df['bookage'])

st.subheader("Number of Books per Author")
books_per_author = df.groupby('author').size()
st.bar_chart(books_per_author)
# Switch MySQL to CSV for free deployment
