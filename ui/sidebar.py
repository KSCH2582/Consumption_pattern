# ui/sidebar.py

import streamlit as st
import pandas as pd
from services.data_loader import DataLoader
from utils.session import SessionManager

def render_sidebar():
    with st.sidebar:

        # ✅ 1) 필터 먼저 (데이터 있을 때만)
        if st.session_state.expense_data:
            st.header(" 필터")
            _render_filters()
            st.markdown("---")

        # --------------------------

        # 2) 데이터 업로드
        st.header(" 데이터 업로드")
        uploaded_file = st.file_uploader(
            "CSV 또는 Excel 파일",
            type=["csv", "xlsx", "xls"],
            key="file_uploader"
        )

        # 파일 업로드 상태 추적
        if "prev_file_name" not in st.session_state:
            st.session_state.prev_file_name = None

        # 파일 제거 시 세션 초기화
        if uploaded_file is None and st.session_state.prev_file_name is not None:
            SessionManager.clear_data()
            st.session_state.prev_file_name = None
            st.rerun()

        # 새 파일 업로드 시
        if uploaded_file:
            try:
                expense_data = DataLoader.load(uploaded_file)
                SessionManager.set_data(
                    expense_data, file_name=uploaded_file.name
                )
                st.session_state.prev_file_name = uploaded_file.name
                st.success(f"업로드 완료: {uploaded_file.name}")
                st.rerun()
            except Exception as e:
                st.error(f"파일 로드 오류: {str(e)}")

        st.markdown("---")

        # 3) 샘플 데이터 버튼
        st.markdown("### 샘플 데이터")
        if st.button(" 샘플 데이터 로드", key="btn_sample"):
            try:
                sample_data = DataLoader.generate_sample()
                SessionManager.set_data(
                    sample_data, file_name="sample_expense_data.csv"
                )
                st.session_state.prev_file_name = "sample_expense_data.csv"
                st.success("✅ 샘플 데이터 로드 완료!")
                st.rerun()
            except Exception as e:
                st.error(f"샘플 데이터 로드 오류: {str(e)}")


def _render_filters():
    base_data = st.session_state.expense_data

    if base_data is None or base_data.df is None or base_data.df.empty:
        st.warning("데이터가 없습니다.")
        return

    filtered = base_data

    # 날짜 필터
    if 'date' in base_data.df.columns:
        valid_dates = base_data.df['date'].dropna()
        if not valid_dates.empty:
            try:
                if not pd.api.types.is_datetime64_any_dtype(valid_dates):
                    valid_dates = pd.to_datetime(valid_dates, errors='coerce')
                    valid_dates = valid_dates.dropna()
                if not valid_dates.empty:
                    min_date = valid_dates.min().date()
                    max_date = valid_dates.max().date()
                    date_range = st.date_input(
                        "기간", (min_date, max_date),
                        min_value=min_date, max_value=max_date
                    )
                    if len(date_range) == 2:
                        filtered = filtered.filter_by_date(*date_range)
            except Exception as e:
                st.warning(f"날짜 필터링 오류: {str(e)}")

    # 카테고리 필터
    if 'category' in base_data.df.columns:
        try:
            categories = base_data.df['category'].dropna().unique().tolist()
            if categories:
                selected = st.multiselect(
                    "카테고리", categories, default=categories
                )
                if selected:
                    filtered = filtered.filter_by_category(selected)
        except Exception as e:
            st.warning(f"카테고리 필터링 오류: {str(e)}")

    SessionManager.set_filtered_data(filtered)