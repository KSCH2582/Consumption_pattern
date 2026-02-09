# app.py
import streamlit as st
from utils.session import SessionManager
from ui.sidebar import render_sidebar
from ui.metrics import render_metrics
from ui.charts import category_pie, monthly_line, category_bar
from services.expense_analyzer import ExpenseAnalyzer
from services.report_generator import ReportGenerator

st.set_page_config("💰 개인 지출 분석", layout="wide")
st.title("💰 개인 지출 분석 대시보드")

SessionManager.init()
render_sidebar()

if st.session_state.filtered_data:
    expense_data = st.session_state.filtered_data

    render_metrics(expense_data)

    analyzer = ExpenseAnalyzer(expense_data)
    category_df = analyzer.category_summary()
    monthly_df = analyzer.monthly_summary()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("카테고리별 지출")
        category_pie(category_df)
    with col2:
        st.subheader("월별 지출 추이")
        monthly_line(monthly_df)

    st.subheader("카테고리별 지출 금액")
    category_bar(category_df)

    st.markdown("---")
    st.subheader("📋 월간 리포트")

    if st.button("📄 리포트 생성"):
        report = ReportGenerator(expense_data).generate(
            st.session_state.last_insights
        )
        st.markdown(report)
