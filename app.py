import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

st.title("📦 Upload IMDb 2024 CSV to MySQL Database")

# Step 1: Upload CSV
uploaded_file = st.file_uploader("Upload the merged IMDb 2024 CSV file", type=["csv"])

# Step 2: MySQL Connection Inputs
st.subheader("Enter MySQL Database Credentials")
user = st.text_input("Username", value="root")
password = st.text_input("Password", type="password")
host = st.text_input("Host", value="localhost")
port = st.text_input("Port", value="3306")
database = st.text_input("Database Name", value="imdb_movies")

# Step 3: When file is uploaded
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("✅ Preview of uploaded data:")
    st.dataframe(df.head())

    if st.button("Upload to SQL"):
        try:
            engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{database}')
            df.to_sql(name='movies_2024', con=engine, if_exists='replace', index=False)
            st.success("🎉 Successfully uploaded to MySQL table `movies_2024`!")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")
