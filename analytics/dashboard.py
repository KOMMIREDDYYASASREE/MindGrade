import pandas as pd
import streamlit as st

def show_analytics(results):
    df = pd.DataFrame(results)

    st.subheader("📊 Performance Analytics")

    st.bar_chart(df["Score"])
    st.line_chart(df["Semantic Similarity"])

    st.dataframe(df)
