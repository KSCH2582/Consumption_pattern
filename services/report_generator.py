# services/report_generator.py
"""Generate textual monthly expenditure reports (Markdown)."""
from typing import Optional
import pandas as pd
from models.expense_data import ExpenseData


class ReportGenerator:
    def __init__(self, expense_data: ExpenseData):
        self.expense_data = expense_data
        self.df = expense_data.df

    def generate(self, insights: Optional[str] = None) -> str:
        """월간 지출 리포트 (Markdown) 생성"""
        report = []
        report.append(self._header())
        report.append(self._summary_section())
        report.append(self._category_section())
        report.append(self._top_expense_section())

        if insights:
            report.append(self._ai_insight_section(insights))

        return "\n".join(report)

    # =========================
    # 내부 섹션 메서드들
    # =========================

    def _header(self) -> str:
        return f"""# 📊 월간 지출 리포트

생성일: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}

---
"""

    def _summary_section(self) -> str:
        total = self.df['amount'].sum()
        avg = self.df['amount'].mean()
        max_val = self.df['amount'].max()
        count = len(self.df)

        return f"""## 📈 지출 요약

| 항목 | 금액 |
|------|------|
| 총 지출 | {total:,.0f}원 |
| 평균 지출 | {avg:,.0f}원 |
| 최대 지출 | {max_val:,.0f}원 |
| 거래 건수 | {count}건 |

---
"""

    def _category_section(self) -> str:
        if 'category' not in self.df.columns:
            return ""

        category_sum = (
            self.df
            .groupby('category')['amount']
            .sum()
            .sort_values(ascending=False)
        )

        total = category_sum.sum()

        lines = [
            "## 🏷️ 카테고리별 지출\n",
            "| 카테고리 | 금액 | 비율 |",
            "|----------|------|------|"
        ]

        for cat, amount in category_sum.items():
            percent = amount / total * 100
            lines.append(
                f"| {cat} | {amount:,.0f}원 | {percent:.1f}% |"
            )

        lines.append("\n---\n")
        return "\n".join(lines)

    def _top_expense_section(self) -> str:
        top5 = self.df.nlargest(5, 'amount')

        lines = [
            "## 💡 상위 5개 지출\n",
            "| 날짜 | 카테고리 | 내용 | 금액 |",
            "|------|----------|------|------|"
        ]

        for _, row in top5.iterrows():
            date_str = (
                row['date'].strftime('%Y-%m-%d')
                if 'date' in row and pd.notna(row['date'])
                else "-"
            )
            desc = row.get('description', '-')
            lines.append(
                f"| {date_str} | {row.get('category', '-')} | {desc} | {row['amount']:,.0f}원 |"
            )

        return "\n".join(lines)

    def _ai_insight_section(self, insights: str) -> str:
        return f"""
---

## 🤖 AI 인사이트

{insights}
"""
