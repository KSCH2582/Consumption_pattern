# models/expense_data.py
import pandas as pd

class ExpenseData:
    def __init__(self, df: pd.DataFrame):
        if df is None or not isinstance(df, pd.DataFrame):
            raise ValueError("Invalid DataFrame provided to ExpenseData")
        self.df = df.copy() if len(df) > 0 else df

    def filter_by_date(self, start_date, end_date):
        if 'date' not in self.df.columns:
            return ExpenseData(self.df)
        
        try:
            # Ensure date column is datetime
            if not pd.api.types.is_datetime64_any_dtype(self.df['date']):
                self.df['date'] = pd.to_datetime(self.df['date'], errors='coerce')
            
            filtered = self.df[
                (self.df['date'].dt.date >= start_date) & 
                (self.df['date'].dt.date <= end_date)
            ]
            return ExpenseData(filtered)
        except Exception as e:
            print(f"Error filtering by date: {e}")
            return ExpenseData(self.df)

    def filter_by_category(self, categories):
        if categories is None or len(categories) == 0:
            return ExpenseData(self.df)
        
        if 'category' not in self.df.columns:
            return ExpenseData(self.df)
        
        try:
            filtered = self.df[self.df['category'].isin(categories)]
            return ExpenseData(filtered)
        except Exception as e:
            print(f"Error filtering by category: {e}")
            return ExpenseData(self.df)

    # ===== 데이터 점검 도우미 메서드 =====
    def get_missing_counts(self) -> pd.Series:
        """각 컬럼별 결측값 개수를 반환"""
        return self.df.isna().sum()

    def overview(self) -> dict:
        """간단한 데이터 요약 정보를 딕셔너리로 반환.

        반환값에는 행/열 수, 컬럼 리스트, 각 컬럼별 결측값 개수가 포함된다.
        주로 UI에서 업로드 직후 데이터를 확인할 때 사용한다.
        """
        return {
            'shape': self.df.shape,
            'columns': list(self.df.columns),
            'missing': self.get_missing_counts()
        }
