import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine

st.set_page_config(layout="wide")
st.title("🎮 IMDb 2024 Movie Data Dashboard")

# Database connection
user = "root"
password = "root"
host = "localhost"
database = "imdb_movies"
engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")

@st.cache_data
def load_data():
    return pd.read_sql("SELECT * FROM movies_2024", engine)

df = load_data()

# Convert datatypes
df["Ratings"] = pd.to_numeric(df["Ratings"], errors="coerce")
df["Voting counts"] = pd.to_numeric(df["Voting counts"], errors="coerce")
df["Duration"] = pd.to_numeric(df["Duration"], errors="coerce")

# ----- STATIC VISUALIZATIONS (NO FILTERS) -----

# 1. Top 10 Movies by Rating and Voting Counts
st.subheader("01. Top 10 Movies by Rating and Voting Counts")
top_movies = df.sort_values(["Ratings", "Voting counts"], ascending=[False, False]).head(10)
st.dataframe(top_movies[["Movie name", "Genre", "Ratings", "Voting counts"]])
st.bar_chart(top_movies.set_index("Movie name")[["Ratings"]])

# 2. Genre Distribution
st.subheader("02. Genre Distribution")
genre_counts = df["Genre"].value_counts()
st.bar_chart(genre_counts)

# 3. Average Duration by Genre
st.subheader("03. Average Duration by Genre")
avg_duration = df.groupby("Genre")["Duration"].mean().sort_values()
st.bar_chart(avg_duration)

# 4. Voting Trends by Genre
st.subheader("04. Average Voting Counts by Genre")
avg_votes = df.groupby("Genre")["Voting counts"].mean().sort_values()
st.bar_chart(avg_votes)

# 5. Rating Distribution
st.subheader("05. Rating Distribution")
fig1, ax1 = plt.subplots()
sns.histplot(df["Ratings"], bins=20, kde=True, ax=ax1)
st.pyplot(fig1)

# 6. Genre-Based Rating Leaders
st.subheader("06. Top Rated Movie in Each Genre")
idx = df.groupby("Genre")["Ratings"].idxmax()
top_by_genre = df.loc[idx]
st.dataframe(top_by_genre[["Genre", "Movie name", "Ratings"]])

# 7. Most Popular Genres by Total Votes (Pie)
st.subheader("07. Most Popular Genres by Total Votes")
votes_by_genre = df.groupby("Genre")["Voting counts"].sum()
fig2, ax2 = plt.subplots()
ax2.pie(votes_by_genre, labels=votes_by_genre.index, autopct="%1.1f%%", startangle=90)
ax2.axis("equal")
st.pyplot(fig2)

# 8. Duration Extremes
st.subheader("08. Shortest and Longest Movies")
shortest = df.sort_values("Duration").head(1)
longest = df.sort_values("Duration").tail(1)
st.write("🎮 **Shortest Movie**:")
st.dataframe(shortest[["Movie name", "Genre", "Duration"]])
st.write("🎮 **Longest Movie**:")
st.dataframe(longest[["Movie name", "Genre", "Duration"]])

# 9. Ratings by Genre Heatmap
st.subheader("09. Heatmap: Average Ratings by Genre")
heatmap_data = df.pivot_table(values="Ratings", index="Genre", aggfunc="mean")
fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax3)
st.pyplot(fig3)

# 10. Correlation: Ratings vs Voting Counts
st.subheader("10. Ratings vs Voting Counts (Scatter Plot)")
fig4, ax4 = plt.subplots()
sns.scatterplot(data=df, x="Voting counts", y="Ratings", hue="Genre", ax=ax4)
st.pyplot(fig4)

# ----- INTERACTIVE FILTERING FUNCTIONALITY -----
st.title("🔍 Interactive Filtering Functionality")

# Duration filter
duration_option = st.selectbox("Select Duration Range:", ["All", "< 2 hours", "2–3 hours", "> 3 hours"])
if duration_option == "< 2 hours":
    filtered_df = df[df["Duration"] < 120]
elif duration_option == "2–3 hours":
    filtered_df = df[(df["Duration"] >= 120) & (df["Duration"] <= 180)]
elif duration_option == "> 3 hours":
    filtered_df = df[df["Duration"] > 180]
else:
    filtered_df = df.copy()

# Rating filter
min_rating = st.slider("Minimum Rating", 0.0, 10.0, 7.0)
filtered_df = filtered_df[filtered_df["Ratings"] >= min_rating]

# Voting count filter
min_votes = st.number_input("Minimum Votes", min_value=0, value=10000)
filtered_df = filtered_df[filtered_df["Voting counts"] >= min_votes]

# Genre filter
genre_filter = st.multiselect("Select Genres", options=df["Genre"].unique(), default=list(df["Genre"].unique()))
filtered_df = filtered_df[filtered_df["Genre"].isin(genre_filter)]

st.subheader("🎮 Filtered Movies Table")
st.dataframe(filtered_df.reset_index(drop=True))
