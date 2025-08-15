import pandas as pd
import streamlit as st

# Load CSV
df = pd.read_csv("books.csv")

# Normalize column names (lowercase, no spaces)
df.columns = df.columns.str.strip().str.lower()

# Fill missing values
df['title'] = df['title'].fillna("Unknown Title")
df['author'] = df['author'].fillna("Unknown Author")
df['yearpublished'] = df['yearpublished'].fillna(0)

# Calculate BookAge and clip at 0
df['bookage'] = (pd.Timestamp.now().year - df['yearpublished']).clip(lower=0)

st.title("📚 Library Book Dashboard")

# 1️⃣ Author filter
authors = df['author'].unique()
selected_author = st.selectbox("Select an Author:", authors)
filtered_df = df[df['author'] == selected_author]

# 2️⃣ Year range filter
min_year = int(df['yearpublished'].min())
max_year = int(df['yearpublished'].max())
year_range = st.slider("Select Year Range:", min_year, max_year, (min_year, max_year))
filtered_df = filtered_df[(filtered_df['yearpublished'] >= year_range[0]) &
                          (filtered_df['yearpublished'] <= year_range[1])]

# 3️⃣ Display filtered table
st.dataframe(filtered_df[['title','author','yearpublished','bookage']])

# 4️⃣ Chart for filtered books
st.bar_chart(filtered_df['bookage'])

# 5️⃣ Number of books per author
books_per_author = df.groupby('author').size()
st.subheader("Number of Books per Author")
st.bar_chart(books_per_author)
# Switch MySQL to CSV for free deployment
