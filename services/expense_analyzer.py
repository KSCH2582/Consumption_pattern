# services/expense_analyzer.py
class ExpenseAnalyzer:
    def __init__(self, expense_data):
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
        return (
            self.df
            .groupby('year_month')['amount']
            .sum()
            .reset_index()
        )

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
        return (
            self.df
            .groupby('year_month')['amount']
            .sum()
            .reset_index()
        )
