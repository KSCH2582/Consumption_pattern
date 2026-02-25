# services/ai_insights.py
from openai import OpenAI
from typing import Any


class AIInsightService:
    """서비스 레이어에서 사용하는 AI 분석 도우미 클래스.

    이 클래스는 OpenAI Python 라이브러리 1.x 이후의 새로운
    인터페이스를 사용하도록 마이그레이션되어 있다.
    """

    def __init__(self, api_key: str | None = None):
        # OpenAI 클라이언트 객체를 생성. 키가 전달되면 설정.
        self.client = OpenAI(api_key=api_key) if api_key else OpenAI()

    @staticmethod
    def summarize(expense_data: Any) -> dict:
        """ExpenseData 객체로부터 통계 요약 딕셔너리를 만든다."""
        df = expense_data.df
        summary = {
            'total': df['amount'].sum(),
            'average': df['amount'].mean(),
            'max': df['amount'].max(),
            'min': df['amount'].min(),
            'count': len(df),
        }

        if 'category' in df.columns:
            cat = (
                df.groupby('category')['amount']
                  .agg(['sum', 'count'])
                  .reset_index()
            )
            cat['percentage'] = (cat['sum'] / summary['total'] * 100).round(1)
            summary['category_breakdown'] = cat.to_dict('records')

        if 'year_month' in df.columns:
            monthly = df.groupby('year_month')['amount'].sum().to_dict()
            summary['monthly'] = monthly

        return summary

    def generate(self, summary_data: dict) -> str:
        """요약 데이터를 받아 GPT에 전달할 문자열을 구성하고 호출.

        인스턴스 메서드가 되어 `self.client`를 사용할 수 있도록 변경.
        """
        category_text = ""
        if 'category_breakdown' in summary_data:
            for item in summary_data['category_breakdown']:
                category_text += f"- {item['category']}: {item['sum']:,.0f}원 ({item['percentage']}%)\n"

        prompt = f"""
당신은 개인 재무 전문가입니다. 아래 지출 데이터를 분석하고 실용적인 인사이트와 조언을 제공해주세요.

[지출 요약]
- 총 지출: {summary_data['total']:,.0f}원
- 평균 지출: {summary_data['average']:,.0f}원
- 최대 단일 지출: {summary_data['max']:,.0f}원
- 거래 건수: {summary_data['count']}건

[카테고리별 지출]
{category_text}

[분석 요청]
1. 지출 패턴에서 주목할 점 2-3가지
2. 절약할 수 있는 구체적인 영역과 예상 절약 금액
3. 다음 달 권장 예산 (카테고리별)

친근하고 이해하기 쉬운 말투로 작성해주세요. 
구체적인 수치를 포함해서 실행 가능한 조언을 해주세요.
"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "당신은 친절한 개인 재무 전문가입니다."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            # 새 API는 choices가 리스트이며, 각 choice의 message에 content가 들어있음
            return response.choices[0].message.content
        except Exception as e:
            return f"AI 분석 중 오류가 발생했습니다: {e}"
