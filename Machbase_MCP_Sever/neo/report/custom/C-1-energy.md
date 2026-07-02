---
# compute 미선언 = 제네릭(태그별 통계만). 빌트인 계산 재사용 시 'compute: vibration|driving|finance' 선언
guide: |
  태그별 통계(평균·최소·최대·건수)를 바탕으로 데이터 특성, 이상치, 추세를 해석하라. 데이터 수준에 맞는 톤으로.
  - recommendations는 데이터 도메인에 맞는 실무 조치로 작성
---
# 에너지 분석 커스텀 리포트 템플릿 (C-2-energy)

`neo/report/custom/`에 드롭하는 커스텀 리포트 템플릿 예시입니다. **고유 주제(slug) `energy`** 를 써서 빌트인(general/finance/vibration/driving)과 겹치지 않습니다.

쿼리에 주제 키워드("에너지" 또는 "energy")가 있으면 ollama도 이 커스텀을 자동 선택합니다(쿼리-라우팅) — 빌트인보다 우선. 이게 커스텀의 의도된 동작입니다.

> 💡 새 커스텀은 **고객이 실제로 요청할 고유 주제**로 만드세요(예: `C-3-weather`, `C-4-quality`). 중립/일반어(sample, report, 분석, 데이터 등)는 라우팅 stopword라 자동 선택되지 않습니다 — 그런 데모는 이름으로만 직접 선택됩니다.

제네릭 경로(kind=C-*)가 채워주는 placeholder만 사용합니다 — RMS/FFT 등 파생계산은 Phase 3(공유 카탈로그) 전까지 빈 값이므로 쓰지 않습니다.

## 변수 설명 (제네릭 placeholder 계약)
| 변수 | 설명 | 채우는 주체 |
|------|------|------------|
| {TABLE} | 테이블명 | SQL 결과 |
| {GENERATED_DATE} | 리포트 생성 일시 | 자동 삽입 |
| {TAG_COUNT} | 태그 수 | SQL 결과 |
| {DATA_COUNT} | 총 데이터 건수 | SQL 결과 |
| {TIME_RANGE} | 데이터 시간 범위 | SQL 결과 |
| {TAG_STATS_ROWS} | 태그별 통계 `<tr>` 행 | SQL → 자동 변환 |
| {CHART_DATA_JSON} | 태그별 통계 JSON `[{name,count,avg,min,max}]` | SQL → 자동 변환 |
| {ANALYSIS} | 심층 분석 | LLM 생성 |
| {RECOMMENDATIONS} | 종합 소견 및 권고 | LLM 생성 |

---

### C-1-energy. 에너지 분석 리포트
용도: 고유 주제(energy) 커스텀 예시 / 쿼리-라우팅 데모. 태그별 통계 막대차트 + 통계 테이블 + AI 분석. 슬러그/제목 키워드(energy/에너지)로 라우팅됨.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TABLE} 커스텀 분석 리포트</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', 'Malgun Gothic', sans-serif; background: #f0fdfa; color: #134e4a; line-height: 1.7; }
  .page { max-width: 1000px; margin: 0 auto; padding: 40px 32px; }

  .report-header { background: linear-gradient(135deg, #0f766e 0%, #0d9488 55%, #14b8a6 100%); color: #fff; padding: 44px 40px; border-radius: 16px; margin-bottom: 28px; position: relative; overflow: hidden; }
  .report-header h1 { font-size: 30px; font-weight: 700; margin-bottom: 8px; }
  .report-header .subtitle { font-size: 15px; opacity: 0.85; margin-bottom: 18px; }
  .report-header .meta-row { display: flex; gap: 24px; font-size: 13px; opacity: 0.75; flex-wrap: wrap; }
  .custom-badge { display: inline-block; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.35); color: #fff; font-size: 12px; font-weight: 700; padding: 5px 12px; border-radius: 999px; letter-spacing: 0.5px; margin-bottom: 14px; }

  .section { background: #fff; border-radius: 12px; box-shadow: 0 1px 4px rgba(13,148,136,0.10); padding: 30px; margin-bottom: 24px; }
  .section-title { font-size: 17px; font-weight: 700; color: #0f766e; margin-bottom: 18px; display: flex; align-items: center; gap: 10px; }
  .section-title .icon { width: 30px; height: 30px; border-radius: 8px; background: #ccfbf1; color: #0f766e; display: flex; align-items: center; justify-content: center; font-size: 15px; }

  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }
  .kpi-card { background: linear-gradient(135deg, #0d9488 0%, #115e59 100%); border-radius: 12px; padding: 18px; color: #fff; text-align: center; }
  .kpi-card .kpi-label { font-size: 11px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 6px; }
  .kpi-card .kpi-value { font-size: 22px; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; border-radius: 8px; overflow: hidden; }
  thead th { background: #134e4a; color: #fff; font-weight: 600; padding: 13px 16px; text-align: left; }
  tbody td { padding: 11px 16px; border-bottom: 1px solid #e6fffa; }
  tbody tr:hover { background: #f0fdfa; }
  tbody tr:last-child td { border-bottom: none; }
  .num { text-align: right; font-variant-numeric: tabular-nums; font-family: 'Consolas', 'Menlo', monospace; }

  .analysis-content { color: #334155; font-size: 15px; line-height: 1.9; }
  .analysis-content strong { color: #0f766e; font-weight: 700; }
  .analysis-content ul, .analysis-content ol { margin: 12px 0 16px 24px; }
  .analysis-content li { margin-bottom: 10px; }
  .analysis-content li::marker { color: #0d9488; font-weight: 700; }

  .report-footer { text-align: center; padding: 22px; color: #5eead4; font-size: 12px; border-top: 1px solid #ccfbf1; margin-top: 10px; }
  @media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } .page { padding: 16px; } }
</style>
</head>
<body>
<div class="page">

  <div class="report-header">
    <div class="custom-badge">&#129513; 커스텀 템플릿 · C-2-energy</div>
    <h1>{TABLE} 에너지 분석 리포트</h1>
    <div class="subtitle">Machbase Neo · 에너지 분석 커스텀 리포트</div>
    <div class="meta-row">
      <span>&#128197; {GENERATED_DATE}</span>
      <span>&#128202; {TAG_COUNT}개 태그 · {DATA_COUNT}건</span>
      <span>&#9200; {TIME_RANGE}</span>
    </div>
  </div>

  <div class="section" style="background:transparent;box-shadow:none;padding:0;margin-bottom:24px;">
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-label">테이블</div><div class="kpi-value">{TABLE}</div></div>
      <div class="kpi-card"><div class="kpi-label">태그 수</div><div class="kpi-value">{TAG_COUNT}</div></div>
      <div class="kpi-card"><div class="kpi-label">데이터 건수</div><div class="kpi-value">{DATA_COUNT}</div></div>
      <div class="kpi-card"><div class="kpi-label">분석 기간</div><div class="kpi-value">{TIME_RANGE}</div></div>
    </div>
  </div>

  <!-- Per-tag max bar chart (CHART_DATA_JSON) -->
  <div class="section">
    <div class="section-title"><div class="icon">&#128200;</div> 태그별 최댓값</div>
    <canvas id="barChart" style="display:block;width:100%;"></canvas>
  </div>

  <!-- Tag stats table -->
  <div class="section">
    <div class="section-title"><div class="icon">&#128202;</div> 태그별 통계 요약</div>
    <div style="max-height:400px;overflow-y:auto;border-radius:8px;">
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
    <div class="section-title"><div class="icon">&#128270;</div> 심층 분석</div>
    <div class="analysis-content">{ANALYSIS}</div>
  </div>

  <!-- Recommendations -->
  <div class="section">
    <div class="section-title"><div class="icon">&#128161;</div> 종합 소견 및 권고사항</div>
    <div class="analysis-content">{RECOMMENDATIONS}</div>
  </div>

  <div class="report-footer">&#129513; 커스텀 템플릿(C-2-energy)으로 생성되었습니다.</div>
</div>

<script>
(function(){
  var raw = {CHART_DATA_JSON};
  var stats = (raw || []).map(function(d){ return { name: d.name||d.tag||'', max: Number(d.max)||0 }; });
  var cv = document.getElementById('barChart');
  if (!cv || !stats.length) { if (cv) cv.style.display='none'; return; }
  var dpr = window.devicePixelRatio || 1;
  var w = cv.parentElement.getBoundingClientRect().width;
  var h = 300;
  cv.width = w*dpr; cv.height = h*dpr; cv.style.height = h+'px';
  var ctx = cv.getContext('2d'); ctx.scale(dpr, dpr);
  var pad = { l: 60, r: 16, t: 16, b: 52 };
  var cw = w - pad.l - pad.r, ch = h - pad.t - pad.b;
  var maxV = Math.max.apply(null, stats.map(function(s){ return s.max; })); if (maxV <= 0) maxV = 1;
  ctx.font = '11px sans-serif';
  for (var g = 0; g <= 4; g++) {
    var y = pad.t + ch - (ch * g / 4);
    ctx.strokeStyle = '#e6fffa'; ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(pad.l + cw, y); ctx.stroke();
    ctx.fillStyle = '#64748b'; ctx.fillText((maxV * g / 4).toFixed(2), 6, y + 4);
  }
  ctx.strokeStyle = '#94a3b8'; ctx.beginPath(); ctx.moveTo(pad.l, pad.t); ctx.lineTo(pad.l, pad.t + ch); ctx.lineTo(pad.l + cw, pad.t + ch); ctx.stroke();
  var n = stats.length, gap = 14, bw = Math.max(10, (cw - gap * (n - 1)) / n);
  stats.forEach(function(s, i){
    var bh = ch * (s.max / maxV), x = pad.l + i * (bw + gap), y = pad.t + ch - bh;
    var grad = ctx.createLinearGradient(0, y, 0, pad.t + ch);
    grad.addColorStop(0, '#0d9488'); grad.addColorStop(1, '#99f6e4');
    ctx.fillStyle = grad; ctx.fillRect(x, y, bw, bh);
    ctx.fillStyle = '#334155'; ctx.textAlign = 'center';
    ctx.fillText(s.name.length > 9 ? s.name.slice(0, 8) + '…' : s.name, x + bw / 2, pad.t + ch + 18);
    ctx.fillStyle = '#0f766e'; ctx.fillText(s.max.toFixed(2), x + bw / 2, y - 6);
    ctx.textAlign = 'start';
  });
})();
</script>
</body>
</html>
```
