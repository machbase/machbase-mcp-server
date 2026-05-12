# 금융 데이터 HTML 분석 리포트 템플릿

금융 데이터(주가, 환율, 원자재 등)에 적합한 HTML 분석 리포트 템플릿입니다.

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

### R-1. 금융 데이터 종합 분석 리포트
용도: 금융 데이터(OHLCV)의 캔들스틱, 이동평균, 볼린저밴드, 거래량-가격 상관을 차트와 함께 보여주는 심층 분석 보고서입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{STOCK_NAME} 금융 데이터 분석 리포트</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', 'Malgun Gothic', sans-serif; background: #eef1f6; color: #1a202c; line-height: 1.7; }
  .page { max-width: 1000px; margin: 0 auto; padding: 40px 32px; }

  .report-header { background: linear-gradient(135deg, #0f2027 0%, #203a43 50%, #2c5364 100%); color: #fff; padding: 48px 40px; border-radius: 16px; margin-bottom: 32px; position: relative; overflow: hidden; }
  .report-header::after { content: ''; position: absolute; top: -50%; right: -20%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%); border-radius: 50%; }
  .report-header h1 { font-size: 32px; font-weight: 700; margin-bottom: 8px; position: relative; z-index: 1; }
  .report-header .subtitle { font-size: 16px; opacity: 0.8; margin-bottom: 20px; position: relative; z-index: 1; }
  .report-header .meta-row { display: flex; gap: 24px; font-size: 13px; opacity: 0.7; position: relative; z-index: 1; flex-wrap: wrap; }

  .section { background: #fff; border-radius: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); padding: 32px; margin-bottom: 28px; }
  .section-title { font-size: 18px; font-weight: 700; color: #1a365d; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
  .section-title .icon { width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 16px; }
  .icon-blue { background: #ebf4ff; color: #2b6cb0; }
  .icon-green { background: #e6fffa; color: #2f855a; }
  .icon-orange { background: #fefcbf; color: #c05621; }
  .icon-purple { background: #faf5ff; color: #6b46c1; }
  .icon-red { background: #fff5f5; color: #c53030; }

  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 8px; }
  .kpi-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px; color: #fff; text-align: center; }
  .kpi-card:nth-child(2) { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
  .kpi-card:nth-child(3) { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
  .kpi-card:nth-child(4) { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
  .kpi-card .kpi-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 6px; }
  .kpi-card .kpi-value { font-size: 24px; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

  table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; border-radius: 8px; overflow: hidden; }
  thead th { background: #2d3748; color: #fff; font-weight: 600; padding: 14px 16px; text-align: left; position: sticky; top: 0; z-index: 1; }
  tbody td { padding: 12px 16px; border-bottom: 1px solid #edf2f7; }
  tbody tr:hover { background: #f7fafc; }
  tbody tr:last-child td { border-bottom: none; }
  .num { text-align: right; font-variant-numeric: tabular-nums; font-family: 'Consolas', 'Menlo', monospace; }

  .chart-title { font-size: 14px; font-weight: 600; color: #4a5568; margin-bottom: 12px; }
  .chart-full { margin-bottom: 24px; }
  canvas { width: 100%; border-radius: 8px; background: #f8f9fb; border: 1px solid #e8ecf1; }

  .legend { display: flex; flex-wrap: wrap; gap: 16px; margin-bottom: 12px; font-size: 13px; color: #4a5568; }
  .legend-item { display: flex; align-items: center; gap: 6px; }
  .legend-swatch { width: 20px; height: 3px; border-radius: 2px; }

  .analysis-content { color: #4a5568; font-size: 15px; line-height: 1.9; }
  .analysis-content p { margin-bottom: 14px; }
  .analysis-content strong { color: #1a365d; font-weight: 700; }
  .analysis-content ul, .analysis-content ol { margin: 12px 0 16px 24px; }
  .analysis-content li { margin-bottom: 10px; padding-left: 4px; line-height: 1.7; }
  .analysis-content ol li { list-style-type: decimal; }
  .analysis-content li::marker { color: #2b6cb0; font-weight: 700; }

  .chart-wrap { position: relative; overflow: hidden; }
  .tooltip { position: absolute; pointer-events: none; background: rgba(26,32,44,0.92); color: #fff; padding: 8px 14px; border-radius: 8px; font-size: 12px; line-height: 1.6; white-space: nowrap; display: none; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.25); }
  .crosshair { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; display: none; z-index: 5; }
  .crosshair-v { width: 1px; background: rgba(102,126,234,0.5); position: absolute; top: 0; height: 100%; }

  .report-footer { text-align: center; padding: 24px; color: #a0aec0; font-size: 12px; border-top: 1px solid #e2e8f0; margin-top: 12px; }

  @media print { body { background: #fff; } .page { padding: 0; } .section { box-shadow: none; border: 1px solid #e2e8f0; } }
  @media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } .page { padding: 16px; } }
</style>
</head>
<body>
<div class="page">

  <div class="report-header">
    <h1>{STOCK_NAME} 금융 데이터 분석 리포트</h1>
    <div class="subtitle">Machbase Neo AI 기반 심층 분석 보고서</div>
    <div class="meta-row">
      <span>&#128197; {GENERATED_DATE}</span>
      <span>&#128202; {TAG_COUNT}개 태그 · {DATA_COUNT}건</span>
      <span>&#9200; {TIME_RANGE}</span>
    </div>
  </div>

  <div class="section" style="background:transparent;box-shadow:none;padding:0;">
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-label">종목</div><div class="kpi-value">{STOCK_NAME}</div></div>
      <div class="kpi-card"><div class="kpi-label">태그 수</div><div class="kpi-value">{TAG_COUNT}</div></div>
      <div class="kpi-card"><div class="kpi-label">데이터 건수</div><div class="kpi-value">{DATA_COUNT}</div></div>
      <div class="kpi-card"><div class="kpi-label">분석 기간</div><div class="kpi-value">{TIME_RANGE}</div></div>
    </div>
  </div>

  <!-- Candlestick Chart (OHLC) -->
  <div class="section" id="candlestickSection">
    <div class="section-title"><div class="icon icon-red">&#128200;</div> 캔들스틱 차트 (OHLC)</div>
    <div class="chart-full chart-wrap"><canvas id="candleChart" height="360"></canvas><div class="crosshair" id="candleCross"><div class="crosshair-v"></div></div><div class="tooltip" id="candleTip"></div></div>
  </div>

  <!-- Price Trend + Moving Averages -->
  <div class="section" id="trendSection">
    <div class="section-title"><div class="icon icon-blue">&#128200;</div> 가격 추세 + 이동평균</div>
    <div class="legend" id="trendLegend">
      <div class="legend-item"><div class="legend-swatch" style="background:#4a7cfa;height:3px;"></div>Close</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#f59e42;"></div>MA5</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#48bb78;"></div>MA20</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#9f7aea;"></div>MA60</div>
    </div>
    <div class="chart-full chart-wrap"><canvas id="trendChart" height="340"></canvas><div class="crosshair" id="trendCross"><div class="crosshair-v"></div></div><div class="tooltip" id="trendTip"></div></div>
  </div>

  <!-- Bollinger Bands -->
  <div class="section" id="bollingerSection">
    <div class="section-title"><div class="icon icon-purple">&#128202;</div> 볼린저밴드 (Bollinger Bands)</div>
    <div class="legend">
      <div class="legend-item"><div class="legend-swatch" style="background:#4a7cfa;height:3px;"></div>Close</div>
      <div class="legend-item"><div class="legend-swatch" style="background:#e53e3e;"></div>MA20</div>
      <div class="legend-item"><div class="legend-swatch" style="background:rgba(159,122,234,0.35);height:8px;border-radius:2px;"></div>Band (&#177;2&#963;)</div>
    </div>
    <div class="chart-full chart-wrap"><canvas id="bbChart" height="340"></canvas><div class="crosshair" id="bbCross"><div class="crosshair-v"></div></div><div class="tooltip" id="bbTip"></div></div>
  </div>

  <!-- Volume-Price Correlation -->
  <div class="section" id="volumeSection">
    <div class="section-title"><div class="icon icon-green">&#128202;</div> 거래량-가격 상관 (Volume-Price)</div>
    <div class="chart-full chart-wrap"><canvas id="volumeChart" height="320"></canvas><div class="crosshair" id="volumeCross"><div class="crosshair-v"></div></div><div class="tooltip" id="volumeTip"></div></div>
  </div>

  <!-- Tag Stats -->
  <div class="section">
    <div class="section-title"><div class="icon icon-blue">&#128200;</div> 태그별 통계 요약</div>
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
    <div class="section-title"><div class="icon icon-orange">&#128270;</div> 심층 분석</div>
    <div class="analysis-content">{ANALYSIS}</div>
  </div>

  <!-- Recommendations -->
  <div class="section">
    <div class="section-title"><div class="icon icon-purple">&#128161;</div> 종합 소견 및 권고사항</div>
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
    ctx.strokeStyle = '#e8ecf1'; ctx.lineWidth = 1;
    for (var i = 0; i <= steps; i++) {
      var y = pad.t + ch - (ch * i / steps);
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W - pad.r, y); ctx.stroke();
      ctx.fillStyle = '#8e99a4'; ctx.font = '11px Segoe UI'; ctx.textAlign = 'right';
      ctx.fillText(fmt(mn + range * i / steps), pad.l - 10, y + 4);
    }
  }

  /* ---- Draw X axis labels ---- */
  function drawXLabels(ctx, slice, pad, W, H, step, offset) {
    var n = slice.length;
    ctx.fillStyle = '#8e99a4'; ctx.font = '10px Segoe UI'; ctx.textAlign = 'center';
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
    ctx.strokeStyle = '#cbd5e0'; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(pad.l, pad.t + ch); ctx.lineTo(W - pad.r, pad.t + ch); ctx.stroke();
  }

  /* ---- Zoom hint text ---- */
  function drawZoomHint(ctx, pad, zoomed) {
    ctx.fillStyle = '#a0aec0'; ctx.font = '10px Segoe UI'; ctx.textAlign = 'left';
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

    ctx.fillStyle = '#22c55e'; ctx.font = 'bold 11px Segoe UI'; ctx.textAlign = 'left';
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
    ctx.strokeStyle = '#e8ecf1'; ctx.lineWidth = 1;
    for (var i = 0; i <= 5; i++) {
      var y = pad.t + ch - (ch * i / 5);
      ctx.beginPath(); ctx.moveTo(pad.l, y); ctx.lineTo(W - pad.r, y); ctx.stroke();
      ctx.fillStyle = '#4a7cfa'; ctx.font = '11px Segoe UI'; ctx.textAlign = 'right';
      ctx.fillText(fmt(pMin + pRange * i / 5), pad.l - 10, y + 4);
    }

    // Right Y labels (volume)
    for (var i = 0; i <= 5; i++) {
      var y = pad.t + ch - (ch * i / 5);
      ctx.fillStyle = '#48bb78'; ctx.font = '11px Segoe UI'; ctx.textAlign = 'left';
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
    ctx.fillStyle = '#4a7cfa'; ctx.font = 'bold 11px Segoe UI'; ctx.textAlign = 'left';
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

})();
</script>
</body>
</html>
```
