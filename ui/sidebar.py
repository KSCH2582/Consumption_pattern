# ui/sidebar.py

import streamlit as st
from services.data_loader import DataLoader
from utils.session import SessionManager


def render_sidebar():

    SessionManager.init()

    # uploader 초기화용 key index
    if "uploader_key_index" not in st.session_state:
        st.session_state.uploader_key_index = 0

    # 이전 파일명
    if "prev_file_name" not in st.session_state:
        st.session_state.prev_file_name = None


    uploader_key = f"file_uploader_{st.session_state.uploader_key_index}"


    with st.sidebar:

        # ============================
        # 현재 데이터 상태 표시
        # ============================

        if st.session_state.file_name:

            st.success(f"현재 데이터: {st.session_state.file_name}")

            if st.button("데이터 제거"):

                SessionManager.clear_data()

                st.session_state.prev_file_name = None

                st.session_state.uploader_key_index += 1

                st.rerun()


        st.markdown("---")


        # ============================
        # 필터
        # ============================

        if st.session_state.expense_data is not None:

            st.header("필터")

            _render_filters()

            st.markdown("---")



        # ============================
        # 파일 업로드
        # ============================

        st.header("데이터 업로드")


        uploaded_file = st.file_uploader(
            "CSV 또는 Excel",
            type=["csv", "xlsx", "xls"],
            key=uploader_key
        )


        # ✅ X 눌렀을 때 감지
        if uploaded_file is None and st.session_state.prev_file_name not in (None, "sample"):

            SessionManager.clear_data()

            st.session_state.prev_file_name = None

            st.session_state.uploader_key_index += 1

            st.rerun()



        # ✅ 새 파일 업로드
        if uploaded_file is not None:

            if uploaded_file.name != st.session_state.prev_file_name:

                try:

                    data = DataLoader.load(uploaded_file)

                    SessionManager.set_data(
                        data,
                        file_name=uploaded_file.name
                    )

                    st.session_state.prev_file_name = uploaded_file.name

                    st.rerun()

                except Exception as e:

                    st.error(e)



        st.markdown("---")



        # ============================
        # 샘플 데이터
        # ============================

        st.header("샘플 데이터")


        if st.button("샘플 데이터 로드"):

            sample = DataLoader.generate_sample()

            SessionManager.set_data(
                sample,
                file_name="sample"
            )

            st.session_state.prev_file_name = "sample"

            st.session_state.uploader_key_index += 1

            st.rerun()




# ============================
# 필터
# ============================

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