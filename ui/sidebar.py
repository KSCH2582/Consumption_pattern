# ui/sidebar.py
import streamlit as st
from services.data_loader import DataLoader
from utils.session import SessionManager


def render_sidebar():
    with st.sidebar:
        st.header("📁 데이터 업로드")

        uploaded_file = st.file_uploader(
            "CSV 또는 Excel 파일",
            type=["csv", "xlsx", "xls"]
        )

        if uploaded_file:
            expense_data = DataLoader.load(uploaded_file)
            SessionManager.set_data(
                expense_data,
                file_name=uploaded_file.name
            )
            st.success(f"업로드 완료: {uploaded_file.name}")

        # 샘플 데이터 버튼
        st.markdown("---")
        st.markdown("### 📥 샘플 데이터")
        if st.button("🎯 샘플 데이터 로드"):
            sample_data = DataLoader.generate_sample()
            SessionManager.set_data(
                sample_data,
                file_name="sample_expense_data.csv"
            )
            st.success("✅ 샘플 데이터 로드 완료!")
            st.rerun()

        if st.session_state.expense_data:
            st.markdown("---")
            st.header("🔍 필터")

            _render_filters()


def _render_filters():
    base_data = st.session_state.expense_data

    # 날짜 필터
    if 'date' in base_data.df.columns:
        min_date = base_data.df['date'].min().date()
        max_date = base_data.df['date'].max().date()

        date_range = st.date_input(
            "기간 선택",
            (min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        filtered = base_data
        if len(date_range) == 2:
            filtered = filtered.filter_by_date(*date_range)

    # 카테고리 필터
    if 'category' in base_data.df.columns:
        categories = base_data.df['category'].unique().tolist()
        selected = st.multiselect(
            "카테고리",
            categories,
            default=categories
        )
        filtered = filtered.filter_by_category(selected)

    SessionManager.set_filtered_data(filtered)
