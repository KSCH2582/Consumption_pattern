# ui/sidebar.py

import streamlit as st
from services.data_loader import DataLoader
from utils.session import SessionManager


def render_sidebar():

    with st.sidebar:

        # ✅ 1️⃣ 필터 (데이터 있을 때만)
        if st.session_state.expense_data:

            st.header("필터")
            _render_filters()
            st.markdown("---")

        # ✅ 2️⃣ 데이터 업로드
        st.header("데이터 업로드")

        uploaded_file = st.file_uploader(
            "CSV 또는 Excel 파일",
            type=["csv", "xlsx", "xls"],
            key="file_uploader"
        )

        # 업로드 상태 추적
        if "prev_file_name" not in st.session_state:
            st.session_state.prev_file_name = None

        # 파일 제거 감지
        if uploaded_file is None and st.session_state.prev_file_name is not None:

            SessionManager.clear_data()
            st.session_state.prev_file_name = None
            st.rerun()


        # 새 파일 업로드
        if uploaded_file:

            try:

                expense_data = DataLoader.load(uploaded_file)

                SessionManager.set_data(
                    expense_data,
                    file_name=uploaded_file.name
                )

                st.session_state.prev_file_name = uploaded_file.name

                st.success(f"업로드 완료: {uploaded_file.name}")

                st.rerun()

            except Exception as e:

                st.error(f"파일 로드 오류: {str(e)}")


        st.markdown("---")


        # ✅ 3️⃣ 샘플 데이터 (기존 기능 그대로 유지)
        st.markdown("샘플 데이터")

        if st.button("샘플 데이터 로드"):

            try:

                sample_data = DataLoader.generate_sample()

                SessionManager.set_data(
                    sample_data,
                    file_name="sample_expense_data.csv"
                )

                st.session_state.prev_file_name = "sample_expense_data.csv"

                st.success("샘플 데이터 로드 완료")

                st.rerun()

            except Exception as e:

                st.error(f"샘플 데이터 오류: {str(e)}")



def _render_filters():

    base_data = st.session_state.expense_data

    if base_data is None:
        return

    filtered = base_data


    # 날짜 필터
    if "date" in base_data.df.columns:

        min_date = base_data.df["date"].min().date()
        max_date = base_data.df["date"].max().date()

        date_range = st.date_input(
            "기간",
            (min_date, max_date)
        )

        if len(date_range) == 2:

            filtered = filtered.filter_by_date(
                date_range[0],
                date_range[1]
            )


    # 카테고리 필터
    if "category" in base_data.df.columns:

        categories = base_data.df["category"].unique()

        selected = st.multiselect(
            "카테고리",
            categories,
            default=categories
        )

        if selected:

            filtered = filtered.filter_by_category(selected)


    SessionManager.set_filtered_data(filtered)