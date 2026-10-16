import io
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="CSV/Excel Data Cleaning Assistant", page_icon="🧹", layout="wide"
)

st.title("🧹 CSV/Excel Data Cleaning Assistant")
st.markdown(
    "Upload your dataset, check missing values, remove duplicates, convert types, rename columns, visualize data, and export polished files!"
)

# Sidebar for File Upload
st.sidebar.header("1. Upload Dataset")
uploaded_file = st.sidebar.file_uploader(
    "Choose a CSV or Excel file", type=["csv", "xlsx", "xls"]
)

if uploaded_file is not None:
  try:
    if uploaded_file.name.endswith(".csv"):
      df = pd.read_csv(uploaded_file)
    else:
      df = pd.read_excel(uploaded_file)
  except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

  st.success(f"Successfully uploaded **{uploaded_file.name}**[cite: 1]!")

  # --- Dataset Overview ---
  st.header("📊 Dataset Overview")
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Rows", df.shape[0])
  col2.metric("Total Columns", df.shape[1])
  col3.metric("Total Missing Values", int(df.isnull().sum().sum()))

  with st.expander("🔍 Preview Raw Data"):
    st.dataframe(df.head(10))

  # --- Column Management (Rename & Type Conversion) ---
  st.header("⚙️ Column Management (Rename & Type Conversion)")

  with st.expander("Rename Columns"):
    st.write("Modify column names below:")
    rename_dict = {}
    for col in df.columns:
      new_name = st.text_input(f"Rename `{col}` to:", value=col, key=f"rename_{col}")
      if new_name != col:
        rename_dict[col] = new_name

    if rename_dict and st.button("Apply Column Renaming"):
      df = df.rename(columns=rename_dict)
      st.success("Columns successfully renamed! Please check the preview below.")

  with st.expander("Change Column Data Types"):
    col_to_convert = st.selectbox(
        "Select Column", options=df.columns, key="dtype_col"
    )
    new_type = st.selectbox(
        "Target Data Type", options=["int", "float", "str", "datetime"]
    )
    if st.button("Convert Data Type"):
      try:
        if new_type == "int":
          df[col_to_convert] = pd.to_numeric(
              df[col_to_convert], errors="coerce"
          ).astype("Int64")
        elif new_type == "float":
          df[col_to_convert] = pd.to_numeric(
              df[col_to_convert], errors="coerce"
          )
        elif new_type == "str":
          df[col_to_convert] = df[col_to_convert].astype(str)
        elif new_type == "datetime":
          df[col_to_convert] = pd.to_datetime(
              df[col_to_convert], errors="coerce"
          )
        st.success(
            f"Successfully converted `{col_to_convert}` to `{new_type}`!"
        )
      except Exception as e:
        st.error(f"Conversion failed: {e}")

  # --- Data Quality Analysis (Missing Value Summary & Duplicates) ---
  st.header("🔍 Data Quality Analysis")
  missing_df = pd.DataFrame(
      {
          "Missing Count": df.isnull().sum(),
          "Missing Percentage (%)": (df.isnull().mean() * 100).round(2),
      }
  )
  st.dataframe(missing_df[missing_df["Missing Count"] > 0])

  duplicate_count = df.duplicated().sum()
  st.info(f"Number of duplicate rows found: **{duplicate_count}**")

  # --- Data Cleaning Operations ---
  st.header("🛠️ Data Cleaning Operations")

  # 1. Duplicate Removal
  if duplicate_count > 0:
    if st.checkbox("Remove Duplicate Rows"):
      df = df.drop_duplicates().reset_index(drop=True)
      st.success(f"Removed {duplicate_count} duplicate rows!")

  # 2. Missing Values Handling
  st.subheader("Handle Missing Values")
  cleaning_strategy = st.selectbox(
      "Choose a strategy",
      [
          "-- Select Strategy --",
          "Drop rows with missing values",
          "Fill with Constant",
          "Impute Numeric (Mean) & Categorical (Mode)",
      ],
  )

  if cleaning_strategy == "Drop rows with missing values":
    df = df.dropna()
    st.success("Dropped rows with missing values.")
  elif cleaning_strategy == "Fill with Constant":
    val = st.text_input("Enter fill value", value="0")
    if st.button("Apply Fill"):
      df = df.fillna(val)
      st.success(f"Filled missing values with {val}.")
  elif cleaning_strategy == "Impute Numeric (Mean) & Categorical (Mode)":
    if st.button("Apply Imputation"):
      for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
          df[col] = df[col].fillna(df[col].mean())
        else:
          df[col] = df[col].fillna(
              df[col].mode()[0] if not df[col].mode().empty else "Unknown"
          )
      st.success("Imputed missing values successfully!")

  # 3. Outlier Management
  st.subheader("📈 Outlier Management (IQR Method)")
  numeric_cols = df.select_dtypes(
      include=["int64", "float64", "Int64"]
  ).columns.tolist()
  if numeric_cols:
    outlier_col = st.selectbox(
        "Select numeric column to check outliers", numeric_cols
    )
    if outlier_col:
      Q1 = df[outlier_col].quantile(0.25)
      Q3 = df[outlier_col].quantile(0.75)
      IQR = Q3 - Q1
      lower_bound = Q1 - 1.5 * IQR
      upper_bound = Q3 + 1.5 * IQR
      outliers_count = df[
          (df[outlier_col] < lower_bound) | (df[outlier_col] > upper_bound)
      ].shape[0]

      st.write(
          f"Detected **{outliers_count}** potential outliers in `{outlier_col}`."
      )
      if outliers_count > 0 and st.button("Remove Outliers for this Column"):
        df = df[
            (df[outlier_col] >= lower_bound) & (df[outlier_col] <= upper_bound)
        ].reset_index(drop=True)
        st.success(f"Outliers removed from `{outlier_col}`!")

  # --- Data Visualizations Section ---
  st.header("📈 Data Visualizations")
  if numeric_cols:
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["-- Select Chart --", "Histogram / Distribution", "Correlation Heatmap"],
    )

    if viz_type == "Histogram / Distribution":
      hist_col = st.selectbox(
          "Choose a numeric column for histogram", numeric_cols, key="hist_col"
      )
      if hist_col:
        fig, ax = plt.subplots(figsize=(8, 4))
        sns.histplot(df[hist_col].dropna(), kde=True, ax=ax, color="skyblue")
        ax.set_title(f"Distribution of {hist_col}")
        st.pyplot(fig)

    elif viz_type == "Correlation Heatmap":
      if len(numeric_cols) > 1:
        fig, ax = plt.subplots(figsize=(8, 6))
        corr_matrix = df[numeric_cols].corr()
        sns.heatmap(
            corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax
        )
        ax.set_title("Correlation Matrix of Numeric Features")
        st.pyplot(fig)
      else:
        st.warning(
            "Need at least 2 numeric columns to generate a correlation heatmap."
        )

  # --- Export Cleaned File ---
  st.header("✨ Cleaned Dataset Preview & Export")
  st.dataframe(df.head(10))

  export_format = st.radio(
      "Select export format", options=["CSV (.csv)", "Excel (.xlsx)"]
  )

  if export_format == "CSV (.csv)":
    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Download Cleaned CSV",
        csv_data,
        file_name="cleaned_data.csv",
        mime="text/csv",
    )
  else:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
      df.to_excel(writer, index=False, sheet_name="Cleaned_Data")
    excel_data = output.getvalue()
    st.download_button(
        "📥 Download Cleaned Excel File",
        excel_data,
        file_name="cleaned_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
else:
  st.info("👈 Upload a file from the sidebar to get started!")