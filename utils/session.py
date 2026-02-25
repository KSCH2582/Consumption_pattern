# utils/session.py

import streamlit as st


class SessionManager:

    @staticmethod
    def init():

        defaults = {

            "expense_data": None,
            "filtered_data": None,
            "last_insights": None,
            "last_report": None,
            "file_name": None

        }

        for key, value in defaults.items():

            if key not in st.session_state:

                st.session_state[key] = value



    @staticmethod
    def clear_data():

        keys = [

            "expense_data",
            "filtered_data",
            "last_insights",
            "last_report",
            "file_name"

        ]

        for key in keys:

            if key in st.session_state:

                st.session_state[key] = None



    @staticmethod
    def set_data(expense_data, file_name=None):

        st.session_state.expense_data = expense_data

        st.session_state.filtered_data = expense_data

        st.session_state.file_name = file_name

        st.session_state.last_insights = None

        st.session_state.last_report = None



    @staticmethod
    def set_filtered_data(expense_data):

        st.session_state.filtered_data = expense_data



    @staticmethod
    def save_insights(insights):

        st.session_state.last_insights = insights



    @staticmethod
    def save_report(report):

        st.session_state.last_report = report