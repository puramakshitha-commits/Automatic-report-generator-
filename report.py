import streamlit as st
import pandas as pd
import numpy as np

# Page config
st.set_page_config(page_title="Automatic Report Generator", layout="wide")

st.title("📊 Automatic Report Generator")

# Upload file
file = st.file_uploader("Upload your CSV file", type=["csv"])

if file is not None:
    try:
        df = pd.read_csv(file)

        # Show data
        st.subheader("Dataset Preview")
        st.dataframe(df)

        # Info
        st.subheader("Basic Information")
        col1, col2 = st.columns(2)
        col1.write("Rows:", df.shape[0])
        col2.write("Columns:", df.shape[1])

        # Column names
        st.write("Column Names:", list(df.columns))

        # Summary
        st.subheader("Statistical Summary")
        st.write(df.describe())

        # Missing values
        st.subheader("Missing Values")
        st.write(df.isnull().sum())

        # Numeric columns
        num_cols = df.select_dtypes(include=np.number).columns.tolist()

        if len(num_cols) > 0:
            col = st.selectbox("Select column to visualize", num_cols)

            # Histogram
            st.subheader("Histogram")
            fig, ax = plt.subplots()
            ax.hist(df[col].dropna(), bins=15, color='blue')
            ax.set_title(f"Histogram of {col}")
            st.pyplot(fig)

            # Line chart
            st.subheader("Line Chart")
            st.line_chart(df[col])

        else:
            st.warning("No numeric columns found!")

        # Report generation
        if st.button("Generate Text Report"):
            report = f"""
AUTOMATIC REPORT
-------------------------
Rows: {df.shape[0]}
Columns: {df.shape[1]}

Columns:
{', '.join(df.columns)}

Missing Values:
{df.isnull().sum().to_string()}
"""
            st.download_button("Download Report", report, "report.txt")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Please upload a CSV file to begin.")