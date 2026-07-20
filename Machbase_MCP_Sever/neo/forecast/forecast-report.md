# 시계열 예측 HTML 리포트 템플릿

**`forecast_table` 도구 전용 템플릿입니다.** `save_html_report`(일반 리포트)와는 **별개 폴더**로 관리합니다 —
`neo/report/`에 두면 리포트 스캐너가 자동 등록해 LLM 노출·질의 라우팅 대상이 되고,
save_html_report가 이 템플릿을 고르면 `{FORECAST_DATA_JSON}`을 채우지 못해 **빈 페이지**가 저장됩니다.
여기(`neo/forecast/`)에 있으면 리포트 스캐너가 **애초에 보지 못합니다**.

**태그 드롭다운 × 모델 드롭다운**으로 태그별·모델별 예측 결과를 전부 열람할 수 있습니다.
차트는 외부 라이브러리 없이 canvas 2D로 직접 그립니다(오프라인 안전, CDN 불가 환경 대응).

## 디자인
**Neo Web UI(neo-web) 디자인 시스템** 기반 — **기본은 다크 모드**(2026-07-15 사용자 재확정 — 라이트 기본을 하루 써보고 되돌림), 우상단 토글로 **다크 모드** 전환(선택은 localStorage 저장). `src/design-system/tokens/_colors.scss` 기준. 구현: CSS `:root`=다크 토큰 + `.theme-light` 오버라이드 구조는 그대로 두고, 기본은 `:root` 다크 토큰 그대로, 저장 선택이 light일 때만 head 스크립트가 `theme-light` 부착(동기 실행 — 플래시 없음).
- 배경 `#1e1e1e`(page·차트 섹션) / `#252525`(panel) / `#2c2c2c`(elevated) / `#2d2d2d`(dropdown)
- 텍스트 `#f1f1f1` → `#c4c4c4` → `#a3a3a3` → `#727272`, 테두리 `rgba(255,255,255,0.13)`
- Primary `#005fb8`(hover `#0075e2`), success `#71e071`, error `#ff5353`, warning `#ff9800`
- 폰트 Pretendard(UI) / D2Coding(코드·숫자), radius 4·8px
- 차트 색은 Neo Tag Analyzer 팔레트: 실측 `#4199ff`, 예측 `#fdb532`(95% 구간은 동일 앰버 세로 그라디언트 + 점선 경계), 백테스트 `#71e071`
- 상단 = 레터헤드(eyebrow·제목·메타) + 4칸 스펙 패널(학습 기간·태그·예측 구간·모델 수는 데이터에서 계산), y축은 라운드 눈금, 위험 태그(MAPE≥40%)엔 상태 점

## 커스터마이징
`neo/forecast/custom/` 폴더에 같은 형식의 `.md`(```html 블록)를 넣으면 **그게 우선 사용**됩니다.
아래 `{PLACEHOLDER}`들은 도구가 채우니 이름을 바꾸지 마세요.

## 변수 설명
| 변수 | 설명 | 채우는 주체 |
|------|------|------------|
| {TABLE} | 테이블명 | 예측 엔진 |
| {LOGO_IMG} | 헤더 로고 `<img>` (machbase-logo-header.**b64** 를 읽어 data URI로 인라인 — jsh는 PNG 바이너리를 못 읽는다) | 예측 엔진 |
| {GENERATED_DATE} | 리포트 생성 일시 | 자동 삽입 |
| {TAG_COUNT} | 태그 수 | 예측 엔진 |
| {DATA_UNIT} | 데이터 간격(예: "일 단위 데이터") | 예측 엔진 |
| {TIME_RANGE} | 학습 데이터 기간 | 예측 엔진 |
| {ROLLUP_LABEL} | 단위 한글(일/시간/분…) | 예측 엔진 |
| {HORIZON_LABEL} | 예측 구간(예: 181일) | 예측 엔진 |
| {TAG_STATS_ROWS} | 태그별 요약 `<tr>` 행 | 예측 엔진 |
| {FORECAST_DATA_JSON} | 태그×모델 전체 예측 데이터 | 예측 엔진 |
| {ANALYSIS} | 분석문 | 예측 엔진(결정론 생성) |

---

## 템플릿

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TABLE} 예측 리포트</title>
<!-- 기본 = 다크(:root 토큰 그대로). 저장된 선택이 라이트일 때만 theme-light 부착(head 동기 실행 — 플래시 없음). -->
<script>try{if(localStorage.getItem('neoReportTheme2')==='light')document.documentElement.classList.add('theme-light');}catch(e){}</script>
<style>
  /* Neo Web UI design tokens (src/design-system/tokens/_colors.scss) */
  :root {
    --bg-primary: #1e1e1e;
    --bg-panel: #252525;
    --bg-elevated: #2c2c2c;
    --bg-dropdown: #2d2d2d;
    --bg-hover: rgba(255, 255, 255, 0.08);
    --bg-input: rgba(255, 255, 255, 0.13);

    --text-primary: #f1f1f1;
    --text-secondary: #c4c4c4;
    --text-tertiary: #a3a3a3;
    --text-muted: #727272;

    --border-default: rgba(255, 255, 255, 0.13);
    --border-medium: #626263;
    --border-faint: rgba(255, 255, 255, 0.06);

    --primary: #005fb8;
    --primary-hover: #0075e2;
    --success: #71e071;
    --error: #ff5353;
    --warning: #ff9800;
    --event: #ffdc72;

    --series-actual: #4199ff;
    --series-forecast: #fdb532;
    --series-backtest: #71e071;

    --radius-sm: 4px;
    --radius-md: 8px;
    --shadow-sm: 0 2px 2px rgba(0, 0, 0, 0.25);
  }

  /* 라이트 모드 — DS 라이트 팔레트(잉크 #262831, 표면 #fff/#f5f6f8). 액센트·시맨틱 색은 두 모드 공통. */
  .theme-light {
    --bg-primary: #e9ebef;
    --bg-panel: #ffffff;
    --bg-elevated: #f5f6f8;
    --bg-dropdown: #ffffff;
    --bg-hover: rgba(0, 0, 0, 0.045);
    --bg-input: rgba(0, 0, 0, 0.05);
    --text-primary: #262831;
    --text-secondary: #40434e;
    --text-tertiary: #5f636f;
    --text-muted: #8a8d99;
    --border-default: rgba(0, 0, 0, 0.12);
    --border-medium: #b9bcc5;
    --border-faint: rgba(0, 0, 0, 0.08);
    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.08);
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Pretendard', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Malgun Gothic', sans-serif;
    background: var(--bg-primary);
    color: var(--text-primary);
    line-height: 1.65;
    font-size: 15px;
  }
  .page { max-width: 1320px; margin: 0 auto; padding: 40px 28px 56px; }

  /* Header — 레터헤드: 왼쪽 제목·메타 / 오른쪽 로고 */
  .report-header {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 24px;
    padding: 4px 0 26px; border-bottom: 1px solid var(--border-default); margin-bottom: 28px;
  }
  /* 로고: 제목(30px)과 균형 맞춰 42px. 1320px 폭에서 30px는 너무 작아 보였다. */
  .report-header .logo { height: 42px; width: auto; flex-shrink: 0; opacity: 1; margin-top: 2px; margin-right: 2px; }
  .theme-light .report-header .logo { filter: brightness(0.18); }
  .hd-right { display: flex; flex-direction: column; align-items: flex-end; gap: 16px; flex-shrink: 0; }
  .theme-btn {
    display: inline-flex; align-items: center; justify-content: center; width: 34px; height: 34px; padding: 0;
    color: var(--text-secondary);
    background: var(--bg-input); border: 1px solid var(--border-default); border-radius: var(--radius-sm);
    cursor: pointer; transition: background .15s ease, border-color .15s ease, color .15s ease;
  }
  .theme-btn:hover { border-color: var(--border-medium); color: var(--text-primary); }
  .theme-btn:active { transform: scale(.96); }
  .theme-btn svg { width: 18px; height: 18px; display: block; }
  .theme-btn .ic-sun { display: none; }
  .theme-light .theme-btn .ic-sun { display: block; }
  .theme-light .theme-btn .ic-moon { display: none; }
  .eyebrow { font-size: 11px; font-weight: 700; letter-spacing: 1.4px; line-height: 1; text-transform: uppercase; color: var(--primary-hover); margin-bottom: 10px; }
  .report-header h1 { font-size: 30px; font-weight: 700; line-height: 1.2; color: var(--text-primary); letter-spacing: -0.3px; }
  .report-header h1 .hl { color: var(--primary-hover); }
  .meta-row { display: flex; flex-wrap: wrap; gap: 10px 26px; margin-top: 16px; font-size: 13px; }
  .meta-row .meta { display: flex; align-items: baseline; gap: 8px; }
  .meta-row .meta-k { font-size: 10px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: var(--text-muted); }
  .meta-row .meta-v { color: var(--text-secondary); }
  .meta-row .mono { font-family: 'D2Coding', 'Consolas', monospace; }

  /* KPI */
  /* 스펙 패널 — 카드 4장 나열 대신 하나의 패널을 세로 구분선으로 나눈다(모델 요약 stat 행과 동일 패턴). */
  .spec-panel { display: flex; flex-wrap: wrap; background: var(--bg-panel); border: 1px solid var(--border-default); border-radius: var(--radius-md); overflow: hidden; margin-bottom: 28px; }
  .spec-col { flex: 1 1 0; min-width: 180px; padding: 18px 22px; border-right: 1px solid var(--border-default); display: flex; flex-direction: column; }
  .spec-col:last-child { border-right: none; }
  .spec-k { font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: var(--text-muted); }
  .spec-v { margin-top: 7px; font-size: 24px; font-weight: 700; color: var(--text-primary); font-variant-numeric: tabular-nums; line-height: 1.1; }
  .spec-v .unit { font-size: 14px; font-weight: 600; color: var(--text-tertiary); margin-left: 2px; }
  .spec-meta { margin-top: 14px; font-size: 12px; color: var(--text-tertiary); font-family: 'D2Coding', 'Consolas', monospace; }
  .spec-meta .m { color: var(--text-secondary); }

  /* Section */
  .section { background: var(--bg-panel); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 24px 26px; margin-bottom: 24px; }
  /* 핵심 섹션(차트)은 에디터 톤(#1e1e1e)으로 한 단계 눌러 시선을 잡는다 — 부연 섹션과 무게를 구분. */
  .section.section-chart { background: var(--bg-primary); }
  /* 위험 데이터 행: 앞에 상태 점 하나. 채우지 않고 점 + MAPE 강조만으로 "믿지 마세요"를 전달. */
  .dot { display: inline-block; width: 7px; height: 7px; border-radius: 50%; background: var(--warning); margin-right: 8px; vertical-align: middle; }
  .section-title { display: flex; align-items: center; gap: 9px; font-size: 17px; font-weight: 600; color: var(--text-primary); margin-bottom: 18px; }
  .section-title .bar { width: 3px; height: 16px; border-radius: 2px; background: var(--primary); }
  .section-title .aside { margin-left: auto; font-size: 13px; font-weight: 400; color: var(--text-muted); }
  /* 차트가 인터랙티브라는 신호 — 제목 옆 작은 칩(DS: 필 금지 → 4px 네모). */
  .chart-badge {
    display: inline-flex; align-items: center; gap: 6px; padding: 3px 8px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.2px;
    color: var(--primary-hover); background: rgba(0, 108, 210, 0.12);
    border: 1px solid rgba(0, 108, 210, 0.28); border-radius: var(--radius-sm);
  }
  .chart-badge svg { width: 13px; height: 13px; }
  /* Selects */
  .sel-group { display: flex; align-items: center; gap: 9px; margin-left: auto; }
  .sel-group label { font-size: 13px; color: var(--text-tertiary); }
  select {
    background: var(--bg-dropdown); color: var(--text-primary);
    border: 1px solid var(--border-default); border-radius: var(--radius-sm);
    padding: 7px 12px; font-size: 14px; font-family: inherit; cursor: pointer; min-width: 150px;
  }
  select:hover { border-color: var(--border-medium); }
  select:focus { outline: none; border-color: var(--primary-hover); }

  /* Table */
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  thead th {
    text-align: left; font-weight: 600; color: var(--text-tertiary); font-size: 13px;
    padding: 12px 14px; border-bottom: 1px solid var(--border-default); white-space: nowrap;
  }
  tbody td { padding: 12px 14px; border-bottom: 1px solid var(--border-faint); color: var(--text-secondary); }
  tbody tr:last-child td { border-bottom: none; }
  tbody tr.clickable { cursor: pointer; }
  tbody tr.clickable:hover { background: var(--bg-hover); }
  tbody tr.is-sel td { background: rgba(0, 95, 184, 0.16); color: var(--text-primary); font-weight: 600; }
  tbody tr.is-out td { color: var(--text-muted); }
  .num { text-align: right; font-variant-numeric: tabular-nums; font-family: 'D2Coding', 'Consolas', 'Menlo', monospace; }
  code {
    font-family: 'D2Coding', 'Consolas', 'Menlo', monospace; font-size: 13px;
    background: var(--bg-input); color: var(--text-primary); padding: 2px 6px; border-radius: 3px;
  }
  .badge { display: inline-block; padding: 2px 8px; border-radius: 3px; font-size: 12px; font-weight: 600; }
  .badge-sel { background: rgba(113, 224, 113, 0.16); color: var(--success); }
  .badge-out { background: rgba(255, 83, 83, 0.14); color: var(--error); }
  .warn { color: var(--warning); font-weight: 600; }

  /* Chart */
  .chart-wrap { position: relative; }
  canvas { width: 100%; display: block; background: var(--bg-elevated); border: 1px solid var(--border-default); border-radius: var(--radius-sm); }
  .tooltip {
    position: absolute; pointer-events: none; display: none; z-index: 10;
    background: var(--bg-dropdown); color: var(--text-primary);
    border: 1px solid var(--border-medium); border-radius: var(--radius-sm);
    padding: 7px 10px; font-size: 12px; line-height: 1.6; white-space: nowrap; box-shadow: var(--shadow-sm);
  }
  .tooltip.fixed { position: fixed; }        /* 커서 추적형(표 위험 행) — 기준 요소 불필요 */
  tr[data-tip] { cursor: help; }             /* 위험 행: 커서 모양으로 "설명 있음"을 알림 */
  .legend { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; margin-top: 14px; font-size: 13px; color: var(--text-tertiary); }
  .legend span { display: flex; align-items: center; gap: 7px; }
  .swatch { width: 20px; height: 2px; border-radius: 1px; }
  /* 범례 스와치도 차트와 동일하게: 옅은 채움 + 위아래 경계선(차트에서 실제로 보이는 모양과 맞춘다). */
  .swatch-band {
    width: 20px; height: 11px; border-radius: 2px;
    background: rgba(253, 181, 50, 0.13);
    border-top: 1px dashed rgba(253, 181, 50, 0.55);
    border-bottom: 1px dashed rgba(253, 181, 50, 0.55);
  }
  .nav-hint { margin-left: auto; color: var(--text-muted); font-size: 12px; }
  .nav-hint b { color: var(--text-tertiary); font-weight: 600; }

  /* Notes — 밑줄 각주(밴드 캐프션과 동일 톤). 박스 대신 흐린 한 줄로 통일. */
  .note {
    margin-top: 16px; font-size: 12px; line-height: 1.7; color: var(--text-muted);
  }
  .note strong { color: var(--text-tertiary); font-weight: 600; }
  .note code { font-size: 12px; }

  /* 밴드(95% 구간) 설명 — 박스가 아니라 차트 아래 한 줄 각주로. */
  .band-help {
    display: flex; align-items: baseline; gap: 8px; flex-wrap: wrap;
    margin-top: 12px; font-size: 12px; line-height: 1.6; color: var(--text-muted);
  }
  .band-help .swatch-band { flex-shrink: 0; align-self: center; }
  .band-help b { color: var(--text-tertiary); font-weight: 600; }

  /* 선택 모델 요약 — 한 줄에 다 욱여넣었더니 읽기 힘들었다 → 헤더 / 수치 3칸 / 경고 로 층을 나눈다. */
  .model-note { margin-top: 16px; background: var(--bg-elevated); border: 1px solid var(--border-default); border-radius: var(--radius-md); overflow: hidden; }
  .mn-head {
    display: flex; align-items: center; flex-wrap: wrap; gap: 8px;
    padding: 11px 16px; background: transparent; border-bottom: 1px solid var(--border-default);
    font-size: 14px; color: var(--text-primary);
  }
  .mn-head .mn-tag { font-weight: 700; }
  .mn-head .mn-sub { font-size: 12px; color: var(--text-muted); }
  .mn-stats { display: flex; flex-wrap: wrap; }
  .mn-stat { flex: 1 1 0; min-width: 150px; padding: 12px 16px; border-right: 1px solid var(--border-default); }
  .mn-stat:last-child { border-right: none; }
  .mn-label { font-size: 11px; color: var(--text-tertiary); text-transform: uppercase; letter-spacing: 0.4px; }
  .mn-value {
    margin-top: 3px; font-size: 18px; font-weight: 700; color: var(--text-primary);
    font-family: 'D2Coding', 'Consolas', monospace; font-variant-numeric: tabular-nums;
  }
  .mn-value.sm { font-size: 15px; }
  .mn-alert {
    display: flex; gap: 8px; padding: 11px 16px;
    background: rgba(255, 152, 0, 0.08); border-top: 1px solid var(--border-default);
    font-size: 13px; line-height: 1.7; color: var(--text-tertiary);
  }
  .mn-alert b { color: var(--warning); font-weight: 700; }
  /* 지표 설명 — 색을 셋(주황·흰색·회색) 섞었더니 뭘 강조하는지 사라졌다.
     → 용어는 칩으로 분리하고, 본문은 한 톤으로. 강조는 <b> 하나만(색 없이 밝기만). */
  .metric-help { margin-top: 18px; padding-top: 16px; border-top: 1px solid var(--border-faint); }
  .mh-row { display: flex; align-items: baseline; gap: 12px; margin-bottom: 8px; }
  .mh-row:last-child { margin-bottom: 0; }
  .mh-term {
    flex: 0 0 62px; text-align: center;
    font-family: 'D2Coding', 'Consolas', monospace; font-size: 12px; font-weight: 700;
    color: var(--text-tertiary); background: var(--bg-elevated);
    border: 1px solid var(--border-default); border-radius: 3px; padding: 2px 0;
  }
  .mh-desc { font-size: 13px; line-height: 1.7; color: var(--text-tertiary); }
  .mh-desc b { color: var(--text-secondary); font-weight: 600; }

  /* Analysis */
  .analysis-content { color: var(--text-secondary); font-size: 15px; line-height: 1.95; }
  .analysis-content h4 {
    margin: 24px 0 10px; font-size: 15px; font-weight: 700; color: var(--text-primary); letter-spacing: -0.1px;
  }
  .analysis-content h4:first-child { margin-top: 0; }
  /* 리드: 소제목 아래 한 줄 요지 — 안 읽어도 핵심이 잡히도록. 색 없이 굵기·크기로만 구분. */
  .analysis-content .lead { font-size: 16px; font-weight: 600; line-height: 1.6; color: var(--text-primary); margin: -2px 0 12px; }
  .analysis-content p { margin-bottom: 12px; }
  .analysis-content strong { color: var(--text-primary); font-weight: 600; }
  .analysis-content em { font-style: normal; color: var(--text-tertiary); }
  .analysis-content ul { margin: 10px 0 16px 22px; }
  .analysis-content li { margin-bottom: 9px; }
  .analysis-content li::marker { color: var(--primary-hover); }
  /* 분석 = 라벨 + 한 줄 행. 산문 문단을 이어 붙이면 눈이 미끄러진다 — 항목별로 끊어 스캔 가능하게. */
  .analysis-content .a-row { display: flex; gap: 16px; padding: 11px 0; border-bottom: 1px solid var(--border-faint); line-height: 1.8; }
  .analysis-content .a-row:first-child { padding-top: 0; }
  .analysis-content .a-row:last-child { border-bottom: none; padding-bottom: 0; }
  .analysis-content .a-k { flex: 0 0 58px; font-size: 12px; font-weight: 700; color: var(--text-muted); padding-top: 4px; letter-spacing: 0.3px; }
  .analysis-content .a-v { flex: 1; min-width: 0; }
  /* 한계 행 강조 — 빨강(=오류 의미론)은 과함, 틴트+보더 콜아웃도 "너무 튐"(라이브 2회 확정).
     미니멀 헤어라인 구성에서 색 박스 하나는 경고 배너처럼 소리 지른다 → **라벨 색만 앰버**(회색 라벨들 사이라 이것으로 충분). */
  .analysis-content .a-row.a-caution .a-k { color: var(--warning); }

  .report-footer { text-align: center; padding: 26px 0 0; color: var(--text-muted); font-size: 12px; border-top: 1px solid var(--border-default); }

  @media (max-width: 768px) {
    .spec-col { flex-basis: 45%; }
    .page { padding: 16px; }
    .sel-group { flex-wrap: wrap; }
    /* 좀은 화면에서 6열 표가 깨지지 않도록 가로 스크롤 허용. */
    .section { overflow-x: auto; }
    table { min-width: 560px; }
  }
</style>
</head>
<body>
<div class="page">

  <div class="report-header">
    <div class="hd-left">
      <div class="eyebrow">Forecast Report &middot; 시계열 예측</div>
      <h1><span class="hl">{TABLE}</span> 시계열 예측 리포트</h1>
      <div class="meta-row">
        <span class="meta"><span class="meta-k">생성</span><span class="meta-v mono">{GENERATED_DATE}</span></span>
        <span class="meta"><span class="meta-k">소스</span><span class="meta-v"><span class="mono">{TABLE}</span> &middot; TAG table</span></span>
      </div>
    </div>
    <div class="hd-right">
    <img class="logo" src="data:image/png;base64,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" alt="Machbase">
      <button id="themeBtn" class="theme-btn" type="button" aria-label="테마 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"></path></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg></button>
    </div>
  </div>

  <div class="spec-panel">
    <div class="spec-col">
      <div class="spec-k">학습 기간</div>
      <div class="spec-v" id="specSpan">-</div>
      <div class="spec-meta">{TIME_RANGE}</div>
    </div>
    <div class="spec-col">
      <div class="spec-k">예측 태그</div>
      <div class="spec-v">{TAG_COUNT}<span class="unit">개</span></div>
      <div class="spec-meta" id="specTags">-</div>
    </div>
    <div class="spec-col">
      <div class="spec-k">예측 구간</div>
      <div class="spec-v">{HORIZON_LABEL}</div>
      <div class="spec-meta" id="specFcRange">-</div>
    </div>
    <div class="spec-col">
      <div class="spec-k">비교 모델</div>
      <div class="spec-v" id="kpiModels">-</div>
      <div class="spec-meta">MAPE 최저 모델 자동 선택</div>
    </div>
  </div>

  <!-- 태그별 요약 -->
  <div class="section">
    <div class="section-title"><span class="bar"></span> 태그별 예측 요약</div>
    <table>
      <thead><tr><th>태그</th><th>선택 모델</th><th class="num">추세 /{ROLLUP_LABEL}</th><th class="num">최근값</th><th class="num">R&sup2;</th><th class="num">MAPE</th></tr></thead>
      <tbody>{TAG_STATS_ROWS}</tbody>
    </table>
    <div class="metric-help">
      <div class="mh-row">
        <span class="mh-term">R&sup2;</span>
        <span class="mh-desc">모델이 <b>과거</b>를 얼마나 잘 설명하는지. 1에 가까울수록 잘 맞습니다. 미래 정확도는 아닙니다. 평활&middot;자기회귀 계열 모델(ses/holt/ar)은 R&sup2;를 계산하지 않아 &mdash;로 표시됩니다.</span>
      </div>
      <div class="mh-row">
        <span class="mh-term">MAPE</span>
        <span class="mh-desc">과거 뒷부분을 가리고 <b>실제로 맞혀본 오차율</b>. 낮을수록 정확하며, 예측 정확도는 이 값으로 판단합니다.</span>
      </div>
    </div>
  </div>

  <!-- 분석 — 결론 해석은 표 바로 아래(숫자 → 해석 → 탐색(차트·모델비교) 순서. 맨 끝에 두면 안 읽힌다) -->
  <div class="section">
    <div class="section-title"><span class="bar"></span> 분석</div>
    <div class="analysis-content">{ANALYSIS}</div>
  </div>

  <!-- 예측 차트: 태그 × 모델 -->
  <div class="section section-chart">
    <div class="section-title">
      <span class="bar"></span> 예측 차트
      <span class="chart-badge" title="휠로 확대, 드래그로 이동"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 9 2 12 5 15"></polyline><polyline points="9 5 12 2 15 5"></polyline><polyline points="15 19 12 22 9 19"></polyline><polyline points="19 9 22 12 19 15"></polyline><line x1="2" y1="12" x2="22" y2="12"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>확대·이동</span>
      <div class="sel-group">
        <label for="tagSel">태그</label>
        <select id="tagSel"></select>
        <label for="modelSel">모델</label>
        <select id="modelSel"></select>
      </div>
    </div>
    <div class="chart-wrap">
      <canvas id="fcChart" height="460"></canvas>
      <div class="tooltip" id="fcTip"></div>
    </div>
    <div class="legend">
      <span><i class="swatch" style="background:#4199ff"></i> 실측</span>
      <span><i class="swatch" style="background:#fdb532"></i> 예측</span>
      <span><i class="swatch-band"></i> 95% 구간</span>
      <span><i class="swatch" style="background:#71e071"></i> 백테스트(검증)</span>
      <span class="nav-hint"><b>휠</b> 확대·축소 &middot; <b>드래그</b> 좌우 이동 &middot; <b>더블클릭</b> 되돌리기</span>
    </div>

    <div class="band-help">
      <i class="swatch-band"></i>
      <span><b>95% 구간</b> — 실제 값이 들어올 것으로 보이는 범위. 띠가 넓을수록 불확실하니 위·아래 끝을 함께 보세요.</span>
    </div>

    <div class="model-note" id="modelNote"></div>
  </div>

  <!-- 모델 비교 -->
  <div class="section">
    <div class="section-title">
      <span class="bar"></span> 모델 비교
      <div class="sel-group">
        <label for="lbTagSel">태그 기준</label>
        <select id="lbTagSel"></select>
      </div>
    </div>
    <table>
      <thead><tr><th style="width:56px;">순위</th><th>모델</th><th class="num">검증 MAPE</th><th class="num" id="lbFcHead">예측값</th><th>설명</th></tr></thead>
      <tbody id="lbBody"></tbody>
    </table>
    <div class="note">
      <span><strong>제외</strong> = 예측값이 과거 변동폭을 크게 벗어난 모델. 검증 MAPE가 낮아도 {HORIZON_LABEL} 끝까지 뻗었을 때 폭주하면 제외되며, 자동 선택에서만 빠질 뿐 드롭다운·행 클릭으로 확인할 수 있습니다.</span>
    </div>
  </div>

  <div class="report-footer">Machbase Neo 데이터 기반으로 생성 되었습니다.</div>
</div>

<script>
(function () {
  var D = {FORECAST_DATA_JSON};
  var tags = D.tags || [];
  if (!tags.length) return;
  var curTag = tags[0], curModel = null;

  // Neo design tokens (차트는 canvas라 CSS 변수를 못 쓴다 → 여기 상수로 둔다. _colors.scss와 동일 값 유지할 것.)
  var C = {
    grid: 'rgba(255,255,255,0.07)',
    axis: '#a3a3a3',
    actual: '#4199ff',
    forecast: '#fdb532',
    // 브랜드 앨버(#fdb532) 기반. 채움은 최소한, 밝은 경계선으로 범위를 읽힌다.
    band: 'rgba(253,181,50,0.13)',
    bandEdge: 'rgba(253,181,50,0.45)',
    backtest: '#71e071',
    divider: '#626263',
  };

  // 차트 보기 상태(시간축 ms). 기존 리포트와 같은 조작: 휠=확대/축소, 드래그=좌우 이동, 더블클릭=되돌리기.
  // (드롭다운으로 구간을 고르게 했더니 조작감이 다른 리포트와 달라 어색했다 → 캔버스 직접 조작으로 통일.)
  var view = null;          // {x0, x1}
  var viewFull = null;      // 전체 범위
  var DEFAULT_MULT = 2;     // 처음 보기 = 예측 구간 × 2 만큼의 과거 + 예측(전체를 다 그리면 예측 근방이 눌린다)

  var tagSel = document.getElementById('tagSel');
  var modelSel = document.getElementById('modelSel');
  var lbBody = document.getElementById('lbBody');
  var lbTagSel = document.getElementById('lbTagSel');
  var noteEl = document.getElementById('modelNote');
  var cv = document.getElementById('fcChart');
  var tip = document.getElementById('fcTip');

  var maxModels = 0;
  tags.forEach(function (t) { var k = Object.keys(D.perTag[t].models).length; if (k > maxModels) maxModels = k; });
  document.getElementById('kpiModels').innerHTML = maxModels + '<span class="unit">개</span>';

  // 스펙 패널의 나머지 값은 데이터에서 직접 계산한다(플레이스홀더 불필요 — 어떤 테이블/태그에도 동작).
  (function () {
    var t0 = D.perTag[tags[0]];
    var av = t0 && t0.actual;
    if (av && av.length > 1) {
      var days = (av[av.length - 1][0] - av[0][0]) / 86400000;
      var span = days >= 365 ? (days / 365).toFixed(1) + '<span class="unit">년</span>'
        : (days >= 60 ? Math.round(days / 30) + '<span class="unit">개월</span>'
        : Math.round(days) + '<span class="unit">일</span>');
      var es = document.getElementById('specSpan'); if (es) es.innerHTML = span;
    }
    var st = document.getElementById('specTags'); if (st) st.textContent = tags.join('·');
    var au = t0 && t0.models[t0.auto], fc = au && au.fc;
    if (fc && fc.length) {
      var fr = document.getElementById('specFcRange');
      if (fr) fr.textContent = fmtDate(fc[0][0]) + ' ~ ' + fmtDate(fc[fc.length - 1][0]);
    }
  })();

  function fmt(v) {
    if (!isFinite(v)) return '-';
    var a = Math.abs(v);
    if (a >= 100000) return (v / 1000).toFixed(0) + 'K';
    if (a >= 1000) return v.toFixed(0);
    if (a >= 1) return v.toFixed(2);
    if (a >= 0.01) return v.toFixed(4);
    return v === 0 ? '0' : v.toExponential(1);
  }
  function fmtDate(ms) {
    var d = new Date(ms);
    function p(n) { return (n < 10 ? '0' : '') + n; }
    return d.getFullYear() + '-' + p(d.getMonth() + 1) + '-' + p(d.getDate());
  }

  // 태그 셀렉터는 **두 곳**(차트 위, 모델 비교 위)에 있고 같은 상태를 공유한다 — 어느 쪽을 바꿔도 둘 다 따라온다.
  [tagSel, lbTagSel].forEach(function (sel) {
    tags.forEach(function (t) {
      var o = document.createElement('option'); o.value = t; o.textContent = t; sel.appendChild(o);
    });
    sel.onchange = function () { setTag(this.value); };
  });

  function setTag(t) {
    curTag = t;
    tagSel.value = t; lbTagSel.value = t;
    curModel = D.perTag[curTag].auto;
    syncModelSel();
    resetView();
    render();
  }

  function syncModelSel() {
    var T = D.perTag[curTag], ms = T.models;
    modelSel.innerHTML = '';
    T.order.forEach(function (m) {                       // 리더보드 순서(성적순, 실격 뒤) == 드롭다운 순서
      var e = ms[m], o = document.createElement('option');
      o.value = m;
      // 체크·경고 아이콘 없이 텍스트로만 — 선택 상태는 표의 하이라이트와 배지가 이미 말해준다(아이콘은 중복).
      o.textContent = m + '  (MAPE ' + (e.mape >= 0 ? e.mape.toFixed(1) + '%' : '-') + ')' +
        (m === T.auto ? '  — 자동 선택' : '') + (e.exploded ? '  — 제외됨' : '');
      modelSel.appendChild(o);
    });
    modelSel.value = curModel;
  }
  modelSel.onchange = function () { curModel = this.value; render(); };

  // 태그/모델이 바뀌면 보기 상태를 기본값으로 되돌린다.
  function resetView() {
    var T = D.perTag[curTag], e = T.models[curModel];
    var act = T.actual, fc = e.fc || [];
    var x0 = act[0][0];
    var x1 = fc.length ? fc[fc.length - 1][0] : act[act.length - 1][0];
    viewFull = { x0: x0, x1: x1 };
    var fcStart = fc.length ? fc[0][0] : x1;
    var fcSpan = (fc.length > 1) ? (fc[fc.length - 1][0] - fc[0][0]) : 0;
    var lo = (fcSpan > 0) ? Math.max(x0, fcStart - DEFAULT_MULT * fcSpan) : x0;
    view = { x0: lo, x1: x1 };
  }

  function renderLb() {
    var T = D.perTag[curTag], ms = T.models;
    document.getElementById('lbFcHead').textContent = D.horizonLabel + ' 후';
    lbBody.innerHTML = '';
    var rank = 0;
    T.order.forEach(function (m) {
      var e = ms[m];
      var tr = document.createElement('tr');
      tr.className = 'clickable' + (m === curModel ? ' is-sel' : '') + (e.exploded ? ' is-out' : '');
      tr.onclick = function () { curModel = m; modelSel.value = m; render(); };
      var rankTxt;
      if (e.exploded) rankTxt = '—';
      else { rank++; rankTxt = String(rank); }   // ✓는 뺀다 — 행 하이라이트 + "자동 선택" 배지로 이미 드러난다
      var desc = e.exploded
        ? '<span class="badge badge-out">제외</span> ' + e.desc
        : (m === T.auto ? '<span class="badge badge-sel">자동 선택</span> ' : '') + e.desc;
      // 예측값을 같이 보여준다 — 실격 행이 **스스로를 설명**하게 만드는 열이다(예: holt → -728 이면 왜 뺐는지 즉시 납득).
      var fcTxt = isFinite(e.endV) ? fmt(e.endV) : '-';
      tr.innerHTML = '<td>' + rankTxt + '</td><td><code>' + m + '</code></td>' +
        '<td class="num">' + (e.mape >= 0 ? e.mape.toFixed(1) + '%' : '-') + '</td>' +
        '<td class="num"' + (e.exploded ? ' style="color:var(--error);font-weight:600;"' : '') + '>' + fcTxt + '</td>' +
        '<td>' + desc + '</td>';
      lbBody.appendChild(tr);
    });
  }

  function renderNote() {
    var T = D.perTag[curTag], e = T.models[curModel];

    var head = '<span class="mn-tag">' + curTag + '</span> <code>' + curModel + '</code>';
    head += (curModel === T.auto)
      ? ' <span class="badge badge-sel">자동 선택</span>'
      : ' <span class="mn-sub">수동 선택</span>';

    var stats =
      '<div class="mn-stat"><div class="mn-label">' + D.horizonLabel + ' 후 예측</div>' +
        '<div class="mn-value">' + fmt(e.endV) + '</div></div>' +
      '<div class="mn-stat"><div class="mn-label">95% 구간 (이 안에 있을 가능성 95%)</div>' +
        '<div class="mn-value sm">' + (isFinite(e.endLo) ? fmt(e.endLo) + ' ~ ' + fmt(e.endHi) : '-') + '</div></div>' +
      '<div class="mn-stat"><div class="mn-label">검증 오차 (MAPE, 낮을수록 정확)</div>' +
        '<div class="mn-value">' + (e.mape >= 0 ? e.mape.toFixed(1) + '%' : '-') + '</div></div>';

    var alert = '';
    if (e.exploded) {
      alert = '<div class="mn-alert"><span>⚠</span><span><b>자동 선택에서 제외된 모델입니다.</b> ' +
        '예측값이 과거 변동폭을 크게 벗어납니다 — 참고로만 보세요.</span></div>';
    } else if (e.mape >= 20) {
      alert = '<div class="mn-alert"><span>⚠</span><span><b>검증 오차가 큽니다.</b> ' +
        '과거 패턴만으로 예측하기 어려운 데이터입니다. 값보다 방향만 참고하세요.</span></div>';
    }

    noteEl.innerHTML = '<div class="mn-head">' + head + '</div><div class="mn-stats">' + stats + '</div>' + alert;
  }

  // ── 차트 (canvas 2D, 외부 라이브러리 없음) ──
  var hit = [];
  function draw() {
    var T = D.perTag[curTag], e = T.models[curModel];
    var dpr = window.devicePixelRatio || 1;
    var W = cv.parentElement.getBoundingClientRect().width, Hh = 460;
    cv.width = W * dpr; cv.height = Hh * dpr; cv.style.width = W + 'px'; cv.style.height = Hh + 'px';
    var ctx = cv.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, Hh);

    var padL = 64, padR = 18, padT = 18, padB = 32;
    var pw = W - padL - padR, ph = Hh - padT - padB;

    var actAll = T.actual, fcAll = e.fc || [], btAll = e.bt || [];
    if (!actAll.length) return;
    if (!view) resetView();

    var xmin = view.x0, xmax = view.x1;

    // 보이는 구간만 그린다. y 범위도 **보이는 것만** 기준으로 잡는다
    // (전체 기준으로 잡으면 과거 저점 때문에 확대해도 납작해 보인다).
    function inView(p) { return p[0] >= xmin && p[0] <= xmax; }
    var act = actAll.filter(inView);
    var fc = fcAll.filter(inView);
    var bt = btAll.filter(inView);
    if (act.length < 2 && actAll.length >= 2) act = actAll.slice(-2);

    var ymin = Infinity, ymax = -Infinity;
    function acc(v) { if (isFinite(v)) { if (v < ymin) ymin = v; if (v > ymax) ymax = v; } }
    act.forEach(function (p) { acc(p[1]); });
    bt.forEach(function (p) { acc(p[1]); });
    fc.forEach(function (p) { acc(p[2]); acc(p[3]); });
    if (!isFinite(ymin)) { ymin = 0; ymax = 1; }
    if (ymin === ymax) { ymin -= 1; ymax += 1; }

    // 눈금을 깔끔하게: 데이터 min/max를 그대로 쓰면 99.33 같은 값이 찍힌다.
    // nice-number로 20·40·60처럼 끔어지는 눈금과 그에 맞춘 축 범위를 잡는다.
    function niceNum(rng, round) {
      var exp = Math.floor(Math.log(rng) / Math.LN10), f = rng / Math.pow(10, exp), nf;
      if (round) { nf = f < 1.5 ? 1 : f < 3 ? 2 : f < 7 ? 5 : 10; }
      else { nf = f <= 1 ? 1 : f <= 2 ? 2 : f <= 5 ? 5 : 10; }
      return nf * Math.pow(10, exp);
    }
    var yStep = niceNum(niceNum(ymax - ymin, false) / 4, true);
    ymin = Math.floor(ymin / yStep) * yStep;
    ymax = Math.ceil(ymax / yStep) * yStep;
    var yTicks = [];
    for (var yv = ymin; yv <= ymax + yStep * 0.5; yv += yStep) yTicks.push(yv);

    function X(t) { return padL + (t - xmin) / (xmax - xmin || 1) * pw; }
    function Y(v) { return padT + ph - (v - ymin) / (ymax - ymin || 1) * ph; }

    ctx.strokeStyle = C.grid; ctx.fillStyle = C.axis; ctx.lineWidth = 1;
    ctx.font = "11px 'D2Coding', Consolas, monospace";
    for (var g = 0; g < yTicks.length; g++) {
      var vy = yTicks[g], y = Y(vy);
      ctx.beginPath(); ctx.moveTo(padL, y); ctx.lineTo(W - padR, y); ctx.stroke();
      ctx.textAlign = 'right'; ctx.fillText(fmt(vy), padL - 8, y + 4);
    }
    for (var g2 = 0; g2 <= 4; g2++) {
      var tx = xmin + (xmax - xmin) * g2 / 4;
      // \uc591 \ub05d \ub77c\ubca8\uc740 \uc548\ucabd \uc815\ub82c\ub85c \u2014 \uac00\uc6b4\ub370 \uc815\ub82c\uc774\uba74 \ub9c8\uc9c0\ub9c9 \ub0a0\uc9dc\uac00 \uce90\ubc84\uc2a4 \ubc16\uc73c\ub85c \uc798\ub9b0\ub2e4.
      ctx.textAlign = g2 === 0 ? 'left' : g2 === 4 ? 'right' : 'center';
      ctx.fillText(fmtDate(tx), X(tx), Hh - 10);
    }

    // 95% 구간: 채움을 옅게 하고 **위·아래 경계선**을 그린다.
    // (진한 단색으로 채웠더니 "갈색 덩어리"로 보여 범위라는 게 안 읽혔다.)
    if (fc.length > 1) {
      ctx.beginPath();
      ctx.moveTo(X(fc[0][0]), Y(fc[0][3]));
      for (var i = 1; i < fc.length; i++) ctx.lineTo(X(fc[i][0]), Y(fc[i][3]));
      for (var j = fc.length - 1; j >= 0; j--) ctx.lineTo(X(fc[j][0]), Y(fc[j][2]));
      ctx.closePath();
      // \ucc44\uc6c0\uc744 \uc194\ub9ac\ub4dc \uc568\ubc84\ub85c \uae54\uba74 \ub113\uc740 \ub760\uac00 \uc5b4\ub450\uc6b4 \ubc30\uacbd\uacfc \uc11e\uc5ec \u2018\uac08\uc0c9 \uc5bc\ub8e9\u2019\uc774 \ub41c\ub2e4.\n      // \uc138\ub85c \uadf8\ub77c\ub514\uc5b8\ud2b8\ub85c \uc704\u00b7\uc544\ub798 \ub05d\ub9cc \uc568\ubc84\ub97c \ub0a8\uae30\uace0 \uac00\uc6b4\ub370\ub294 \uac70\uc758 \ud22c\uba85\ud558\uac8c \u2192 \ubc94\uc704\ub9cc \uc77d\ud78c\ub2e4.\n      var bg = ctx.createLinearGradient(0, padT, 0, padT + ph);\n      bg.addColorStop(0, 'rgba(253,181,50,0.16)');\n      bg.addColorStop(0.5, 'rgba(253,181,50,0.035)');\n      bg.addColorStop(1, 'rgba(253,181,50,0.16)');\n      ctx.fillStyle = bg; ctx.fill();

      ctx.setLineDash([2, 3]); ctx.strokeStyle = C.bandEdge; ctx.lineWidth = 1;
      var e2;
      for (e2 = 2; e2 <= 3; e2++) {                       // 2 = lo, 3 = hi
        ctx.beginPath();
        for (i = 0; i < fc.length; i++) {
          var xx = X(fc[i][0]), yy = Y(fc[i][e2]);
          if (i === 0) ctx.moveTo(xx, yy); else ctx.lineTo(xx, yy);
        }
        ctx.stroke();
      }
      ctx.setLineDash([]);
    }

    function line(pts, color, dash, width) {
      if (!pts.length) return;
      ctx.beginPath(); ctx.setLineDash(dash || []);
      ctx.strokeStyle = color; ctx.lineWidth = width || 2;
      for (var i = 0; i < pts.length; i++) {
        var x = X(pts[i][0]), y = Y(pts[i][1]);
        if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke(); ctx.setLineDash([]);
    }
    line(act, C.actual, [], 1.6);
    line(bt, C.backtest, [2, 3], 1.4);
    line(fc.map(function (p) { return [p[0], p[1]]; }), C.forecast, [], 2.4);

    // 예측 시작선은 **원본 fc의 첫 점** 기준(줌으로 잘린 fc[0]을 쓰면 엉뚱한 위치에 그어진다).
    if (fcAll.length) {
      var fcT = fcAll[0][0];
      if (fcT >= xmin && fcT <= xmax) {
        var xs = X(fcT);
        ctx.beginPath(); ctx.setLineDash([3, 3]); ctx.strokeStyle = C.divider; ctx.lineWidth = 1;
        ctx.moveTo(xs, padT); ctx.lineTo(xs, padT + ph); ctx.stroke(); ctx.setLineDash([]);
        ctx.fillStyle = C.axis; ctx.textAlign = 'left';
        ctx.font = "11px 'Pretendard', sans-serif";
        if (xs < W - padR - 70) ctx.fillText('예측 시작', xs + 5, padT + 11);
      }
    }

    hit = [];
    act.forEach(function (p) { hit.push({ x: X(p[0]), y: Y(p[1]), t: p[0], v: p[1], k: '실측' }); });
    fc.forEach(function (p) { hit.push({ x: X(p[0]), y: Y(p[1]), t: p[0], v: p[1], lo: p[2], hi: p[3], k: '예측' }); });
  }

  cv.onmousemove = function (ev) {
    var r = cv.getBoundingClientRect(), mx = ev.clientX - r.left;
    var best = null, bd = Infinity;
    for (var i = 0; i < hit.length; i++) {
      var d = Math.abs(hit[i].x - mx);
      if (d < bd) { bd = d; best = hit[i]; }
    }
    if (best && bd < 40) {
      var s = '<b>' + fmtDate(best.t) + '</b><br>' + best.k + ' ' + fmt(best.v);
      if (best.k === '예측' && isFinite(best.lo)) s += '<br>95% ' + fmt(best.lo) + ' ~ ' + fmt(best.hi);
      tip.innerHTML = s; tip.style.display = 'block';
      var tx = best.x + 14; if (tx + 170 > r.width) tx = best.x - 170;
      tip.style.left = tx + 'px'; tip.style.top = Math.max(8, best.y - 42) + 'px';
    } else { tip.style.display = 'none'; }
  };
  cv.onmouseleave = function () { tip.style.display = 'none'; drag.active = false; cv.style.cursor = 'grab'; };

  // ── 줌/팬 (기존 리포트 차트와 동일한 조작감) ──
  var PAD_L = 64, PAD_R = 18;
  var MIN_SPAN_RATIO = 0.02;                          // 전체의 2%까지만 확대(과확대로 빈 화면 되는 것 방지)

  cv.addEventListener('wheel', function (ev) {
    if (!view || !viewFull) return;
    ev.preventDefault();
    var rect = cv.getBoundingClientRect();
    var cw = rect.width - PAD_L - PAD_R;
    var ratio = Math.max(0, Math.min(1, (ev.clientX - rect.left - PAD_L) / cw));  // 커서 위치를 고정점으로
    var span = view.x1 - view.x0;
    var full = viewFull.x1 - viewFull.x0;
    var newSpan = span * (ev.deltaY > 0 ? 1.3 : 0.7);
    if (newSpan >= full) { view = { x0: viewFull.x0, x1: viewFull.x1 }; draw(); return; }
    if (newSpan < full * MIN_SPAN_RATIO) newSpan = full * MIN_SPAN_RATIO;
    var center = view.x0 + span * ratio;
    var x0 = center - newSpan * ratio, x1 = x0 + newSpan;
    if (x0 < viewFull.x0) { x0 = viewFull.x0; x1 = x0 + newSpan; }
    if (x1 > viewFull.x1) { x1 = viewFull.x1; x0 = x1 - newSpan; }
    view = { x0: x0, x1: x1 };
    draw();
  }, { passive: false });

  cv.addEventListener('dblclick', function () { resetView(); draw(); });

  var drag = { active: false, x: 0, x0: 0, x1: 0 };
  cv.addEventListener('mousedown', function (ev) {
    if (!view) return;
    drag.active = true; drag.x = ev.clientX; drag.x0 = view.x0; drag.x1 = view.x1;
    cv.style.cursor = 'grabbing';
  });
  window.addEventListener('mousemove', function (ev) {
    if (!drag.active || !viewFull) return;
    var rect = cv.getBoundingClientRect();
    var cw = rect.width - PAD_L - PAD_R;
    var span = drag.x1 - drag.x0;
    var shift = -(ev.clientX - drag.x) / cw * span;
    var x0 = drag.x0 + shift, x1 = drag.x1 + shift;
    if (x0 < viewFull.x0) { x0 = viewFull.x0; x1 = x0 + span; }
    if (x1 > viewFull.x1) { x1 = viewFull.x1; x0 = x1 - span; }
    view = { x0: x0, x1: x1 };
    draw();
  });
  window.addEventListener('mouseup', function () {
    if (!drag.active) return;
    drag.active = false; cv.style.cursor = 'grab';
  });

  function render() { draw(); renderLb(); renderNote(); }

  function applyChartTheme() {
    var light = document.documentElement.classList.contains('theme-light');
    C.grid = light ? 'rgba(0,0,0,0.09)' : 'rgba(255,255,255,0.07)';
    C.axis = light ? '#5f636f' : '#a3a3a3';
    C.divider = light ? '#a7abb5' : '#626263';
  }
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) themeBtn.onclick = function () {
    var el = document.documentElement;
    el.classList.toggle('theme-light');
    try { localStorage.setItem('neoReportTheme2', el.classList.contains('theme-light') ? 'light' : 'dark'); } catch (e) {}
    applyChartTheme(); draw();
  };
  applyChartTheme();

  setTag(curTag);            // 두 셀렉터·모델·보기 상태를 한 번에 초기화
  cv.style.cursor = 'grab';
  window.addEventListener('resize', function () { draw(); });
})();
</script>
<script>
// 위험 행(●) 즉석 툴팁 — 네이티브 title은 커서를 ~1초 정지해야 떠서 사실상 발견 불가(라이브 피드백 "호버 안 뜨는데?")
// → 행 위에서 커서를 따라 즉시 표시. 메인 스크립트와 분리(데이터 없어도 동작해야 하므로 — 메인은 태그 0이면 조기 return).
(function () {
  var rows = document.querySelectorAll('tr[data-tip]');
  if (!rows.length) return;
  var t = document.createElement('div');
  t.className = 'tooltip fixed';
  document.body.appendChild(t);
  Array.prototype.forEach.call(rows, function (tr) {
    tr.addEventListener('mousemove', function (e) {
      t.textContent = tr.getAttribute('data-tip');
      t.style.display = 'block';
      var x = Math.min(e.clientX + 14, window.innerWidth - t.offsetWidth - 8);
      t.style.left = x + 'px';
      t.style.top = (e.clientY + 16) + 'px';
    });
    tr.addEventListener('mouseleave', function () { t.style.display = 'none'; });
  });
})();
</script>
</body>
</html>
```
