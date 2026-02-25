# ui/metrics.py
import streamlit as st
from services.expense_analyzer import ExpenseAnalyzer
from services.ai_insights import AIInsightService
from utils.session import SessionManager


def render_metrics(expense_data):
    analyzer = ExpenseAnalyzer(expense_data)
    summary = analyzer.summary()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💵 총 지출", f"{summary['total']:,.0f}원")
    col2.metric("📊 평균 지출", f"{summary['average']:,.0f}원")
    col3.metric("📈 최대 지출", f"{summary['max']:,.0f}원")
    col4.metric("🧾 거래 건수", f"{summary['count']}건")
