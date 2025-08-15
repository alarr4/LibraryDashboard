import pandas as pd
import streamlit as st

# Load CSV file
df = pd.read_csv("books.csv")

# Fill missing values
df['Title'] = df['Title'].fillna("Unknown Title")
df['Author'] = df['Author'].fillna("Unknown Author")
df['YearPublished'] = df['YearPublished'].fillna(0)

# Calculate BookAge
df['BookAge'] = (pd.Timestamp.now().year - df['YearPublished']).clip(lower=0)

st.title("📚 Library Book Dashboard")

# 1️⃣ Author filter
authors = df['Author'].unique()
selected_author = st.selectbox("Select an Author:", authors)
filtered_df = df[df['Author'] == selected_author]

# 2️⃣ Year range filter
min_year = int(df['YearPublished'].min())
max_year = int(df['YearPublished'].max())
year_range = st.slider("Select Year Range:", min_year, max_year, (min_year, max_year))
filtered_df = filtered_df[(filtered_df['YearPublished'] >= year_range[0]) &
                          (filtered_df['YearPublished'] <= year_range[1])]

# 3️⃣ Display filtered table
st.dataframe(filtered_df)

# 4️⃣ Chart for filtered books
st.bar_chart(filtered_df['BookAge'])

# 5️⃣ Number of books per author
books_per_author = df.groupby('Author').size()
st.subheader("Number of Books per Author")
st.bar_chart(books_per_author)
# Switch MySQL to CSV for free deployment
