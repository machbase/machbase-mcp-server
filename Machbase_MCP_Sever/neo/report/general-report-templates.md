# 범용 데이터 HTML 분석 리포트 템플릿

도메인에 관계없이 모든 시계열 데이터에 적용 가능한 범용 HTML 분석 리포트 템플릿입니다.
차트 없이 통계 테이블과 AI 분석 텍스트로 구성됩니다.

## 디자인
**예측 리포트(neo/forecast)와 동일한 Neo Web UI 디자인 체계**(2026-07-14 이식) — 기본 다크 모드, 우상단 토글로 라이트 전환(localStorage `neoReportTheme2`), Pretendard/D2Coding, 레터헤드 헤더(로고 base64 인라인), 스펙 패널, `| bar` 섹션 타이틀. 차트가 없으므로 canvas 팔레트(JS `CC`)는 불필요 — 테마 전환은 CSS 변수만으로 완결.

## 변수 설명
| 변수 | 설명 | 채우는 주체 |
|------|------|------------|
| {TABLE} | 테이블명 | SQL 결과 |
| {GENERATED_DATE} | 리포트 생성 일시 | 자동 삽입 |
| {TAG_COUNT} | 태그 수 | SQL 결과 |
| {DATA_COUNT} | 총 데이터 건수 | SQL 결과 |
| {TIME_RANGE} | 데이터 시간 범위 | SQL 결과 |
| {TAG_STATS_ROWS} | 태그별 통계 `<tr>` 행 | SQL → 자동 변환 |
| {ANALYSIS} | 심층 분석 | LLM 생성 |
| {RECOMMENDATIONS} | 종합 소견 및 권고 | LLM 생성 |

---

### R-0-general. 범용 데이터 종합 분석 리포트
용도: 도메인 구분 없이 모든 시계열 데이터의 태그별 통계와 AI 심층 분석을 보여주는 범용 보고서입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TABLE} 데이터 분석 리포트</title>
<!-- 기본 = 다크(:root 토큰 그대로). 저장된 선택이 라이트일 때만 theme-light 부착(head 동기 실행 — 플래시 없음). -->
<script>try{if(localStorage.getItem('neoReportTheme2')==='light')document.documentElement.classList.add('theme-light');}catch(e){}</script>
<style>
  /* Neo Web UI design tokens (src/design-system/tokens/_colors.scss) — 예측 리포트와 동일 체계 */
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

    --radius-sm: 4px;
    --radius-md: 8px;
    --shadow-sm: 0 2px 2px rgba(0, 0, 0, 0.25);
  }
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

  /* Header — 레터헤드: 왼쪽 제목·메타 / 오른쪽 로고·테마토글 */
  .report-header {
    display: flex; align-items: flex-start; justify-content: space-between; gap: 24px;
    padding: 4px 0 26px; border-bottom: 1px solid var(--border-default); margin-bottom: 28px;
  }
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

  /* 스펙 패널 — KPI 카드 대신 하나의 패널을 세로 구분선으로 나눈다 */
  .spec-panel { display: flex; flex-wrap: wrap; background: var(--bg-panel); border: 1px solid var(--border-default); border-radius: var(--radius-md); overflow: hidden; margin-bottom: 28px; }
  .spec-col { flex: 1 1 0; min-width: 180px; padding: 18px 22px; border-right: 1px solid var(--border-default); display: flex; flex-direction: column; }
  .spec-col:last-child { border-right: none; }
  .spec-k { font-size: 11px; font-weight: 600; letter-spacing: 0.5px; text-transform: uppercase; color: var(--text-muted); }
  .spec-v { margin-top: 7px; font-size: 24px; font-weight: 700; color: var(--text-primary); font-variant-numeric: tabular-nums; line-height: 1.1; }
  .spec-v .unit { font-size: 14px; font-weight: 600; color: var(--text-tertiary); margin-left: 2px; }
  .spec-v.small { font-size: 17px; font-weight: 600; margin-top: 11px; font-family: 'D2Coding', 'Consolas', monospace; }
  /* 기간 칸: 풀 타임스탬프가 길어 줄바꿈으로 뭉개짐 → 넓게 + 아래 축약 스크립트 */
  .spec-col.wide { flex: 1.8 1 0; min-width: 260px; }

  /* Section */
  .section { background: var(--bg-panel); border: 1px solid var(--border-default); border-radius: var(--radius-md); padding: 24px 26px; margin-bottom: 24px; }
  .section-title { display: flex; align-items: center; gap: 9px; font-size: 17px; font-weight: 600; color: var(--text-primary); margin-bottom: 18px; }
  .section-title .bar { width: 3px; height: 16px; border-radius: 2px; background: var(--primary); }

  /* Table */
  table { width: 100%; border-collapse: collapse; font-size: 14px; }
  thead th {
    text-align: left; font-weight: 600; color: var(--text-tertiary); font-size: 13px;
    padding: 12px 14px; border-bottom: 1px solid var(--border-default); white-space: nowrap;
  }
  tbody td { padding: 12px 14px; border-bottom: 1px solid var(--border-faint); color: var(--text-secondary); }
  tbody tr:last-child td { border-bottom: none; }
  tbody tr:hover td { background: var(--bg-hover); }
  .num { text-align: right; font-variant-numeric: tabular-nums; font-family: 'D2Coding', 'Consolas', 'Menlo', monospace; }
  .table-scroll { max-height: 400px; overflow-y: auto; border: 1px solid var(--border-faint); border-radius: var(--radius-sm); }

  /* Analysis */
  .analysis-content { color: var(--text-secondary); font-size: 15px; line-height: 1.9; }
  .analysis-content p { margin-bottom: 14px; }
  .analysis-content strong { color: var(--text-primary); font-weight: 600; }
  .analysis-content ul, .analysis-content ol { margin: 12px 0 16px 24px; }
  .analysis-content li { margin-bottom: 10px; padding-left: 4px; line-height: 1.7; }
  .analysis-content ol li { list-style-type: decimal; }
  .analysis-content li::marker { color: var(--primary-hover); font-weight: 700; }

  .report-footer { text-align: center; padding: 26px 0 0; color: var(--text-muted); font-size: 12px; border-top: 1px solid var(--border-default); margin-top: 12px; }

  @media print { body { background: #fff; } .page { padding: 0; } .section { box-shadow: none; } }
  @media (max-width: 768px) { .spec-col { flex-basis: 45%; } .page { padding: 16px; } }
</style>
</head>
<body>
<div class="page">

  <div class="report-header">
    <div>
      <div class="eyebrow">Data Analysis Report</div>
      <h1><span class="hl">{TABLE}</span> 데이터 분석 리포트</h1>
      <div class="meta-row">
        <span class="meta"><span class="meta-k">생성</span><span class="meta-v mono">{GENERATED_DATE}</span></span>
        <span class="meta"><span class="meta-k">소스</span><span class="meta-v"><span class="mono">{TABLE}</span> &middot; TAG table</span></span>
        <span class="meta"><span class="meta-k">기간</span><span class="meta-v mono" id="metaRange">{TIME_RANGE}</span></span>
      </div>
    </div>
    <div class="hd-right">
      <img class="logo" src="data:image/png;base64,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" alt="Machbase">
      <button id="themeBtn" class="theme-btn" type="button" aria-label="테마 전환"><svg class="ic-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.8A9 9 0 1 1 11.2 3 7 7 0 0 0 21 12.8z"></path></svg><svg class="ic-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"></circle><path d="M12 2v2M12 20v2M4.9 4.9l1.4 1.4M17.7 17.7l1.4 1.4M2 12h2M20 12h2M4.9 19.1l1.4-1.4M17.7 6.3l1.4-1.4"></path></svg></button>
    </div>
  </div>

  <div class="spec-panel">
    <div class="spec-col">
      <div class="spec-k">테이블</div>
      <div class="spec-v">{TABLE}</div>
    </div>
    <div class="spec-col">
      <div class="spec-k">태그</div>
      <div class="spec-v">{TAG_COUNT}<span class="unit">개</span></div>
    </div>
    <div class="spec-col">
      <div class="spec-k">데이터</div>
      <div class="spec-v">{DATA_COUNT}<span class="unit">건</span></div>
    </div>
    <div class="spec-col wide">
      <div class="spec-k">분석 기간</div>
      <div class="spec-v small" id="specRange">{TIME_RANGE}</div>
    </div>
  </div>

  <!-- Tag Stats -->
  <div class="section">
    <div class="section-title"><span class="bar"></span> 태그별 통계 요약</div>
    <div class="table-scroll">
    <table>
      <thead><tr>
        <th>태그(NAME)</th><th class="num">건수(COUNT)</th><th class="num">평균(AVG)</th><th class="num">최솟값(MIN)</th><th class="num">최댓값(MAX)</th>
      </tr></thead>
      <tbody>{TAG_STATS_ROWS}</tbody>
    </table>
    </div>
  </div>

  <!-- Analysis -->
  <div class="section">
    <div class="section-title"><span class="bar"></span> 심층 분석</div>
    <div class="analysis-content">{ANALYSIS}</div>
  </div>

  <!-- Recommendations -->
  <div class="section">
    <div class="section-title"><span class="bar"></span> 종합 소견 및 권고사항</div>
    <div class="analysis-content">{RECOMMENDATIONS}</div>
  </div>

  <div class="report-footer">Machbase Neo 데이터 기반으로 생성 되었습니다.</div>
</div>

<script>
// 테마 토글 — 차트가 없어 CSS 변수 전환만으로 완결(재그리기 불필요).
(function () {
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) themeBtn.onclick = function () {
    var el = document.documentElement;
    el.classList.toggle('theme-light');
    try { localStorage.setItem('neoReportTheme2', el.classList.contains('theme-light') ? 'light' : 'dark'); } catch (e) {}
  };
})();
</script>
<script>
// 기간 표기 축약 — "YYYY-MM-DD 00:00:00 ~ ..." 풀 타임스탬프가 스펙 칸을 여러 줄로 뭉갬(라이브 스크린샷).
// **초만 제거**(시:분은 항상 표시 — 사용자 확정): "2023-09-21 00:00 ~ 2026-02-11 18:00". 표시만 바꾼다.
(function () {
  ['specRange', 'metaRange'].forEach(function (id) {
    var el = document.getElementById(id);
    if (!el) return;
    el.textContent = el.textContent.replace(/(\d{2}:\d{2}):\d{2}/g, '$1');
  });
})();
</script>
</body>
</html>
```
