# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

st.set_page_config(page_title="CSV Data Explorer", layout="wide")

# ------------------- Sidebar: File Upload -------------------
st.sidebar.title("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])

use_sample = st.sidebar.checkbox("Use sample dataset")

# ------------------- Load Data -------------------
@st.cache_data
def load_data(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    else:
        return pd.read_excel(file)

@st.cache_data
def get_sample_data():
    return pd.DataFrame({
        "date": pd.date_range("2023-01-01", periods=10),
        "category": ["A", "B"] * 5,
        "value": [5, 7, 3, 8, 2, 9, 4, 6, 1, 10]
    })

df = None
if uploaded_file:
    try:
        df = load_data(uploaded_file)
    except Exception as e:
        st.error(f"❌ Failed to load file: {e}")
elif use_sample:
    df = get_sample_data()

if df is not None:
    st.title("📊 CSV Data Explorer Dashboard")

    # ------------------- Data Overview -------------------
    with st.expander("📌 Data Overview", expanded=True):
        st.subheader("Data Preview")
        st.dataframe(df, use_container_width=True)

        st.subheader("Data Summary")
        st.write(df.describe(include='all').transpose())

        st.subheader("Missing Values")
        st.write(df.isnull().sum())

        st.subheader("Column Types")
        st.write(df.dtypes)

    # ------------------- Filtering -------------------
    with st.expander("🔍 Filter Data"):
        filters = {}
        for col in df.columns:
            if df[col].dtype in [int, float]:
                min_val, max_val = float(df[col].min()), float(df[col].max())
                filters[col] = st.slider(f"{col} range", min_val, max_val, (min_val, max_val))
            elif df[col].dtype == object or df[col].dtype.name == "category":
                unique_vals = df[col].dropna().unique()
                filters[col] = st.multiselect(f"Select {col}", unique_vals, default=list(unique_vals))
        df_filtered = df.copy()
        for col, val in filters.items():
            if isinstance(val, tuple):
                df_filtered = df_filtered[df_filtered[col].between(*val)]
            else:
                df_filtered = df_filtered[df_filtered[col].isin(val)]

        st.write(f"Filtered Rows: {len(df_filtered)}")
        st.dataframe(df_filtered, use_container_width=True)

    # ------------------- Visualizations -------------------
    with st.expander("📈 Visualize"):
        numeric_cols = df_filtered.select_dtypes(include=["int", "float"]).columns.tolist()
        categorical_cols = df_filtered.select_dtypes(include=["object", "category"]).columns.tolist()

        chart_type = st.selectbox("Chart Type", ["Histogram", "Scatter", "Bar", "Pie", "Line"])

        if chart_type == "Histogram":
            col = st.selectbox("Select Numeric Column", numeric_cols)
            fig = px.histogram(df_filtered, x=col)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Scatter":
            x_col = st.selectbox("X Axis", numeric_cols)
            y_col = st.selectbox("Y Axis", numeric_cols, index=1 if len(numeric_cols) > 1 else 0)
            fig = px.scatter(df_filtered, x=x_col, y=y_col, color=categorical_cols[0] if categorical_cols else None)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Bar":
            cat_col = st.selectbox("Category Column", categorical_cols)
            val_col = st.selectbox("Value Column", numeric_cols)
            fig = px.bar(df_filtered, x=cat_col, y=val_col, color=cat_col)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Pie":
            cat_col = st.selectbox("Category Column", categorical_cols)
            fig = px.pie(df_filtered, names=cat_col)
            st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Line":
            x_col = st.selectbox("X Axis", df_filtered.columns, index=0)
            y_col = st.selectbox("Y Axis", numeric_cols)
            fig = px.line(df_filtered, x=x_col, y=y_col)
            st.plotly_chart(fig, use_container_width=True)

    # ------------------- Export Options -------------------
    with st.expander("⬇️ Export"):
        st.subheader("Download Filtered Data")
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", csv, "filtered_data.csv", "text/csv")

        st.subheader("Download Summary Stats")
        stats = df_filtered.describe().to_csv().encode("utf-8")
        st.download_button("Download Stats CSV", stats, "summary.csv", "text/csv")

else:
    st.info("Upload a dataset from the sidebar to begin.")
