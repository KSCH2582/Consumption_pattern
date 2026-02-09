# models/expense_data.py
import pandas as pd

class ExpenseData:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def filter_by_date(self, start_date, end_date):
        if 'date' in self.df.columns:
            filtered = self.df[
                (self.df['date'].dt.date >= start_date) & 
                (self.df['date'].dt.date <= end_date)
            ]
            return ExpenseData(filtered)
        return ExpenseData(self.df)

    def filter_by_category(self, categories):
        if 'category' in self.df.columns:
            filtered = self.df[self.df['category'].isin(categories)]
            return ExpenseData(filtered)
        return ExpenseData(self.df)
