# ui/charts.py
import streamlit as st
import plotly.express as px


def category_pie(df):
    fig = px.pie(
        df,
        values="amount",
        names="category",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)


def monthly_line(df):
    fig = px.line(
        df,
        x="year_month",
        y="amount",
        markers=True
    )
    st.plotly_chart(fig, use_container_width=True)


def category_bar(df):
    df = df.sort_values("amount", ascending=True)
    fig = px.bar(
        df,
        x="amount",
        y="category",
        orientation="h",
        color="amount",
        color_continuous_scale="Oranges"
    )
    st.plotly_chart(fig, use_container_width=True)
