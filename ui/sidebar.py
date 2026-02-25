# ui/sidebar.py

import streamlit as st
from services.data_loader import DataLoader
from utils.session import SessionManager


def render_sidebar():

    SessionManager.init()

    with st.sidebar:

        # =====================
        # 0. 초기화 버튼 (핵심 추가)
        # =====================

        if st.session_state.expense_data is not None:

            if st.button("데이터 적용 해제"):

                SessionManager.clear_data()

                # uploader 초기화
                st.session_state.pop("file_uploader", None)

                st.session_state.last_uploaded_file = None

                st.rerun()


        # =====================
        # 1. 필터
        # =====================

        if st.session_state.expense_data is not None:

            st.header("필터")

            _render_filters()

            st.markdown("---")


        # =====================
        # 2. 파일 업로드
        # =====================

        st.header("데이터 업로드")

        uploaded_file = st.file_uploader(
            "CSV 또는 Excel 파일",
            type=["csv", "xlsx", "xls"],
            key="file_uploader"
        )


        if "last_uploaded_file" not in st.session_state:

            st.session_state.last_uploaded_file = None


        # 새 파일 업로드

        if uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:

            try:

                expense_data = DataLoader.load(uploaded_file)

                SessionManager.set_data(
                    expense_data,
                    file_name=uploaded_file.name
                )

                st.session_state.last_uploaded_file = uploaded_file

                st.success("파일 업로드 완료")

                st.rerun()

            except Exception as e:

                st.error(e)


        st.markdown("---")


        # =====================
        # 3. 샘플 데이터
        # =====================

        st.header("샘플 데이터")

        if st.button("샘플 데이터 로드"):

            try:

                sample_data = DataLoader.generate_sample()

                SessionManager.set_data(
                    sample_data,
                    file_name="sample"
                )

                # 핵심: uploader 완전 초기화
                st.session_state.pop("file_uploader", None)

                st.session_state.last_uploaded_file = None

                st.success("샘플 데이터 적용됨")

                st.rerun()

            except Exception as e:

                st.error(e)



# =====================
# 필터
# =====================

def _render_filters():

    data = st.session_state.expense_data

    filtered = data


    if "date" in data.df.columns:

        min_date = data.df["date"].min().date()

        max_date = data.df["date"].max().date()


        date_range = st.date_input(
            "기간",
            (min_date, max_date)
        )


        if len(date_range) == 2:

            filtered = filtered.filter_by_date(
                date_range[0],
                date_range[1]
            )


    if "category" in data.df.columns:

        categories = data.df["category"].unique()


        selected = st.multiselect(
            "카테고리",
            categories,
            default=categories
        )


        if selected:

            filtered = filtered.filter_by_category(selected)


    SessionManager.set_filtered_data(filtered)