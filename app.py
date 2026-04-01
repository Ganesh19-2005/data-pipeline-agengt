import streamlit as st
from pipeline import run_pipeline

st.title("🤖 Autonomous Data Pipeline Agent")

uploaded_file = st.file_uploader("Upload your CSV")

if uploaded_file:
    if not uploaded_file.name.endswith(".csv"):
        st.error("❌ Please upload a CSV file only")
    else:
        with open("temp.csv", "wb") as f:
            f.write(uploaded_file.getbuffer())

        if st.button("Run Pipeline"):
            try:
                df, logs = run_pipeline("temp.csv")

                st.success("✅ Pipeline Completed!")

                # 📊 DATA INFO
                st.subheader("📊 Dataset Info")
                st.write(f"Total Rows: {len(df)}")
                st.write(f"Total Columns: {len(df.columns)}")

                # 📊 SHOW LIMITED DATA (FIX FOR LARGE FILES)
                st.subheader("📊 Processed Data")
                st.dataframe(df.head(200))
                st.info("Showing first 200 rows only")

                # 📥 DOWNLOAD FULL DATA
                st.download_button(
                    "📥 Download Full Data",
                    df.to_csv(index=False),
                    file_name="processed_data.csv"
                )

                # 📈 DYNAMIC VISUALIZATION (FIXED)
                st.subheader("📈 Visualization")

                numeric_cols = df.select_dtypes(include=['number']).columns

                if len(numeric_cols) > 0:
                    selected_col = st.selectbox("Select column for chart", numeric_cols)

                    st.write("Bar Chart")
                    st.bar_chart(df[selected_col].head(50))

                    st.write("Line Chart")
                    st.line_chart(df[selected_col].head(50))
                else:
                    st.warning("No numeric columns available for visualization")

                # 🤖 AGENT LOGS
                st.subheader("🤖 Agent Activity")
                for log in logs:
                    st.write(log)

            except Exception as e:
                st.error(f"❌ Error: {e}")