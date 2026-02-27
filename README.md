# 📊 AI 기반 개인 지출 분석 대시보드  
> 데이터 업로드 한 번으로 소비 패턴을 진단하고, AI가 맞춤형 재무 인사이트를 제공하는 개인 금융 분석 플랫폼
---

## 🚀 프로젝트 한 줄 소개

> 데이터 기반 개인 금융 인텔리전스 서비스

CSV/Excel 지출 데이터를 업로드하면

- 자동 데이터 전처리  
- 카테고리별 소비 분석  
- 인터랙티브 시각화 제공  
- GPT 기반 AI 인사이트 생성  
- 맞춤형 예산 가이드 제안  

까지 자동으로 수행하는 Streamlit 기반 웹 대시보드입니다.

---

## 🎯 문제 정의 (Problem Statement)

기존 가계부 서비스의 한계:

- 수기 입력 중심 → 사용자 피로도 증가  
- 단순 기록 제공 → 해석 부재  
- 개인화 부족 → 행동 변화 유도 어려움  

본 프로젝트는 다음 질문에서 출발했습니다:

> “사용자의 소비 데이터를 자동 해석하고, 실제 행동 변화를 유도할 수 없을까?”

---

## 🧠 해결 전략 (Solution Approach)
사용자 업로드
↓
데이터 클리닝 (Pandas)
↓
카테고리 분석
↓
통계 계산 (비율 / 평균 / 편차)
↓
GPT 프롬프트 엔지니어링
↓
AI 인사이트 및 예산 가이드 생성

## 🏗️ 아키텍처 구조
├─ app.py # Streamlit 엔트리 포인트 (UI 중심)
│
├─ services/
│ ├─ data_loader.py # 파일 로딩 / 전처리
│ ├─ expense_analyzer.py # 통계 계산 로직
│ ├─ ai_insights.py # OpenAI 연동
│ └─ report_generator.py # 월간 리포트 생성
│
├─ ui/
│ ├─ sidebar.py # 사이드바 UI
│ ├─ metrics.py # KPI 카드
│ └─ charts.py # Plotly 차트
│
├─ models/
│ └─ expense_data.py # 데이터 객체 관리
│
└─ utils/
└─ session.py # session_state 관리


✔ UI / 분석 로직 / AI 계층 분리  
✔ 유지보수성과 확장성을 고려한 Layered Architecture 설계  

---

## 🛠 기술 스택

| 영역 | 기술 |
|------|------|
| 데이터 처리 | Pandas |
| 시각화 | Plotly |
| 웹앱 | Streamlit |
| AI 분석 | OpenAI GPT API |
| 상태 관리 | Streamlit session_state |
| 설계 방식 | Layered Architecture |

---

## 📊 주요 기능

### 📈 소비 패턴 분석

- 월별 지출 트렌드 분석  
- 카테고리별 소비 비중 시각화    

---

### 🤖 AI 인사이트 생성

GPT API를 활용하여:

- 소비 구조 요약  
- 과소비 영역 진단  
- 절감 가능 항목 제안  
- 맞춤형 예산 가이드 생성  
- 행동 변화 유도형 피드백 제공  

--

### 📑 월간 리포트 생성

- 월간 소비 요약 자동 생성  
- 개선 제안 포함  

---










