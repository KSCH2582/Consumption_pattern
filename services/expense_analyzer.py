# services/expense_analyzer.py
"""Expense analysis utilities."""
from typing import Any


class ExpenseAnalyzer:
    def __init__(self, expense_data: Any):
        self.df = expense_data.df

    def summary(self):
        return {
            "total": self.df['amount'].sum(),
            "average": self.df['amount'].mean(),
            "max": self.df['amount'].max(),
            "count": len(self.df)
        }

    def category_summary(self):
        return (
            self.df
            .groupby('category')['amount']
            .sum()
            .reset_index()
        )

    def monthly_summary(self):
        # year_month 컬럼은 월 시작일(datetime) 형태로 저장된다.
        # 그룹화 후 날짜순 정렬을 한 번 더 해 순서를 보장한다.
        return (
            self.df
            .groupby('year_month')['amount']
            .sum()
            .reset_index()
            .sort_values('year_month')
        )
