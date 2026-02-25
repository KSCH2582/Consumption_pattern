# ui/sidebar.py

import streamlit as st
from services.data_loader import DataLoader
from utils.session import SessionManager


def render_sidebar():

    SessionManager.init()

    with st.sidebar:

        # =====================
        # 1. 필터 (데이터 있을 때만)
        # =====================

        if st.session_state.expense_data is not None:

            st.header("필터")

            _render_filters()

            st.markdown("---")


        # =====================
        # 2. 데이터 업로드
        # =====================

        st.header("데이터 업로드")

        uploaded_file = st.file_uploader(
            "CSV 또는 Excel 파일",
            type=["csv", "xlsx", "xls"],
            key="file_uploader"
        )


        # 세션 변수 생성

        if "last_uploaded_file" not in st.session_state:

            st.session_state.last_uploaded_file = None


        # =====================
        # ✅ X 버튼 눌렀을 때 (초기화 핵심 코드)
        # =====================

        if uploaded_file is None and st.session_state.last_uploaded_file is not None:

            # 데이터 초기화

            SessionManager.clear_data()

            # uploader 상태 제거 (핵심)

            st.session_state.pop("file_uploader", None)

            # 파일 상태 초기화

            st.session_state.last_uploaded_file = None

            st.rerun()


        # =====================
        # 새 파일 업로드 처리
        # =====================

        elif uploaded_file is not None and uploaded_file != st.session_state.last_uploaded_file:

            try:

                expense_data = DataLoader.load(uploaded_file)

                SessionManager.set_data(
                    expense_data,
                    file_name=uploaded_file.name
                )

                st.session_state.last_uploaded_file = uploaded_file

                st.success(f"{uploaded_file.name} 업로드 완료")

                st.rerun()

            except Exception as e:

                st.error(f"업로드 실패: {e}")


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

                # uploader 상태 제거

                st.session_state.pop("file_uploader", None)

                st.session_state.last_uploaded_file = None

                st.success("샘플 데이터 로드 완료")

                st.rerun()

            except Exception as e:

                st.error(f"샘플 로드 실패: {e}")



# =====================
# 필터 함수
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