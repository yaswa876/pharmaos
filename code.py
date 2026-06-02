import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
page_title="PharmaOS",
page_icon="🧬",
layout="wide"
)

# ---------------------------

# THEME

# ---------------------------

st.markdown("""

<style>
.main {
    background-color:#F5F4EF;
}
h1,h2,h3{
    color:#141412;
}
</style>

""", unsafe_allow_html=True)

# ---------------------------

# COLUMN DETECTION

# ---------------------------

def detect_type(col):
c = col.lower()

```
if "drug" in c:
    return "Drug"

if "gene" in c:
    return "Biomarker"

if "smiles" in c:
    return "Molecule"

if "phase" in c:
    return "Clinical Trial"

if "orr" in c:
    return "Clinical Outcome"

if "pfs" in c:
    return "Clinical Outcome"

if "os" in c:
    return "Clinical Outcome"

return "Generic"
```

# ---------------------------

# HEADER

# ---------------------------

st.title("🧬 PharmaOS")
st.caption("AI-Powered Drug Intelligence Platform")

# ---------------------------

# SIDEBAR

# ---------------------------

uploaded_file = st.sidebar.file_uploader(
"Upload Dataset",
type=["csv", "xlsx"]
)

if uploaded_file is None:
st.info("Upload a CSV or Excel file to begin analysis.")
st.stop()

# ---------------------------

# LOAD DATA

# ---------------------------

if uploaded_file.name.endswith(".csv"):
df = pd.read_csv(uploaded_file)
else:
df = pd.read_excel(uploaded_file)

# ---------------------------

# OVERVIEW

# ---------------------------

st.header("Dataset Overview")

c1, c2, c3 = st.columns(3)

c1.metric("Rows", len(df))
c2.metric("Columns", len(df.columns))
c3.metric("Missing Values", int(df.isnull().sum().sum()))

st.dataframe(df.head())

# ---------------------------

# DETECTED ENTITIES

# ---------------------------

st.header("Detected Biomedical Entities")

entity_df = pd.DataFrame({
"Column": df.columns,
"Detected Type": [detect_type(c) for c in df.columns]
})

st.dataframe(entity_df)

# ---------------------------

# DATA PROFILING

# ---------------------------

st.header("Column Analysis")

selected_col = st.selectbox(
"Choose Column",
df.columns
)

st.write(df[selected_col].describe())

# ---------------------------

# VISUALIZATION

# ---------------------------

st.header("Visualization")

numeric_cols = list(
df.select_dtypes(
include=["int64", "float64"]
).columns
)

if len(numeric_cols) > 0:

```
y_col = st.selectbox(
    "Select Numeric Column",
    numeric_cols
)

chart = px.histogram(
    df,
    x=y_col,
    title=y_col
)

st.plotly_chart(
    chart,
    use_container_width=True
)
```

# ---------------------------

# BIOMARKER ANALYSIS

# ---------------------------

st.header("Biomarker Intelligence")

bio_cols = [
c for c in df.columns
if detect_type(c) == "Biomarker"
]

if bio_cols:

```
biomarker_col = bio_cols[0]

biomarker_counts = (
    df[biomarker_col]
    .value_counts()
    .head(10)
)

fig = px.bar(
    biomarker_counts,
    title="Top Biomarkers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```

# ---------------------------

# DRUG ANALYSIS

# ---------------------------

st.header("Drug Intelligence")

drug_cols = [
c for c in df.columns
if detect_type(c) == "Drug"
]

if drug_cols:

```
drug_col = drug_cols[0]

drug_counts = (
    df[drug_col]
    .value_counts()
    .head(10)
)

fig = px.bar(
    drug_counts,
    title="Top Drugs"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
```

# ---------------------------

# QUERY ENGINE

# ---------------------------

st.header("Ask Your Dataset")

question = st.text_input(
"Example: rows, columns, describe ORR"
)

if question:

```
q = question.lower()

if "rows" in q:
    st.success(
        f"Dataset contains {len(df)} rows."
    )

elif "columns" in q:
    st.success(
        f"Dataset contains {len(df.columns)} columns."
    )

elif "describe" in q:

    matched = None

    for col in df.columns:
        if col.lower() in q:
            matched = col
            break

    if matched:
        st.dataframe(
            df[matched].describe()
        )
    else:
        st.warning(
            "Column not found."
        )

elif "highest" in q:

    nums = df.select_dtypes(
        include=["int64", "float64"]
    )

    if len(nums.columns) > 0:

        col = nums.columns[0]

        st.dataframe(
            df.loc[
                [df[col].idxmax()]
            ]
        )

else:

    st.info(
        "Connect an LLM later for advanced AI-powered answers."
    )
```

# ---------------------------

# EXPORT

# ---------------------------

st.header("Export Report")

csv = df.to_csv(index=False)

st.download_button(
"Download Dataset",
csv,
file_name="pharmaos_export.csv",
mime="text/csv"
)
