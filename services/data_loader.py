# services/data_loader.py
import pandas as pd
from models.expense_data import ExpenseData


class DataLoader:
    @staticmethod
    def load(uploaded_file) -> ExpenseData:
        if uploaded_file.name.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file, encoding="utf-8")
            except UnicodeDecodeError:
                uploaded_file.seek(0)
                df = pd.read_csv(uploaded_file, encoding="cp949")
        else:
            df = pd.read_excel(uploaded_file)

        # date 컬럼을 datetime으로 변환 (coerce로 무효한 값은 NaT)
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'], errors='coerce')
            # 변환 불가로 NaT가 생긴 행이 있으면 사용자에게 경고
            na_count = df['date'].isna().sum()
            if na_count > 0:
                # 스트림릿 UI에서는 warning을 표시할 수 있도록
                try:
                    import streamlit as st
                    st.warning(f"날짜 변환에 실패한 {na_count}개 행이 필터에서 제외됩니다.")
                except ImportError:
                    pass
            # 연월 컬럼 추가: 월 단위 Period로 변환한 뒤
            # to_timestamp()로 첫 날(datetime) 값을 취해 저장.
            # 이렇게 하면 정렬이 자연스럽고 JSON 직렬화에도 안전하다.
            df['year_month'] = df['date'].dt.to_period('M').dt.to_timestamp()
            # NaT인 행 제거해서 이후 필터가 안전하게 동작하도록
            df = df[df['date'].notna()]

        return ExpenseData(df)

    @staticmethod
    def generate_sample() -> ExpenseData:
        """샘플 지출 데이터 생성"""
        sample_data = pd.DataFrame({
            'date': pd.date_range('2024-01-01', periods=30, freq='D'),
            'amount': [15000, 3500, 45000, 12000, 8500, 25000, 6000, 
                       32000, 4500, 18000, 55000, 7500, 21000, 9000,
                       28000, 5500, 16000, 42000, 11000, 8000, 35000,
                       4000, 22000, 13500, 48000, 6500, 19000, 38000,
                       7000, 26000],
            'category': ['식비', '교통비', '쇼핑', '식비', '카페', '문화',
                         '교통비', '식비', '카페', '쇼핑', '의료', '교통비',
                         '식비', '카페', '쇼핑', '교통비', '식비', '문화',
                         '교통비', '카페', '식비', '교통비', '쇼핑', '식비',
                         '문화', '카페', '식비', '쇼핑', '교통비', '식비'],
            'description': ['점심 식사', '지하철', '옷 구매', '저녁 식사', '커피',
                            '영화', '버스', '회식', '아메리카노', '온라인쇼핑',
                            '병원', '택시', '배달음식', '카페라떼', '생필품',
                            '지하철', '편의점', '콘서트', '버스', '디저트',
                            '장보기', '지하철', '신발', '외식', '전시회',
                            '커피', '점심', '악세서리', '택시', '저녁']
        })
        
        # 연월 컬럼 추가 (월 시작일 datetime)
        sample_data['year_month'] = sample_data['date'].dt.to_period('M').dt.to_timestamp()
        
        return ExpenseData(sample_data)
