# app.py
import streamlit as st
from utils.session import SessionManager
from ui.sidebar import render_sidebar
from ui.metrics import render_metrics
from ui.charts import category_pie, monthly_line, category_bar
from services.expense_analyzer import ExpenseAnalyzer
from services.report_generator import ReportGenerator
from services.ai_insights import AIInsightService

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

    # 4개 탭으로 구성 (간격 더 띄띄띴 띄띄)
    tab1, tab2, tab3, tab4 = st.tabs(["       Data       ", "       Charts       ", "       Report       ", "       AI       "])

    # ===== TAB 1: 데이터 미리보기 =====
    with tab1:
        st.markdown('<div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; border-left: 4px solid #1976D2;"><h4 style="margin: 0; color: #0D47A1;">📄 데이터 미리보기</h4></div>', unsafe_allow_html=True)
        st.markdown("")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("행", expense_data.df.shape[0])
        with col2:
            st.metric("열", expense_data.df.shape[1])
        with col3:
            missing_total = expense_data.get_missing_counts().sum()
            st.metric("결측", missing_total)
        with col4:
            st.metric("메모리", f"{expense_data.df.memory_usage().sum() / 1024:.1f}KB")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**결측값 개수**")
            missing = expense_data.get_missing_counts()
            st.dataframe(missing.to_frame(name="missing"), height=200, use_container_width=True)
        with col2:
            st.markdown("**데이터 미리**")
            st.dataframe(expense_data.df.head(10), height=200, use_container_width=True)

    # ===== TAB 2: 차트보기 =====
    with tab2:
        st.markdown('<div style="background-color: #E8F5E9; padding: 15px; border-radius: 8px; border-left: 4px solid #388E3C;"><h4 style="margin: 0; color: #1B5E20;">📊 차트 보기</h4></div>', unsafe_allow_html=True)
        st.markdown("")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**카테고리별**")
            category_pie(category_df)
        with col2:
            st.markdown("**월별 추이**")
            monthly_line(monthly_df)

        st.markdown("**카테고리별 금액**")
        category_bar(category_df)

    # ===== TAB 3: 월간 리포트 =====
    with tab3:
        st.markdown('<div style="background-color: #FFF3E0; padding: 15px; border-radius: 8px; border-left: 4px solid #F57C00;"><h4 style="margin: 0; color: #E65100;">📋 월간 리포트</h4></div>', unsafe_allow_html=True)
        st.markdown("")
        
        if st.button("📄 리포트 생성", key="btn_report", use_container_width=True):
            report = ReportGenerator(expense_data).generate(insights=None)
            SessionManager.save_report(report)
        
        if st.session_state.get('last_report'):
            st.markdown(st.session_state.last_report)

    # ===== TAB 4: AI 분석 =====
    with tab4:
        st.markdown('<div style="background-color: #F3E5F5; padding: 15px; border-radius: 8px; border-left: 4px solid #7B1FA2;"><h4 style="margin: 0; color: #4A148C;">🤖 AI 분석</h4></div>', unsafe_allow_html=True)
        st.markdown("")
        st.caption("⚠️ AI 인사이트가 없으면 기본 리포트만 생성")
        
        if st.button("🔍 AI 분석 시작", type="primary", key="btn_ai", use_container_width=True):
            with st.spinner("AI 분석 중..."):
                api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
                service = AIInsightService(api_key=api_key)
                summary_data = AIInsightService.summarize(expense_data)
                insights = service.generate(summary_data)
                SessionManager.save_insights(insights)
        
        if st.session_state.get('last_insights'):
            st.markdown(st.session_state.last_insights)
