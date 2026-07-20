---
compute: vibration
guide: |
  RMS/Peak/Crest Factor 수치를 반드시 참조해 설비 상태를 ISO 10816 기준으로 해석하라. 상태 수준에 맞는 톤을 스스로 판단(양호=예방관리 유지, 위험=즉시 조치).
  - Crest Factor로 충격성 진동 판단(3 이하 정상, 3~6 주의, 6 이상 충격성)
  - FFT 주파수 대역의 특이 피크 → 베어링/기어/불균형 등 고장 모드 추정
  - 롤업 추이로 시간에 따른 악화/안정 판단
  - recommendations는 설비 관리자의 점검/교체/모니터링 조치로 작성
---
# 진동 데이터 HTML 분석 리포트 템플릿

진동 데이터(가속도, 속도, 변위 등)에 적합한 HTML 분석 리포트 템플릿입니다.
태그 선택 드롭다운, Raw Waveform, ISO 10816 게이지, RMS/P2P/Crest Factor 추이, FFT 스펙트럼을 포함합니다.

## 디자인
**금융 리포트(finance-report-templates.md)와 동일한 Neo Web UI 디자인 체계**(2026-07-14 이식) — `src/design-system/tokens/_colors.scss` 기준.
- **기본 다크 모드**, 우상단 토글로 다크 전환(localStorage `neoReportTheme2` 저장, light 저장 시에만 head 스크립트가 `theme-light` 부착)
- 폰트 Pretendard(UI) / D2Coding(숫자·코드), 레터헤드 헤더(로고 base64 인라인 — 단일 HTML로 이동 가능해야 하므로 외부 참조 금지)
- KPI 카드 → **스펙 패널**(세로 구분선), 섹션 타이틀 = `| bar`, 차트 섹션은 `section-chart` 톤
- ⚠️ canvas는 CSS 변수를 못 읽으므로 **중립색(격자/축)은 JS `CC` 팔레트**로 복제 — 테마 토글 시 `applyChartTheme()` 후 `switchTag()`로 전체 재그리기. 시리즈 색(wave/rms/p2p/crest/fft)과 ISO 심각도 상태색·기준선 색은 두 모드 공용.

## 변수 설명
| 변수 | 설명 | 채우는 주체 |
|------|------|------------|
| {TABLE} | 테이블명 | SQL 결과 |
| {GENERATED_DATE} | 리포트 생성 일시 | 자동 삽입 |
| {TAG_COUNT} | 태그 수 | SQL 결과 |
| {DATA_COUNT} | 총 데이터 건수 | SQL 결과 |
| {TIME_RANGE} | 데이터 시간 범위 | SQL 결과 |
| {TAG_STATS_ROWS} | 태그별 통계 `<tr>` 행 | SQL → 자동 변환 |
| {TAG_LIST_JSON} | 태그 목록 JSON 배열 | SQL → 자동 변환 |
| {PER_TAG_DATA_JSON} | 태그별 raw+rollup+stats JSON | SQL → 자동 계산 |
| {ROLLUP_LABEL} | ROLLUP 단위 라벨 | 자동 계산 |
| {ANALYSIS} | 심층 분석 | LLM 생성 |
| {RECOMMENDATIONS} | 종합 소견 및 권고 | LLM 생성 |

## ROLLUP 시간 단위 자동 선택 기준

데이터 시간 범위에 따라 자동으로 적절한 ROLLUP 단위가 선택됩니다.

| 데이터 시간 범위 | ROLLUP 단위 | 라벨 |
|-----------------|------------|------|
| 1시간 미만 | sec | 초별 |
| 1시간 ~ 48시간 | min | 분별 |
| 48시간 ~ 30일 | hour | 시간별 |
| 30일 ~ 1년 | day | 일별 |
| 1년 이상 | month | 월별 |

시간 범위를 알 수 없는 경우 기본값은 `min`(분별)입니다.

---

### R-2-vibration. 진동 데이터 종합 분석 리포트
용도: 진동 데이터(가속도, 속도, 변위 등)의 원시 파형, RMS/Peak-to-Peak/Crest Factor 추이, FFT 주파수 스펙트럼, ISO 10816 심각도를 차트와 함께 보여주는 심층 분석 보고서입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TABLE} 진동 데이터 분석 리포트</title>
<!-- 기본 = 다크(:root 토큰 그대로). 저장된 선택이 라이트일 때만 theme-light 부착(head 동기 실행 — 플래시 없음). -->
<script>try{if(localStorage.getItem('neoReportTheme2')==='light')document.documentElement.classList.add('theme-light');}catch(e){}</script>
<style>
  /* Neo Web UI design tokens (src/design-system/tokens/_colors.scss) — 금융 리포트와 동일 체계 */
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

  /* Tag selector */
  .tag-select {
    padding: 8px 14px; border-radius: var(--radius-sm); border: 1px solid var(--border-default);
    font-size: 14px; font-weight: 600; color: var(--text-primary); background: var(--bg-elevated);
    cursor: pointer; margin-left: 16px; min-width: 160px;
  }
  .tag-select:focus { outline: none; border-color: var(--primary); }

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
      <div class="eyebrow">Vibration Analysis Report</div>
      <h1><span class="hl">{TABLE}</span> 진동 데이터 분석 리포트</h1>
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

  <!-- Tag Selector -->
  <div class="section">
    <div class="section-title">
      <span class="bar"></span> 분석 태그 선택
      <select id="tagSelect" class="tag-select" onchange="switchTag(this.value)"></select>
    </div>
  </div>

  <!-- Raw Waveform -->
  <div class="section section-chart">
    <div class="section-title"><span class="bar"></span> <span id="waveTitle">원시 파형 (Raw Waveform)</span>
      <span class="chart-badge"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="5 9 2 12 5 15"></polyline><polyline points="9 5 12 2 15 5"></polyline><polyline points="15 19 12 22 9 19"></polyline><polyline points="19 9 22 12 19 15"></polyline><line x1="2" y1="12" x2="22" y2="12"></line><line x1="12" y1="2" x2="12" y2="22"></line></svg>확대·이동</span>
      <span class="nav-hint"><b>휠</b> 확대·축소 &middot; <b>드래그</b> 좌우 이동 &middot; <b>더블클릭</b> 되돌리기</span>
    </div>
    <div class="chart-full chart-wrap"><canvas id="waveChart" height="300"></canvas><div class="crosshair" id="waveCross"><div class="crosshair-v"></div></div><div class="tooltip" id="waveTip"></div></div>
  </div>

  <!-- Vibration Severity -->
  <div class="section">
    <div id="severitySection"></div>
  </div>

  <!-- RMS Trend -->
  <div class="section section-chart">
    <div class="section-title"><span class="bar"></span> RMS 추이 ({ROLLUP_LABEL} 평균)</div>
    <div class="chart-full chart-wrap"><canvas id="rmsChart" height="250"></canvas><div class="tooltip" id="rmsTip"></div></div>
  </div>

  <!-- Peak-to-Peak Trend -->
  <div class="section section-chart">
    <div class="section-title"><span class="bar"></span> Peak-to-Peak 추이 ({ROLLUP_LABEL})</div>
    <div class="chart-full chart-wrap"><canvas id="p2pChart" height="250"></canvas><div class="tooltip" id="p2pTip"></div></div>
  </div>

  <!-- Crest Factor Trend -->
  <div class="section section-chart">
    <div class="section-title"><span class="bar"></span> Crest Factor 추이 ({ROLLUP_LABEL})</div>
    <div class="chart-full chart-wrap"><canvas id="crestChart" height="250"></canvas><div class="tooltip" id="crestTip"></div></div>
  </div>

  <!-- FFT Spectrum -->
  <div class="section section-chart">
    <div class="section-title"><span class="bar"></span> FFT 주파수 스펙트럼 (0.2 Hz 해상도)</div>
    <div class="chart-full chart-wrap"><canvas id="fftChart" height="300"></canvas><div class="tooltip" id="fftTip"></div></div>
  </div>

  <!-- Tag Stats Table -->
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
  var tagList = {TAG_LIST_JSON};
  var perTag = {PER_TAG_DATA_JSON};
  var currentTag = tagList[0] || '';

  var dpr = window.devicePixelRatio || 1;

  /* ---- 차트 중립색(격자/축) — canvas는 CSS 변수를 못 읽으므로 여기서 테마별로 복제(_colors.scss와 동일 값).
          시리즈 색(wave/rms/p2p/crest/fft)과 ISO 기준선 색은 두 모드 공용이라 바꾸지 않는다. ---- */
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

  function setup(id,h){var c=document.getElementById(id);if(!c)return null;var w=c.parentElement.getBoundingClientRect().width;c.width=w*dpr;c.height=h*dpr;c.style.width=w+'px';c.style.height=h+'px';var ctx=c.getContext('2d');ctx.scale(dpr,dpr);return{ctx:ctx,w:w,h:h,canvas:c};}
  function niceMax(v){if(v<=0)return 1;var p=Math.pow(10,Math.floor(Math.log10(v)));return Math.ceil(v/p)*p;}
  function fmt(v){if(Math.abs(v)>=10000)return(v/1000).toFixed(1)+'K';if(Math.abs(v)>=100)return v.toFixed(1);if(Math.abs(v)>=1)return v.toFixed(2);return v.toFixed(4);}

  function addTip(canvasId,tipId,pts){
    var cv=document.getElementById(canvasId),tip=document.getElementById(tipId);
    if(!cv||!tip||!pts.length)return;
    var cross=document.getElementById(canvasId.replace('Chart','Cross'));
    cv.style.cursor='crosshair';
    cv.onmousemove=function(e){
      var r=cv.getBoundingClientRect(),mx=e.clientX-r.left;
      var best=null,bd=Infinity;
      pts.forEach(function(p){var d=Math.abs(p.x-mx);if(d<bd){bd=d;best=p;}});
      if(best&&bd<50){
        tip.innerHTML=best.label;tip.style.display='block';
        var tx=best.x+14;if(tx+160>r.width)tx=best.x-160;
        tip.style.left=tx+'px';tip.style.top=Math.max(4,best.y-24)+'px';
        if(cross){cross.style.display='block';cross.querySelector('.crosshair-v').style.left=best.x+'px';}
      }else{tip.style.display='none';if(cross)cross.style.display='none';}
    };
    cv.onmouseleave=function(){tip.style.display='none';if(cross)cross.style.display='none';};
  }

  // --- Scroll zoom helper (reusable for all charts) ---
  var zoomHandlers={};
  function addZoom(canvasId,fullLen,drawFn){
    var cv=document.getElementById(canvasId);if(!cv)return;
    var st={s:0,e:fullLen};
    if(zoomHandlers[canvasId]){
      cv.removeEventListener('wheel',zoomHandlers[canvasId].w);
      cv.removeEventListener('dblclick',zoomHandlers[canvasId].d);
      cv.removeEventListener('mousedown',zoomHandlers[canvasId].md);
      cv.removeEventListener('mousemove',zoomHandlers[canvasId].mm);
      cv.removeEventListener('mouseup',zoomHandlers[canvasId].mu);
      cv.removeEventListener('mouseleave',zoomHandlers[canvasId].ml);
    }
    function onWheel(ev){
      ev.preventDefault();
      var rect=cv.getBoundingClientRect(),mx=ev.clientX-rect.left;
      var cw=rect.width-100,n=st.e-st.s;
      var ratio=Math.max(0,Math.min(1,(mx-70)/cw));
      var zf=ev.deltaY>0?1.3:0.7,newN=Math.round(n*zf);
      if(newN<4)newN=4;
      if(newN>=fullLen){st.s=0;st.e=fullLen;drawFn(st.s,st.e);return;}
      var center=st.s+Math.round(n*ratio),ns=Math.round(center-newN*ratio);
      if(ns<0)ns=0;var ne=ns+newN;if(ne>fullLen){ne=fullLen;ns=ne-newN;}
      st.s=Math.max(0,ns);st.e=ne;drawFn(st.s,st.e);
    }
    function onDbl(){st.s=0;st.e=fullLen;drawFn(st.s,st.e);}
    var drag={active:false,startX:0,startS:0,startE:0};
    function onDown(ev){if(st.e-st.s>=fullLen)return;drag.active=true;drag.startX=ev.clientX;drag.startS=st.s;drag.startE=st.e;cv.style.cursor='grabbing';}
    function onMove(ev){if(!drag.active)return;var rect=cv.getBoundingClientRect(),cw=rect.width-100,n=drag.startE-drag.startS;var shift=Math.round(-(ev.clientX-drag.startX)/cw*n);var ns=drag.startS+shift,ne=drag.startE+shift;if(ns<0){ns=0;ne=n;}if(ne>fullLen){ne=fullLen;ns=fullLen-n;}st.s=ns;st.e=ne;drawFn(st.s,st.e);}
    function onUp(){drag.active=false;cv.style.cursor='crosshair';}
    cv.addEventListener('wheel',onWheel,{passive:false});
    cv.addEventListener('dblclick',onDbl);
    cv.addEventListener('mousedown',onDown);
    cv.addEventListener('mousemove',onMove);
    cv.addEventListener('mouseup',onUp);
    cv.addEventListener('mouseleave',onUp);
    zoomHandlers[canvasId]={w:onWheel,d:onDbl,md:onDown,mm:onMove,mu:onUp,ml:onUp};
  }

  // --- Populate dropdown ---
  var sel=document.getElementById('tagSelect');
  tagList.forEach(function(t){var o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o);});

  // --- Draw functions ---
  var colors={wave:'#667eea',rms:'#38b2ac',p2p:'#805ad5',crest:'#ed8936',fft:'#e53e3e'};

  function drawLineChart(canvasId,tipId,xLabels,yValues,color,height,refLines,tipLabels){
    var c=setup(canvasId,height);if(!c)return;
    var tl=tipLabels||xLabels;
    var ctx=c.ctx,W=c.w,H=c.h,pad={t:30,r:30,b:50,l:70};
    var cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
    var vals=yValues,n=vals.length;if(n<2)return;
    var mn=Math.min.apply(null,vals),mx=Math.max.apply(null,vals);
    var margin=(mx-mn)*0.1||1;mn-=margin;mx+=margin;
    var range=mx-mn||1,step=cw/(n-1);
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle=CC.grid;ctx.lineWidth=1;
    for(var i=0;i<=5;i++){var y=pad.t+ch-(ch*i/5);ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle=CC.axis;ctx.font='11px '+FONT;ctx.textAlign='right';ctx.fillText(fmt(mn+range*i/5),pad.l-10,y+4);}
    if(refLines){refLines.forEach(function(rl){var ry=pad.t+ch-((rl.val-mn)/range*ch);if(ry>pad.t&&ry<pad.t+ch){ctx.strokeStyle=rl.color;ctx.lineWidth=1;ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(pad.l,ry);ctx.lineTo(W-pad.r,ry);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle=rl.color;ctx.font='10px '+FONT;ctx.textAlign='left';ctx.fillText(rl.label,W-pad.r+4,ry+3);}});}
    ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);
    for(var i=0;i<n;i++)ctx.lineTo(pad.l+step*i,pad.t+ch-((vals[i]-mn)/range*ch));
    ctx.lineTo(pad.l+step*(n-1),pad.t+ch);ctx.closePath();
    var g=ctx.createLinearGradient(0,pad.t,0,pad.t+ch);g.addColorStop(0,color+'40');g.addColorStop(1,color+'05');ctx.fillStyle=g;ctx.fill();
    ctx.beginPath();for(var i=0;i<n;i++){var x=pad.l+step*i,y=pad.t+ch-((vals[i]-mn)/range*ch);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
    ctx.strokeStyle=color;ctx.lineWidth=2;ctx.stroke();
    // X-axis: deduplicated labels (skip if same as previous rendered)
    ctx.fillStyle=CC.axis;ctx.font='10px '+FONT;ctx.textAlign='center';
    var ls=Math.max(1,Math.floor(n/8)),lastLabel='';
    for(var i=0;i<n;i+=ls){if(xLabels[i]!==lastLabel){ctx.fillText(xLabels[i],pad.l+step*i,H-pad.b+18);lastLabel=xLabels[i];}}
    ctx.strokeStyle=CC.axisLine;ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);ctx.lineTo(W-pad.r,pad.t+ch);ctx.stroke();
    var pts=vals.map(function(v,i){var x=pad.l+step*i,y=pad.t+ch-((v-mn)/range*ch);return{x:x,y:y,label:'<strong>'+tl[i]+'</strong><br>'+fmt(v)};});
    addTip(canvasId,tipId,pts);
  }

  function drawBarChart(canvasId,tipId,xLabels,yValues,color,height,tipLabels){
    var c=setup(canvasId,height);if(!c)return;
    var tl=tipLabels||xLabels;
    var ctx=c.ctx,W=c.w,H=c.h,pad={t:20,r:30,b:50,l:70};
    var cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
    var n=yValues.length;if(n<1)return;
    var mx=niceMax(Math.max.apply(null,yValues)*1.1);
    var bw=Math.max(2,cw/n-2);
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle=CC.grid;ctx.lineWidth=1;
    for(var i=0;i<=4;i++){var y=pad.t+ch-(ch*i/4);ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle=CC.axis;ctx.font='11px '+FONT;ctx.textAlign='right';ctx.fillText(fmt(mx*i/4),pad.l-10,y+4);}
    var pts=[];
    yValues.forEach(function(v,i){var x=pad.l+(cw/n)*i,bh=(v/mx)*ch,y=pad.t+ch-bh;var g=ctx.createLinearGradient(0,y,0,pad.t+ch);g.addColorStop(0,color);g.addColorStop(1,color+'60');ctx.fillStyle=g;ctx.fillRect(x,y,bw,bh);pts.push({x:x+bw/2,y:y,label:'<strong>'+tl[i]+'</strong><br>'+fmt(v)});});
    // X-axis: deduplicated
    ctx.fillStyle=CC.axis;ctx.font='10px '+FONT;ctx.textAlign='center';
    var ls=Math.max(1,Math.floor(n/8)),lastLabel='';
    for(var i=0;i<n;i+=ls){if(xLabels[i]!==lastLabel){ctx.fillText(xLabels[i],pad.l+(cw/n)*i+bw/2,H-pad.b+18);lastLabel=xLabels[i];}}
    ctx.strokeStyle=CC.axisLine;ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);ctx.lineTo(W-pad.r,pad.t+ch);ctx.stroke();
    addTip(canvasId,tipId,pts);
  }

  // --- Severity Section (gauge + indicators combined) ---
  function drawSeverity(stats, table, tag){
    var el=document.getElementById('severitySection');if(!el)return;
    var sev=stats.severity||{};
    var grade=sev.grade||0;
    var zones=[
      {label:'Good',color:'#38a169',thresh:'< 1.12'},
      {label:'Warning',color:'#d69e2e',thresh:'1.12 - 2.8'},
      {label:'Danger',color:'#dd6b20',thresh:'2.8 - 7.1'},
      {label:'Critical',color:'#e53e3e',thresh:'> 7.1'}
    ];
    var z=zones[grade]||zones[0];
    var ind=sev.indicators||{};
    var thresholds={avg_rms:2.8,peak_rms:2.8,crest:3.0,trend:2.0};
    var unitLabels={avg_rms:' <span style="font-size:13px;font-weight:500;color:var(--text-muted);">mm/s</span>',peak_rms:' <span style="font-size:13px;font-weight:500;color:var(--text-muted);">mm/s</span>',crest:'',trend:''};
    var prefixes={avg_rms:'',peak_rms:'',crest:'',trend:'&times;'};
    var threshLabels={avg_rms:'기준 < 2.8',peak_rms:'기준 < 2.8',crest:'기준 < 3.0',trend:'기준 < &times;2.0'};
    var recoText={0:'정상 운전 유지',1:'모니터링 강화 권고',2:'점검 권고: 24시간 내',3:'즉시 정지 권고'};

    var h='';
    // Header
    h+='<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:18px;">';
    h+='<div style="font-size:16px;font-weight:600;color:var(--text-primary);display:flex;align-items:center;gap:8px;">';
    h+='<span style="color:'+z.color+';font-size:18px;">&#9888;</span> 진동 심각도 평가</div>';
    h+='<div style="font-size:13px;color:var(--text-muted);">설비 '+table+' &middot; '+tag+'</div>';
    h+='</div>';

    // Grade box
    h+='<div style="border:1px solid var(--border-faint);border-radius:12px;padding:20px 24px 14px;margin-bottom:14px;">';
    h+='<div style="display:flex;justify-content:space-between;align-items:flex-end;margin-bottom:14px;">';
    h+='<div>';
    h+='<div style="font-size:11px;color:var(--text-muted);margin-bottom:2px;font-weight:500;">종합 위험도</div>';
    h+='<span style="font-size:40px;font-weight:800;color:'+z.color+';line-height:1;letter-spacing:-1px;">'+z.label+'</span>';
    h+='</div>';
    h+='<div style="font-size:12px;color:var(--text-tertiary);font-weight:500;">'+recoText[grade]+'</div>';
    h+='</div>';
    // Bar
    h+='<div style="position:relative;height:30px;border-radius:6px;overflow:hidden;display:flex;border:1px solid var(--border-faint);">';
    zones.forEach(function(zn,i){
      var active=i===grade;
      var borderR=i<zones.length-1?'border-right:1px solid var(--border-faint);':'';
      h+='<div style="flex:1;background:'+(active?zn.color:'var(--bg-elevated)')+';display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:'+(active?'#fff':'var(--text-muted)')+';'+borderR+'">'+zn.label+'</div>';
    });
    h+='</div>';
    h+='<div style="display:flex;margin-top:3px;">';
    zones.forEach(function(zn){ h+='<div style="flex:1;text-align:center;font-size:10px;color:var(--text-muted);font-weight:400;">'+zn.thresh+'</div>'; });
    h+='</div>';
    h+='</div>';

    // 4 indicator cards
    var indItems=[
      {key:'avg_rms',l:'평균 RMS'},
      {key:'peak_rms',l:'피크 RMS'},
      {key:'crest',l:'Crest Factor'},
      {key:'trend',l:'변화율'}
    ];
    h+='<div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;">';
    indItems.forEach(function(it){
      var d=ind[it.key]||{};var g=d.grade||0;var c=zones[g]||zones[0];
      var val=d.value;var th=thresholds[it.key];
      var diff=val!=null?Math.abs(val-th).toFixed(2):'';
      var over=val>th;var arrowColor=over?'#e53e3e':'#38a169';var arrow=over?'&#9650;':'&#9660;';
      h+='<div style="padding:14px 14px;border:1px solid var(--border-faint);border-radius:10px;border-left:3px solid '+c.color+';">';
      h+='<div style="margin-bottom:8px;font-size:12px;font-weight:500;color:var(--text-secondary);">'+it.l;
      h+='<span style="display:inline-block;padding:1px 7px;border-radius:3px;font-size:9px;font-weight:700;letter-spacing:0.5px;color:#fff;background:'+c.color+';margin-left:6px;vertical-align:middle;">'+c.label.toUpperCase()+'</span></div>';
      h+='<div style="font-size:28px;font-weight:700;color:var(--text-primary);letter-spacing:-0.5px;margin-bottom:8px;">'+prefixes[it.key]+(val!=null?fmt(val):'-')+unitLabels[it.key]+'</div>';
      h+='<div style="display:flex;justify-content:space-between;align-items:center;font-size:11px;">';
      h+='<span style="color:var(--text-muted);font-weight:400;">'+threshLabels[it.key]+'</span>';
      if(val!=null) h+='<span style="color:'+arrowColor+';font-weight:600;">'+arrow+' '+diff+'</span>';
      h+='</div></div>';
    });
    h+='</div>';
    el.innerHTML=h;
  }

  // --- Switch tag (all charts with zoom) ---
  window.switchTag=function(tag){
    currentTag=tag;
    var d=perTag[tag];if(!d)return;
    document.getElementById('waveTitle').textContent='원시 파형 — '+tag;

    // --- Time label helpers ---
    // Axis: HH:MM only (minute granularity for clean display)
    function toHHMM(ms){var dt=new Date(ms);var h=dt.getHours(),m=dt.getMinutes();return(h<10?'0':'')+h+':'+(m<10?'0':'')+m;}
    // Rollup label "YYYY-MM-DD HH:MM:SS" → "HH:MM"
    function rollupToHHMM(t){var m=t.match(/(\d{2}:\d{2})/);return m?m[1]:t;}
    // Tooltip: full datetime with milliseconds
    function toFullTime(ms){var dt=new Date(ms);return dt.getFullYear()+'-'+z(dt.getMonth()+1)+'-'+z(dt.getDate())+' '+z(dt.getHours())+':'+z(dt.getMinutes())+':'+z(dt.getSeconds())+'.'+String(dt.getMilliseconds()).padStart(3,'0');}
    function z(n){return n<10?'0'+n:''+n;}

    // --- Waveform ---
    var raw=d.raw||{};
    var wTimes=raw.times_ms||[],wVals=raw.values||[];
    if(wVals.length>=2){
      var wAxis=wTimes.map(toHHMM);
      var wTip=wTimes.map(toFullTime);
      drawLineChart('waveChart','waveTip',wAxis,wVals,colors.wave,300,null,wTip);
      addZoom('waveChart',wVals.length,function(s,e){
        drawLineChart('waveChart','waveTip',wAxis.slice(s,e),wVals.slice(s,e),colors.wave,300,null,wTip.slice(s,e));
      });
    }

    // --- Rollup data ---
    var rollup=d.rollup||[];
    var tFull=rollup.map(function(r){return r.t;});
    var tAxis=tFull.map(rollupToHHMM);
    var rmsVals=rollup.map(function(r){return r.rms||0;});
    var p2pVals=rollup.map(function(r){return r.p2p||0;});
    var crestVals=rollup.map(function(r){return r.crest||0;});
    var rmsRef=[{val:1.12,color:'#48bb78',label:'Good'},{val:2.8,color:'#ecc94b',label:'Satisfactory'},{val:7.1,color:'#ed8936',label:'Unsatisfactory'}];
    var crestRef=[{val:3.0,color:'#a0aec0',label:'CF=3 (sin)'}];

    // --- RMS Trend + zoom ---
    drawLineChart('rmsChart','rmsTip',tAxis,rmsVals,colors.rms,250,rmsRef,tFull);
    addZoom('rmsChart',tAxis.length,function(s,e){
      drawLineChart('rmsChart','rmsTip',tAxis.slice(s,e),rmsVals.slice(s,e),colors.rms,250,rmsRef,tFull.slice(s,e));
    });

    // --- P2P Trend + zoom ---
    drawBarChart('p2pChart','p2pTip',tAxis,p2pVals,colors.p2p,250,tFull);
    addZoom('p2pChart',tAxis.length,function(s,e){
      drawBarChart('p2pChart','p2pTip',tAxis.slice(s,e),p2pVals.slice(s,e),colors.p2p,250,tFull.slice(s,e));
    });

    // --- Crest Factor + zoom ---
    drawLineChart('crestChart','crestTip',tAxis,crestVals,colors.crest,250,crestRef,tFull);
    addZoom('crestChart',tAxis.length,function(s,e){
      drawLineChart('crestChart','crestTip',tAxis.slice(s,e),crestVals.slice(s,e),colors.crest,250,crestRef,tFull.slice(s,e));
    });

    // --- FFT (server-computed, full range) ---
    var fftData=d.fft;
    if(fftData&&fftData.freqs&&fftData.freqs.length>0){
      var fLabels=fftData.freqs.map(function(f){return f>=1000?(f/1000).toFixed(1)+'KHz':f.toFixed(1)+'Hz';});
      var fMags=fftData.mags;
      var fTip=fftData.freqs.map(function(f){return f.toFixed(2)+' Hz';});
      drawLineChart('fftChart','fftTip',fLabels,fMags,colors.fft,300,null,fTip);
      addZoom('fftChart',fMags.length,function(s,e){
        drawLineChart('fftChart','fftTip',fLabels.slice(s,e),fMags.slice(s,e),colors.fft,300,null,fTip.slice(s,e));
      });
    } else {
      var fc=document.getElementById('fftChart');if(fc){var fctx=fc.getContext('2d');fctx.clearRect(0,0,fc.width,fc.height);fctx.fillStyle=CC.hint;fctx.font='14px '+FONT;fctx.textAlign='center';fctx.fillText('FFT 데이터 없음',fc.width/2,fc.height/2);}
    }

    // --- Severity Section ---
    var stats=d.stats||{};
    drawSeverity(stats, '{TABLE}', tag);
  };

  // Initial render
  if(currentTag)switchTag(currentTag);

  /* ---- 테마 토글: 클래스 전환 + 저장 + 차트 중립색 갱신 + 전체 재그리기(switchTag가 모든 draw 함수를 다시 호출한다) ---- */
  var themeBtn = document.getElementById('themeBtn');
  if (themeBtn) themeBtn.onclick = function () {
    var el = document.documentElement;
    el.classList.toggle('theme-light');
    try { localStorage.setItem('neoReportTheme2', el.classList.contains('theme-light') ? 'light' : 'dark'); } catch (e) {}
    applyChartTheme();
    if (currentTag) switchTag(currentTag);
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
