---
compute: finance
guide: |
  기간 변동률과 거래량을 반드시 참조해 시장 동향을 해석하라. 수익률 수준에 맞는 톤을 스스로 판단(상승=강세 요인·지속성, 하락=리스크·반등 가능성).
  - 가격 추세(상승/하락/횡보) 판단
  - 거래량 변화와 가격 움직임의 상관관계
  - recommendations는 투자 판단에 참고할 시장 전망과 전략으로 작성
---
# 금융 데이터 HTML 분석 리포트 템플릿

금융 데이터(주가, 환율, 원자재 등)에 적합한 HTML 분석 리포트 템플릿입니다.

## 디자인
**예측 리포트(neo/forecast)와 동일한 Neo Web UI 디자인 체계**(2026-07-14 이식) — `src/design-system/tokens/_colors.scss` 기준.
- **기본 다크 모드**, 우상단 토글로 다크 전환(localStorage `neoReportTheme2` 저장, light 저장 시에만 head 스크립트가 `theme-light` 부착)
- 폰트 Pretendard(UI) / D2Coding(숫자·코드), 레터헤드 헤더(로고 base64 인라인 — 단일 HTML로 이동 가능해야 하므로 외부 참조 금지)
- KPI 카드 → **스펙 패널**(세로 구분선), 섹션 타이틀 = `| bar`, 차트 섹션은 `section-chart` 톤
- ⚠️ canvas는 CSS 변수를 못 읽으므로 **중립색(격자/축)은 JS `CC` 팔레트**로 복제 — 테마 토글 시 `applyChartTheme()`+전체 재그리기. 시리즈 색(파랑/캔들 녹적/MA)은 두 모드 공용.

## 변수 설명
| 변수 | 설명 | 채우는 주체 |
|------|------|------------|
| {TABLE} | 테이블명 | SQL 결과 |
| {STOCK_NAME} | 종목/자산명 (예: AAPL, GOLD) | SQL 결과 |
| {GENERATED_DATE} | 리포트 생성 일시 | 자동 삽입 |
| {TAG_COUNT} | 태그 수 | SQL 결과 |
| {DATA_COUNT} | 총 데이터 건수 | SQL 결과 |
| {TIME_RANGE} | 데이터 시간 범위 | SQL 결과 |
| {TAG_STATS_ROWS} | 태그별 통계 `<tr>` 행 | SQL → LLM 변환 |
| {CHART_DATA_JSON} | 태그별 통계 JSON | SQL → LLM 변환 |
| {TREND_DATA_JSON} | OHLCV 시계열 JSON | SQL → LLM 변환 |
| {ANALYSIS} | 심층 분석 | LLM 생성 |
| {RECOMMENDATIONS} | 종합 소견 및 권고 | LLM 생성 |

---

### R-1-finance. 금융 데이터 종합 분석 리포트
용도: 금융 데이터(OHLCV)의 캔들스틱, 이동평균, 볼린저밴드, 거래량-가격 상관을 차트와 함께 보여주는 심층 분석 보고서입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{STOCK_NAME} 금융 데이터 분석 리포트</title>
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
  .section.section-chart { background: var(--bg-primary); }
  .section-title { display: flex; align-items: center; gap: 9px; font-size: 17px; font-weight: 600; color: var(--text-primary); margin-bottom: 18px; }
  .section-title .bar { width: 3px; height: 16px; border-radius: 2px; background: var(--primary); }
  .chart-badge {
    display: inline-flex; align-items: center; gap: 6px; padding: 3px 8px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.2px;
    color: var(--primary-hover); background: rgba(0, 108, 210, 0.12);
    border: 1px solid rgba(0, 108, 210, 0.28); border-radius: var(--radius-sm);
  }
  .chart-badge svg { width: 13px; height: 13px; }

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

  /* Chart */
  .chart-wrap { position: relative; overflow: hidden; }
  canvas { width: 100%; display: block; background: var(--bg-elevated); border: 1px solid var(--border-default); border-radius: var(--radius-sm); }
  .tooltip {
    position: absolute; pointer-events: none; display: none; z-index: 10;
    background: var(--bg-dropdown); color: var(--text-primary);
    border: 1px solid var(--border-medium); border-radius: var(--radius-sm);
    padding: 7px 10px; font-size: 12px; line-height: 1.6; white-space: nowrap; box-shadow: var(--shadow-sm);
  }
  .crosshair { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; display: none; z-index: 5; }
  .crosshair-v { width: 1px; background: rgba(0, 117, 226, 0.45); position: absolute; top: 0; height: 100%; }
  .legend { display: flex; flex-wrap: wrap; align-items: center; gap: 8px 18px; margin-bottom: 12px; font-size: 13px; color: var(--text-tertiary); }
  .legend-item { display: flex; align-items: center; gap: 7px; }
  .legend-swatch { width: 20px; height: 2px; border-radius: 1px; }
  .nav-hint { margin-left: auto; font-size: 12px; color: var(--text-muted); }
  .nav-hint b { color: var(--text-tertiary); font-weight: 600; }
  .chart-full { margin-bottom: 6px; }

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
      <div class="eyebrow">Financial Analysis Report</div>
      <h1><span class="hl">{STOCK_NAME}</span> 금융 데이터 분석 리포트</h1>
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
      <div class="spec-k">종목</div>
      <div class="spec-v">{STOCK_NAME}</div>
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

  <!-- Candlestick Chart (OHLC) -->
  <div class="section section-chart" id="candlestickSection">
    <div class="section-title"><span class="bar"></span> 캔들스틱 (OHLC)
      <span class="chart-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 9 2 12 5 15"></polyline><polyline points="9 5 12 2 15 5"></polyline><polyline points="15 19 12 22 9 19"></polyline><polyline points="19 9 22 12 19 15"></polyline><line x1="2" y1="12" x2="22" y2="12"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>확대·이동</span>
      <span class="nav-hint"><b>휠</b> 확대·축소 &middot; <b>드래그</b> 좌우 이동 &middot; <b>더블클릭</b> 되돌리기</span>
    </div>
    <div class="chart-full chart-wrap"><canvas id="candleChart" height="360"></canvas><div class="crosshair" id="candleCross"><div class="crosshair-v"></div></div><div class="tooltip" id="candleTip"></div></div>
  </div>

  <!-- Price Trend + Moving Averages -->
  <div class="section section-chart" id="trendSection">
    <div class="section-title"><span class="bar"></span> 가격 추세 + 이동평균</div>
    <div class="legend" id="trendLegend">
      <div class="legend-item"><div class="legend-swatch" style="background:#4a7cfa;height:3px;"></div>Close</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#f59e42;"></div>MA5</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#48bb78;"></div>MA20</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#9f7aea;"></div>MA60</div>
    </div>
    <div class="chart-full chart-wrap"><canvas id="trendChart" height="340"></canvas><div class="crosshair" id="trendCross"><div class="crosshair-v"></div></div><div class="tooltip" id="trendTip"></div></div>
  </div>

  <!-- Bollinger Bands -->
  <div class="section section-chart" id="bollingerSection">
    <div class="section-title"><span class="bar"></span> 볼린저밴드 (Bollinger Bands)</div>
    <div class="legend">
      <div class="legend-item"><div class="legend-swatch" style="background:#4a7cfa;height:3px;"></div>Close</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#e53e3e;"></div>MA20</div>
      <div class="legend-item"><div class="legend-swatch" style="background:rgba(159,122,234,0.35);height:8px;border-radius:2px;"></div>Band (&#177;2&#963;)</div>
    </div>
    <div class="chart-full chart-wrap"><canvas id="bbChart" height="340"></canvas><div class="crosshair" id="bbCross"><div class="crosshair-v"></div></div><div class="tooltip" id="bbTip"></div></div>
  </div>

  <!-- Volume-Price Correlation -->
  <div class="section section-chart" id="volumeSection">
    <div class="section-title"><span class="bar"></span> 거래량-가격 상관 (Volume-Price)</div>
    <div class="chart-full chart-wrap"><canvas id="volumeChart" height="320"></canvas><div class="crosshair" id="volumeCross"><div class="crosshair-v"></div></div><div class="tooltip" id="volumeTip"></div></div>
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
(function(){
  var rawStats = {CHART_DATA_JSON};
  var allStats = rawStats.map(function(d) {
    return { name: d.name||d.tag||'', avg: Number(d.avg)||0, min: Number(d.min)||0, max: Number(d.max)||0, count: Number(d.count)||0 };
  });

  var rawTrend = {TREND_DATA_JSON};
  var trend = rawTrend.map(function(d) {
    var t = d.time || d.t || '';
    return {
      time: t,
      open: d.open != null ? Number(d.open) : null,
      high: d.high != null ? Number(d.high) : null,
      low: d.low != null ? Number(d.low) : null,
      close: d.close != null ? Number(d.close) : 0,
      volume: d.volume != null ? Number(d.volume) : 0
    };
  });

  var hasOHLC = trend.some(function(d){ return d.open !== null && d.high !== null && d.low !== null; });
  var hasVolume = trend.some(function(d){ return d.volume > 0; });
  var dpr = window.devicePixelRatio || 1;

  /* ---- 차트 중립색(격자/축) — canvas는 CSS 변수를 못 읽으므로 여기서 테마별로 복제(_colors.scss와 동일 값).
          시리즈 색(파랑 종가/MA/캔들 녹적/밴드 보라)은 두 모드 공용이라 바꾸지 않는다. ---- */
  var CC = { grid: '', axis: '', axisLine: '', hint: '' };
  function applyChartTheme() {
    var light = document.documentElement.classList.contains('theme-light');
    CC.grid = light ? 'rgba(0,0,0,0.08)' : 'rgba(255,255,255,0.07)';
    CC.axis = light ? '#5f636f' : '#a3a3a3';
    CC.axisLine = light ? '#b9bcc5' : '#626263';
    CC.hint = light ? '#8a8d99' : '#727272';
  }
  applyChartTheme();
  var FONT = 'Pretendard, sans-serif';

  /* ---- Utility functions ---- */
  function setup(id, h) {
    var c = document.getElementById(id);
    if (!c) return null;
    var w = c.parentElement.getBoundingClientRect().width;
    c.width = w * dpr; c.height = h * dpr;
    c.style.width = w + 'px'; c.style.height = h + 'px';
    var ctx = c.getContext('2d');
    ctx.scale(dpr, dpr);
    return { ctx: ctx, w: w, h: h, canvas: c };
  }

  function niceMax(v) { if (v <= 0) return 1; var p = Math.pow(10, Math.floor(Math.log10(v))); return Math.ceil(v / p) * p; }
  function niceMin(v) { if (v <= 0) return 0; var p = Math.pow(10, Math.floor(Math.log10(v))); return Math.floor(v / p) * p; }

  function fmt(v) {
    if (v == null || isNaN(v)) return '-';
    var abs = Math.abs(v);
    if (abs >= 1e7) return (v / 1e6).toFixed(1) + 'M';
    if (abs >= 10000) return (v / 1000).toFixed(0) + 'K';
    if (abs >= 1000) return v.toLocaleString(undefined, { maximumFractionDigits: 1 });
    if (abs >= 1) return v.toFixed(2);
    return v.toPrecision(4);
  }

  function calcMA(data, period) {
    var result = [];
    for (var i = 0; i < data.length; i++) {
      if (i < period - 1) { result.push(null); continue; }
      var sum = 0;
      for (var j = i - period + 1; j <= i; j++) sum += data[j].close;
      result.push(sum / period);
    }
    return result;
  }

  function calcStdDev(data, period, ma) {
    var result = [];
    for (var i = 0; i < data.length; i++) {
      if (ma[i] === null) { result.push(null); continue; }
      var sum = 0;
      for (var j = i - period + 1; j <= i; j++) {
        var diff = data[j].close - ma[i];
        sum += diff * diff;
      }
      result.push(Math.sqrt(sum / period));
    }
    return result;
  }

  /* ---- Tooltip helper ---- */
  function addTip(canvasId, tipId, pts) {
    var cv = document.getElementById(canvasId), tip = document.getElementById(tipId);
    if (!cv || !tip || !pts.length) return;
    var cross = document.getElementById(canvasId.replace('Chart', 'Cross'));
    cv.style.cursor = 'crosshair';
    cv.addEventListener('mousemove', function(e) {
      var r = cv.getBoundingClientRect(), mx = e.clientX - r.left, my = e.clientY - r.top;
      var best = null, bd = Infinity;
      pts.forEach(function(p) { var d = Math.abs(p.x - mx); if (d < bd) { bd = d; best = p; } });
      if (best && bd < 50) {
        tip.innerHTML = best.label; tip.style.display = 'block';
        var tx = best.x + 14; if (tx + 180 > r.width) tx = best.x - 180;
        var ty = Math.max(4, best.y - 24); if (ty < 4) ty = 4;
        tip.style.left = tx + 'px'; tip.style.top = ty + 'px';
        if (cross) { cross.style.display = 'block'; cross.querySelector('.crosshair-v').style.left = best.x + 'px'; }
      } else { tip.style.display = 'none'; if (cross) cross.style.display = 'none'; }
    });
    cv.addEventListener('mouseleave', function() { tip.style.display = 'none'; if (cross) cross.style.display = 'none'; });
  }

  /* ---- Scroll zoom helper ---- */
  function addZoom(canvasId, state, dataLen, drawFn) {
    var cv = document.getElementById(canvasId);
    if (!cv) return;
    cv.addEventListener('wheel', function(e) {
      e.preventDefault();
      var rect = cv.getBoundingClientRect();
      var mx = e.clientX - rect.left;
      var pad = { l: 65, r: 50 };
      var cw = rect.width - pad.l - pad.r;
      var n = state.end - state.start;
      var ratio = Math.max(0, Math.min(1, (mx - pad.l) / cw));
      var zoomFactor = e.deltaY > 0 ? 1.3 : 0.7;
      var newN = Math.round(n * zoomFactor);
      if (newN < 5) newN = 5;
      if (newN >= dataLen) { state.start = 0; state.end = dataLen; state.zoomed = false; drawFn(); return; }
      var center = state.start + Math.round(n * ratio);
      var newStart = Math.round(center - newN * ratio);
      if (newStart < 0) newStart = 0;
      var newEnd = newStart + newN;
      if (newEnd > dataLen) { newEnd = dataLen; newStart = newEnd - newN; }
      state.start = Math.max(0, newStart); state.end = newEnd; state.zoomed = true;
      drawFn();
    }, { passive: false });
    cv.addEventListener('dblclick', function() { state.start = 0; state.end = dataLen; state.zoomed = false; drawFn(); });
    // Drag to pan
    var drag = { active: false, startX: 0, startS: 0, startE: 0 };
    cv.addEventListener('mousedown', function(ev) {
      if (state.end - state.start >= dataLen) return;
      drag.active = true; drag.startX = ev.clientX; drag.startS = state.start; drag.startE = state.end;
      cv.style.cursor = 'grabbing';
    });
    cv.addEventListener('mousemove', function(ev) {
      if (!drag.active) return;
      var rect = cv.getBoundingClientRect(), cw = rect.width - 115;
      var n = drag.startE - drag.startS;
      var shift = Math.round(-(ev.clientX - drag.startX) / cw * n);
      var ns = drag.startS + shift, ne = drag.startE + shift;
      if (ns < 0) { ns = 0; ne = n; }
      if (ne > dataLen) { ne = dataLen; ns = dataLen - n; }
      state.start = ns; state.end = ne; state.zoomed = true;
      drawFn();
    });
    function endDrag() { drag.active = false; cv.style.cursor = 'crosshair'; }
    cv.addEventListener('mouseup', endDrag);
    cv.addEventListener('mouseleave', endDrag);
  }

  /* ---- Draw grid + Y axis ---- */
  function drawGrid(ctx, pad, W, H, mn, mx, steps) {
    var ch = H - pad.t - pad.b;
    var range = mx - mn || 1;
    ctx.strokeStyle = CC.grid; ctx.lineWidth = 1;
    for (var i = 0; i <= steps; i++) {
      var y = pad.t + ch - (ch * i / steps);
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W - pad.r, y); ctx.stroke();
      ctx.fillStyle = CC.axis; ctx.font = '11px ' + FONT; ctx.textAlign = 'right';
      ctx.fillText(fmt(mn + range * i / steps), pad.l - 10, y + 4);
    }
  }

  /* ---- Draw X axis labels ---- */
  function drawXLabels(ctx, slice, pad, W, H, step, offset) {
    var n = slice.length;
    ctx.fillStyle = CC.axis; ctx.font = '10px ' + FONT; ctx.textAlign = 'center';
    var ls = Math.max(1, Math.floor(n / 8));
    for (var i = 0; i < n; i += ls) {
      ctx.fillText(slice[i].time, pad.l + step * i + (offset || 0), H - pad.b + 18);
    }
    if ((n - 1) % ls !== 0) {
      ctx.fillText(slice[n - 1].time, pad.l + step * (n - 1) + (offset || 0), H - pad.b + 18);
    }
  }

  /* ---- Draw bottom axis line ---- */
  function drawAxisLine(ctx, pad, W, H) {
    var ch = H - pad.t - pad.b;
    ctx.strokeStyle = CC.axisLine; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(pad.l, pad.t + ch); ctx.lineTo(W - pad.r, pad.t + ch); ctx.stroke();
  }

  /* ---- Zoom hint text ---- */
  function drawZoomHint(ctx, pad, zoomed) {
    ctx.fillStyle = CC.hint; ctx.font = '10px ' + FONT; ctx.textAlign = 'left';
    ctx.fillText(zoomed ? 'Double-click to reset' : 'Scroll to zoom', pad.l, pad.t - 10);
  }

  /* ==============================================================
     1. CANDLESTICK CHART
     ============================================================== */
  if (!hasOHLC) {
    var csec = document.getElementById('candlestickSection');
    if (csec) csec.style.display = 'none';
  }

  var candleState = { start: 0, end: trend.length, zoomed: false };

  function drawCandle() {
    if (!hasOHLC) return;
    var slice = trend.slice(candleState.start, candleState.end);
    if (!slice.length) return;
    var c = setup('candleChart', 360); if (!c) return;
    var ctx = c.ctx, W = c.w, H = c.h;
    var pad = { t: 30, r: 50, b: 50, l: 65 };
    var cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;
    var n = slice.length;

    var allLow = [], allHigh = [];
    slice.forEach(function(d) { if (d.low !== null) allLow.push(d.low); if (d.high !== null) allHigh.push(d.high); });
    var mn = niceMin(Math.min.apply(null, allLow) * 0.995);
    var mx = niceMax(Math.max.apply(null, allHigh) * 1.005);
    var range = mx - mn || 1;
    var barW = Math.max(3, Math.min(20, (cw / n) * 0.7));
    var step = cw / (n || 1);

    ctx.clearRect(0, 0, W, H);
    drawGrid(ctx, pad, W, H, mn, mx, 5);

    var pts = [];
    slice.forEach(function(d, i) {
      var cx = pad.l + step * i + step / 2;
      var o = d.open !== null ? d.open : d.close;
      var hi = d.high !== null ? d.high : Math.max(o, d.close);
      var lo = d.low !== null ? d.low : Math.min(o, d.close);
      var cl = d.close;

      var yHi = pad.t + ch - ((hi - mn) / range * ch);
      var yLo = pad.t + ch - ((lo - mn) / range * ch);
      var yO = pad.t + ch - ((o - mn) / range * ch);
      var yC = pad.t + ch - ((cl - mn) / range * ch);

      var bullish = cl >= o;
      var color = bullish ? '#22c55e' : '#ef4444';

      // Wick line
      ctx.strokeStyle = color; ctx.lineWidth = 1;
      ctx.beginPath(); ctx.moveTo(cx, yHi); ctx.lineTo(cx, yLo); ctx.stroke();

      // Body
      var bodyTop = Math.min(yO, yC);
      var bodyH = Math.max(1, Math.abs(yO - yC));
      ctx.fillStyle = bullish ? '#22c55e' : '#ef4444';
      ctx.fillRect(cx - barW / 2, bodyTop, barW, bodyH);
      if (!bullish) {
        ctx.strokeStyle = '#ef4444'; ctx.lineWidth = 1;
        ctx.strokeRect(cx - barW / 2, bodyTop, barW, bodyH);
      }

      pts.push({
        x: cx, y: bodyTop,
        label: '<strong>' + d.time + '</strong><br>Open: ' + fmt(o) + '<br>High: ' + fmt(hi) + '<br>Low: ' + fmt(lo) + '<br>Close: ' + fmt(cl) + (d.volume ? '<br>Vol: ' + d.volume.toLocaleString() : '')
      });
    });

    drawXLabels(ctx, slice, pad, W, H, step, step / 2);
    drawAxisLine(ctx, pad, W, H);
    drawZoomHint(ctx, pad, candleState.zoomed);

    ctx.fillStyle = '#22c55e'; ctx.font = 'bold 11px ' + FONT; ctx.textAlign = 'left';
    ctx.fillText('Bullish', pad.l + 140, pad.t - 10);
    ctx.fillStyle = '#ef4444';
    ctx.fillText('Bearish', pad.l + 200, pad.t - 10);

    addTip('candleChart', 'candleTip', pts);
  }
  drawCandle();
  addZoom('candleChart', candleState, trend.length, drawCandle);

  /* ==============================================================
     2. PRICE TREND + MOVING AVERAGES
     ============================================================== */
  if (!trend.length) {
    var tsec = document.getElementById('trendSection');
    if (tsec) tsec.style.display = 'none';
  }

  var ma5 = calcMA(trend, 5);
  var ma20 = calcMA(trend, 20);
  var ma60 = calcMA(trend, 60);

  var trendState = { start: 0, end: trend.length, zoomed: false };

  function drawTrend() {
    var slice = trend.slice(trendState.start, trendState.end);
    if (!slice.length) return;
    var sliceMA5 = ma5.slice(trendState.start, trendState.end);
    var sliceMA20 = ma20.slice(trendState.start, trendState.end);
    var sliceMA60 = ma60.slice(trendState.start, trendState.end);

    var c = setup('trendChart', 340); if (!c) return;
    var ctx = c.ctx, W = c.w, H = c.h;
    var pad = { t: 30, r: 50, b: 50, l: 65 };
    var cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;
    var n = slice.length, step = cw / (n - 1 || 1);

    // Compute Y range from all visible data
    var allVals = slice.map(function(d) { return d.close; });
    [sliceMA5, sliceMA20, sliceMA60].forEach(function(arr) {
      arr.forEach(function(v) { if (v !== null) allVals.push(v); });
    });
    var mn = Math.min.apply(null, allVals) * 0.98;
    var mx = niceMax(Math.max.apply(null, allVals) * 1.02);
    if (mn < 0) mn = 0;
    var range = mx - mn || 1;

    function yPos(v) { return pad.t + ch - ((v - mn) / range * ch); }

    ctx.clearRect(0, 0, W, H);
    drawGrid(ctx, pad, W, H, mn, mx, 5);

    // Area fill under close line
    ctx.beginPath(); ctx.moveTo(pad.l, pad.t + ch);
    for (var i = 0; i < n; i++) ctx.lineTo(pad.l + step * i, yPos(slice[i].close));
    ctx.lineTo(pad.l + step * (n - 1), pad.t + ch); ctx.closePath();
    var g = ctx.createLinearGradient(0, pad.t, 0, pad.t + ch);
    g.addColorStop(0, 'rgba(74,124,250,0.18)'); g.addColorStop(1, 'rgba(74,124,250,0.01)');
    ctx.fillStyle = g; ctx.fill();

    // Close price line
    ctx.beginPath();
    for (var i = 0; i < n; i++) { var x = pad.l + step * i, y = yPos(slice[i].close); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }
    ctx.strokeStyle = '#4a7cfa'; ctx.lineWidth = 2.5; ctx.stroke();

    // MA lines
    function drawMA(arr, color) {
      ctx.beginPath(); var started = false;
      for (var i = 0; i < n; i++) {
        if (arr[i] === null) { started = false; continue; }
        var x = pad.l + step * i, y = yPos(arr[i]);
        if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
      }
      ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.stroke();
    }
    drawMA(sliceMA5, '#f59e42');
    drawMA(sliceMA20, '#48bb78');
    drawMA(sliceMA60, '#9f7aea');

    drawXLabels(ctx, slice, pad, W, H, step, 0);
    drawAxisLine(ctx, pad, W, H);
    drawZoomHint(ctx, pad, trendState.zoomed);

    // Tooltip data
    var pts = slice.map(function(d, i) {
      var x = pad.l + step * i, y = yPos(d.close);
      var lbl = '<strong>' + d.time + '</strong><br>Close: ' + fmt(d.close);
      if (sliceMA5[i] !== null) lbl += '<br>MA5: ' + fmt(sliceMA5[i]);
      if (sliceMA20[i] !== null) lbl += '<br>MA20: ' + fmt(sliceMA20[i]);
      if (sliceMA60[i] !== null) lbl += '<br>MA60: ' + fmt(sliceMA60[i]);
      return { x: x, y: y, label: lbl };
    });
    addTip('trendChart', 'trendTip', pts);
  }
  drawTrend();
  addZoom('trendChart', trendState, trend.length, drawTrend);

  /* ==============================================================
     3. BOLLINGER BANDS
     ============================================================== */
  if (trend.length < 20) {
    var bsec = document.getElementById('bollingerSection');
    if (bsec) bsec.style.display = 'none';
  }

  var bbMA = calcMA(trend, 20);
  var bbStd = calcStdDev(trend, 20, bbMA);

  var bbState = { start: 0, end: trend.length, zoomed: false };

  function drawBB() {
    if (trend.length < 20) return;
    var slice = trend.slice(bbState.start, bbState.end);
    if (!slice.length) return;
    var sliceBBMA = bbMA.slice(bbState.start, bbState.end);
    var sliceBBStd = bbStd.slice(bbState.start, bbState.end);

    var c = setup('bbChart', 340); if (!c) return;
    var ctx = c.ctx, W = c.w, H = c.h;
    var pad = { t: 30, r: 50, b: 50, l: 65 };
    var cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;
    var n = slice.length, step = cw / (n - 1 || 1);

    // Compute Y range
    var allVals = [];
    for (var i = 0; i < n; i++) {
      allVals.push(slice[i].close);
      if (sliceBBMA[i] !== null && sliceBBStd[i] !== null) {
        allVals.push(sliceBBMA[i] + 2 * sliceBBStd[i]);
        allVals.push(sliceBBMA[i] - 2 * sliceBBStd[i]);
      }
    }
    var mn = Math.min.apply(null, allVals) * 0.98;
    var mx = niceMax(Math.max.apply(null, allVals) * 1.02);
    if (mn < 0) mn = 0;
    var range = mx - mn || 1;

    function yPos(v) { return pad.t + ch - ((v - mn) / range * ch); }

    ctx.clearRect(0, 0, W, H);
    drawGrid(ctx, pad, W, H, mn, mx, 5);

    // Shaded band area
    var upperPts = [], lowerPts = [];
    for (var i = 0; i < n; i++) {
      if (sliceBBMA[i] !== null && sliceBBStd[i] !== null) {
        var x = pad.l + step * i;
        upperPts.push({ x: x, y: yPos(sliceBBMA[i] + 2 * sliceBBStd[i]) });
        lowerPts.push({ x: x, y: yPos(sliceBBMA[i] - 2 * sliceBBStd[i]) });
      }
    }
    if (upperPts.length > 1) {
      ctx.beginPath();
      ctx.moveTo(upperPts[0].x, upperPts[0].y);
      for (var i = 1; i < upperPts.length; i++) ctx.lineTo(upperPts[i].x, upperPts[i].y);
      for (var i = lowerPts.length - 1; i >= 0; i--) ctx.lineTo(lowerPts[i].x, lowerPts[i].y);
      ctx.closePath();
      ctx.fillStyle = 'rgba(159,122,234,0.15)'; ctx.fill();

      // Upper band line
      ctx.beginPath();
      ctx.moveTo(upperPts[0].x, upperPts[0].y);
      for (var i = 1; i < upperPts.length; i++) ctx.lineTo(upperPts[i].x, upperPts[i].y);
      ctx.strokeStyle = 'rgba(159,122,234,0.5)'; ctx.lineWidth = 1; ctx.stroke();

      // Lower band line
      ctx.beginPath();
      ctx.moveTo(lowerPts[0].x, lowerPts[0].y);
      for (var i = 1; i < lowerPts.length; i++) ctx.lineTo(lowerPts[i].x, lowerPts[i].y);
      ctx.strokeStyle = 'rgba(159,122,234,0.5)'; ctx.lineWidth = 1; ctx.stroke();
    }

    // MA20 center line
    ctx.beginPath(); var started = false;
    for (var i = 0; i < n; i++) {
      if (sliceBBMA[i] === null) { started = false; continue; }
      var x = pad.l + step * i, y = yPos(sliceBBMA[i]);
      if (!started) { ctx.moveTo(x, y); started = true; } else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = '#e53e3e'; ctx.lineWidth = 1.5; ctx.stroke();

    // Close price line
    ctx.beginPath();
    for (var i = 0; i < n; i++) { var x = pad.l + step * i, y = yPos(slice[i].close); if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y); }
    ctx.strokeStyle = '#4a7cfa'; ctx.lineWidth = 2; ctx.stroke();

    drawXLabels(ctx, slice, pad, W, H, step, 0);
    drawAxisLine(ctx, pad, W, H);
    drawZoomHint(ctx, pad, bbState.zoomed);

    // Tooltip
    var pts = slice.map(function(d, i) {
      var x = pad.l + step * i, y = yPos(d.close);
      var lbl = '<strong>' + d.time + '</strong><br>Close: ' + fmt(d.close);
      if (sliceBBMA[i] !== null) {
        lbl += '<br>MA20: ' + fmt(sliceBBMA[i]);
        if (sliceBBStd[i] !== null) {
          lbl += '<br>Upper: ' + fmt(sliceBBMA[i] + 2 * sliceBBStd[i]);
          lbl += '<br>Lower: ' + fmt(sliceBBMA[i] - 2 * sliceBBStd[i]);
        }
      }
      return { x: x, y: y, label: lbl };
    });
    addTip('bbChart', 'bbTip', pts);
  }
  drawBB();
  addZoom('bbChart', bbState, trend.length, drawBB);

  /* ==============================================================
     4. VOLUME-PRICE CORRELATION (Dual Y-axis)
     ============================================================== */
  if (!hasVolume) {
    var vsec = document.getElementById('volumeSection');
    if (vsec) vsec.style.display = 'none';
  }

  var volState = { start: 0, end: trend.length, zoomed: false };

  function drawVolume() {
    if (!hasVolume) return;
    var slice = trend.slice(volState.start, volState.end);
    if (!slice.length) return;
    var c = setup('volumeChart', 320); if (!c) return;
    var ctx = c.ctx, W = c.w, H = c.h;
    var pad = { t: 30, r: 60, b: 50, l: 65 };
    var cw = W - pad.l - pad.r, ch = H - pad.t - pad.b;
    var n = slice.length, step = cw / (n || 1);

    // Price range (left Y)
    var prices = slice.map(function(d) { return d.close; });
    var pMin = Math.min.apply(null, prices) * 0.98;
    var pMax = niceMax(Math.max.apply(null, prices) * 1.02);
    var pRange = pMax - pMin || 1;

    // Volume range (right Y)
    var volumes = slice.map(function(d) { return d.volume; });
    var vMax = niceMax(Math.max.apply(null, volumes) * 1.1);

    function yPrice(v) { return pad.t + ch - ((v - pMin) / pRange * ch); }
    function yVol(v) { return pad.t + ch - ((v / vMax) * ch); }

    ctx.clearRect(0, 0, W, H);

    // Left Y grid (price)
    ctx.strokeStyle = CC.grid; ctx.lineWidth = 1;
    for (var i = 0; i <= 5; i++) {
      var y = pad.t + ch - (ch * i / 5);
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W - pad.r, y); ctx.stroke();
      ctx.fillStyle = '#4a7cfa'; ctx.font = '11px ' + FONT; ctx.textAlign = 'right';
      ctx.fillText(fmt(pMin + pRange * i / 5), pad.l - 10, y + 4);
    }

    // Right Y labels (volume)
    for (var i = 0; i <= 5; i++) {
      var y = pad.t + ch - (ch * i / 5);
      ctx.fillStyle = '#48bb78'; ctx.font = '11px ' + FONT; ctx.textAlign = 'left';
      ctx.fillText(fmt(vMax * i / 5), W - pad.r + 8, y + 4);
    }

    // Volume bars
    var barW = Math.max(2, step * 0.6);
    slice.forEach(function(d, i) {
      var x = pad.l + step * i + (step - barW) / 2;
      var bh = (d.volume / vMax) * ch;
      var y = pad.t + ch - bh;
      // Color by price direction
      var prevClose = i > 0 ? slice[i - 1].close : d.close;
      var bullish = d.close >= prevClose;
      ctx.fillStyle = bullish ? 'rgba(34,197,94,0.4)' : 'rgba(239,68,68,0.4)';
      ctx.fillRect(x, y, barW, bh);
    });

    // Price line (close)
    ctx.beginPath();
    for (var i = 0; i < n; i++) {
      var x = pad.l + step * i + step / 2, y = yPrice(slice[i].close);
      if (i === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.strokeStyle = '#4a7cfa'; ctx.lineWidth = 2.5; ctx.stroke();

    drawXLabels(ctx, slice, pad, W, H, step, step / 2);
    drawAxisLine(ctx, pad, W, H);
    drawZoomHint(ctx, pad, volState.zoomed);

    // Axis labels
    ctx.fillStyle = '#4a7cfa'; ctx.font = 'bold 11px ' + FONT; ctx.textAlign = 'left';
    ctx.fillText('Price (left)', pad.l + 140, pad.t - 10);
    ctx.fillStyle = '#48bb78';
    ctx.fillText('Volume (right)', pad.l + 230, pad.t - 10);

    // Tooltip
    var pts = slice.map(function(d, i) {
      var x = pad.l + step * i + step / 2, y = yPrice(d.close);
      return { x: x, y: y, label: '<strong>' + d.time + '</strong><br>Close: ' + fmt(d.close) + '<br>Volume: ' + d.volume.toLocaleString() };
    });
    addTip('volumeChart', 'volumeTip', pts);
  }
  drawVolume();
  addZoom('volumeChart', volState, trend.length, drawVolume);

  /* ---- 테마 토글: 클래스 전환 + 저장 + 차트 중립색 갱신 + 전체 재그리기 ---- */
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) themeBtn.onclick = function () {
    var el = document.documentElement;
    el.classList.toggle('theme-light');
    try { localStorage.setItem('neoReportTheme2', el.classList.contains('theme-light') ? 'light' : 'dark'); } catch (e) {}
    applyChartTheme();
    drawCandle(); drawTrend(); drawBB(); drawVolume();
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
