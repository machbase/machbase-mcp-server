# 진동 데이터 HTML 분석 리포트 템플릿

진동 데이터(가속도, 속도, 변위 등)에 적합한 HTML 분석 리포트 템플릿입니다.
태그 선택 드롭다운, Raw Waveform, ISO 10816 게이지, RMS/P2P/Crest Factor 추이, FFT 스펙트럼을 포함합니다.

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

---

### R-2. 진동 데이터 종합 분석 리포트
용도: 진동 데이터(가속도, 속도, 변위 등)의 원시 파형, RMS/Peak-to-Peak/Crest Factor 추이, FFT 주파수 스펙트럼, ISO 10816 심각도를 차트와 함께 보여주는 심층 분석 보고서입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TABLE} 진동 데이터 분석 리포트</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: 'Segoe UI', 'Malgun Gothic', sans-serif; background: #eef1f6; color: #1a202c; line-height: 1.7; }
  .page { max-width: 1000px; margin: 0 auto; padding: 40px 32px; }

  .report-header { background: linear-gradient(135deg, #1b0e2e 0%, #2d1b69 50%, #4c1d95 100%); color: #fff; padding: 48px 40px; border-radius: 16px; margin-bottom: 32px; position: relative; overflow: hidden; }
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
  .icon-teal { background: #e6fffa; color: #319795; }

  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 8px; }
  .kpi-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; padding: 20px; color: #fff; text-align: center; }
  .kpi-card:nth-child(2) { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
  .kpi-card:nth-child(3) { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
  .kpi-card:nth-child(4) { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
  .kpi-card .kpi-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 6px; }
  .kpi-card .kpi-value { font-size: 24px; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .kpi-card:nth-child(4) .kpi-value { font-size: 16px; }

  .tag-select { padding: 8px 14px; border-radius: 8px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: 600; color: #2d3748; background: #fff; cursor: pointer; margin-left: 16px; min-width: 160px; }
  .tag-select:focus { outline: none; border-color: #667eea; }

  .gauge-row { display: flex; gap: 24px; align-items: stretch; }
  .gauge-wrap { flex: 0 0 280px; text-align: center; }
  .stats-card { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .stat-item { background: #f7fafc; border-radius: 8px; padding: 12px 16px; }
  .stat-item .stat-label { font-size: 11px; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; }
  .stat-item .stat-value { font-size: 20px; font-weight: 800; color: #2d3748; font-variant-numeric: tabular-nums; }

  table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 14px; border-radius: 8px; overflow: hidden; }
  thead th { background: #2d3748; color: #fff; font-weight: 600; padding: 14px 16px; text-align: left; position: sticky; top: 0; z-index: 1; }
  tbody td { padding: 12px 16px; border-bottom: 1px solid #edf2f7; }
  tbody tr:hover { background: #f7fafc; }
  tbody tr:last-child td { border-bottom: none; }
  .num { text-align: right; font-variant-numeric: tabular-nums; font-family: 'Consolas', 'Menlo', monospace; }

  .chart-full { margin-bottom: 24px; }
  .chart-wrap { position: relative; overflow: hidden; }
  canvas { width: 100%; border-radius: 8px; background: #f8f9fb; border: 1px solid #e8ecf1; }
  .tooltip { position: absolute; pointer-events: none; background: rgba(26,32,44,0.92); color: #fff; padding: 8px 14px; border-radius: 8px; font-size: 12px; line-height: 1.6; white-space: nowrap; display: none; z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.25); }
  .crosshair { position: absolute; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; display: none; z-index: 5; }
  .crosshair-v { width: 1px; background: rgba(102,126,234,0.5); position: absolute; top: 0; height: 100%; }

  .analysis-content { color: #4a5568; font-size: 15px; line-height: 1.9; }
  .analysis-content p { margin-bottom: 14px; }
  .analysis-content strong { color: #1a365d; font-weight: 700; }
  .analysis-content ul, .analysis-content ol { margin: 12px 0 16px 24px; }
  .analysis-content li { margin-bottom: 10px; padding-left: 4px; line-height: 1.7; }
  .analysis-content ol li { list-style-type: decimal; }
  .analysis-content li::marker { color: #2b6cb0; font-weight: 700; }

  .report-footer { text-align: center; padding: 24px; color: #a0aec0; font-size: 12px; border-top: 1px solid #e2e8f0; margin-top: 12px; }
  .gauge-note { font-size: 11px; color: #a0aec0; margin-top: 4px; }

  @media print { body { background: #fff; } .page { padding: 0; } .section { box-shadow: none; border: 1px solid #e2e8f0; } }
  @media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } .gauge-row { flex-direction: column; } .gauge-wrap { flex: none; } .page { padding: 16px; } }
</style>
</head>
<body>
<div class="page">

  <div class="report-header">
    <h1>{TABLE} 진동 데이터 분석 리포트</h1>
    <div class="subtitle">Machbase Neo AI 기반 진동 심층 분석 보고서</div>
    <div class="meta-row">
      <span>&#128197; {GENERATED_DATE}</span>
      <span>&#128202; {TAG_COUNT}개 태그 · {DATA_COUNT}건</span>
      <span>&#9200; {TIME_RANGE}</span>
    </div>
  </div>

  <div class="section" style="background:transparent;box-shadow:none;padding:0;">
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-label">테이블</div><div class="kpi-value">{TABLE}</div></div>
      <div class="kpi-card"><div class="kpi-label">태그 수</div><div class="kpi-value">{TAG_COUNT}</div></div>
      <div class="kpi-card"><div class="kpi-label">데이터 건수</div><div class="kpi-value">{DATA_COUNT}</div></div>
      <div class="kpi-card"><div class="kpi-label">분석 기간</div><div class="kpi-value">{TIME_RANGE}</div></div>
    </div>
  </div>

  <!-- Tag Selector -->
  <div class="section">
    <div class="section-title">
      <div class="icon icon-purple">&#128204;</div> 분석 태그 선택
      <select id="tagSelect" class="tag-select" onchange="switchTag(this.value)"></select>
    </div>
  </div>

  <!-- Raw Waveform -->
  <div class="section">
    <div class="section-title"><div class="icon icon-blue">&#128200;</div> <span id="waveTitle">원시 파형 (Raw Waveform)</span></div>
    <div class="chart-full chart-wrap"><canvas id="waveChart" height="300"></canvas><div class="crosshair" id="waveCross"><div class="crosshair-v"></div></div><div class="tooltip" id="waveTip"></div></div>
  </div>

  <!-- Vibration Severity + Stats -->
  <div class="section">
    <div class="section-title"><div class="icon icon-red">&#9888;</div> 진동 심각도 평가</div>
    <div class="gauge-row">
      <div style="flex:1;min-width:0;">
        <div id="barGauge"></div>
        <div class="gauge-note">ISO 10816 참고 기준 (단위 확인 필요)</div>
      </div>
      <div class="stats-card" id="statsCard"></div>
    </div>
  </div>

  <!-- RMS Trend -->
  <div class="section">
    <div class="section-title"><div class="icon icon-teal">&#128200;</div> RMS 추이 ({ROLLUP_LABEL} 평균)</div>
    <div class="chart-full chart-wrap"><canvas id="rmsChart" height="250"></canvas><div class="tooltip" id="rmsTip"></div></div>
  </div>

  <!-- Peak-to-Peak Trend -->
  <div class="section">
    <div class="section-title"><div class="icon icon-purple">&#128202;</div> Peak-to-Peak 추이 ({ROLLUP_LABEL})</div>
    <div class="chart-full chart-wrap"><canvas id="p2pChart" height="250"></canvas><div class="tooltip" id="p2pTip"></div></div>
  </div>

  <!-- Crest Factor Trend -->
  <div class="section">
    <div class="section-title"><div class="icon icon-orange">&#128200;</div> Crest Factor 추이 ({ROLLUP_LABEL})</div>
    <div class="chart-full chart-wrap"><canvas id="crestChart" height="250"></canvas><div class="tooltip" id="crestTip"></div></div>
  </div>

  <!-- FFT Spectrum -->
  <div class="section">
    <div class="section-title"><div class="icon icon-green">&#128202;</div> FFT 주파수 스펙트럼 (0.2 Hz 해상도)</div>
    <div class="chart-full chart-wrap"><canvas id="fftChart" height="300"></canvas><div class="tooltip" id="fftTip"></div></div>
  </div>

  <!-- Tag Stats Table -->
  <div class="section">
    <div class="section-title"><div class="icon icon-blue">&#128202;</div> 태그별 통계 요약</div>
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
  var tagList = {TAG_LIST_JSON};
  var perTag = {PER_TAG_DATA_JSON};
  var currentTag = tagList[0] || '';

  var dpr = window.devicePixelRatio || 1;
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
    ctx.strokeStyle='#e8ecf1';ctx.lineWidth=1;
    for(var i=0;i<=5;i++){var y=pad.t+ch-(ch*i/5);ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle='#8e99a4';ctx.font='11px Segoe UI';ctx.textAlign='right';ctx.fillText(fmt(mn+range*i/5),pad.l-10,y+4);}
    if(refLines){refLines.forEach(function(rl){var ry=pad.t+ch-((rl.val-mn)/range*ch);if(ry>pad.t&&ry<pad.t+ch){ctx.strokeStyle=rl.color;ctx.lineWidth=1;ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(pad.l,ry);ctx.lineTo(W-pad.r,ry);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle=rl.color;ctx.font='10px Segoe UI';ctx.textAlign='left';ctx.fillText(rl.label,W-pad.r+4,ry+3);}});}
    ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);
    for(var i=0;i<n;i++)ctx.lineTo(pad.l+step*i,pad.t+ch-((vals[i]-mn)/range*ch));
    ctx.lineTo(pad.l+step*(n-1),pad.t+ch);ctx.closePath();
    var g=ctx.createLinearGradient(0,pad.t,0,pad.t+ch);g.addColorStop(0,color+'40');g.addColorStop(1,color+'05');ctx.fillStyle=g;ctx.fill();
    ctx.beginPath();for(var i=0;i<n;i++){var x=pad.l+step*i,y=pad.t+ch-((vals[i]-mn)/range*ch);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
    ctx.strokeStyle=color;ctx.lineWidth=2;ctx.stroke();
    // X-axis: deduplicated labels (skip if same as previous rendered)
    ctx.fillStyle='#8e99a4';ctx.font='10px Segoe UI';ctx.textAlign='center';
    var ls=Math.max(1,Math.floor(n/8)),lastLabel='';
    for(var i=0;i<n;i+=ls){if(xLabels[i]!==lastLabel){ctx.fillText(xLabels[i],pad.l+step*i,H-pad.b+18);lastLabel=xLabels[i];}}
    ctx.strokeStyle='#cbd5e0';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);ctx.lineTo(W-pad.r,pad.t+ch);ctx.stroke();
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
    ctx.strokeStyle='#e8ecf1';ctx.lineWidth=1;
    for(var i=0;i<=4;i++){var y=pad.t+ch-(ch*i/4);ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle='#8e99a4';ctx.font='11px Segoe UI';ctx.textAlign='right';ctx.fillText(fmt(mx*i/4),pad.l-10,y+4);}
    var pts=[];
    yValues.forEach(function(v,i){var x=pad.l+(cw/n)*i,bh=(v/mx)*ch,y=pad.t+ch-bh;var g=ctx.createLinearGradient(0,y,0,pad.t+ch);g.addColorStop(0,color);g.addColorStop(1,color+'60');ctx.fillStyle=g;ctx.fillRect(x,y,bw,bh);pts.push({x:x+bw/2,y:y,label:'<strong>'+tl[i]+'</strong><br>'+fmt(v)});});
    // X-axis: deduplicated
    ctx.fillStyle='#8e99a4';ctx.font='10px Segoe UI';ctx.textAlign='center';
    var ls=Math.max(1,Math.floor(n/8)),lastLabel='';
    for(var i=0;i<n;i+=ls){if(xLabels[i]!==lastLabel){ctx.fillText(xLabels[i],pad.l+(cw/n)*i+bw/2,H-pad.b+18);lastLabel=xLabels[i];}}
    ctx.strokeStyle='#cbd5e0';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);ctx.lineTo(W-pad.r,pad.t+ch);ctx.stroke();
    addTip(canvasId,tipId,pts);
  }

  // --- Severity Bar Gauge (horizontal, HTML-based) ---
  function drawGauge(rmsVal){
    var el=document.getElementById('barGauge');if(!el)return;
    var zones=[
      {max:1.12,color:'#48bb78',bg:'#c6f6d5',label:'Good',emoji:'&#9989;'},
      {max:2.8,color:'#ecc94b',bg:'#fefcbf',label:'Satisfactory',emoji:'&#9888;&#65039;'},
      {max:7.1,color:'#ed8936',bg:'#feebc8',label:'Unsatisfactory',emoji:'&#128308;'},
      {max:18,color:'#e53e3e',bg:'#fed7d7',label:'Unacceptable',emoji:'&#128680;'}
    ];
    // Determine which zone the value falls into
    var activeZone=zones.length-1;
    for(var i=0;i<zones.length;i++){if(rmsVal<=zones[i].max){activeZone=i;break;}}
    var z=zones[activeZone];
    // Marker position (percentage within the full bar, equal-width zones)
    var lo=activeZone===0?0:zones[activeZone-1].max;
    var hi=z.max;
    var frac=(rmsVal-lo)/(hi-lo);
    var pct=(activeZone+frac)/zones.length*100;
    if(pct>100)pct=100;

    var html='<div style="text-align:center;margin-bottom:16px;">';
    html+='<span style="font-size:36px;font-weight:800;color:'+z.color+';">'+fmt(rmsVal)+'</span>';
    html+='<span style="font-size:14px;color:#718096;margin-left:8px;">RMS</span>';
    html+='<div style="font-size:15px;font-weight:700;color:'+z.color+';margin-top:4px;">'+z.emoji+' '+z.label+'</div>';
    html+='</div>';
    // Bar
    html+='<div style="position:relative;height:32px;border-radius:16px;overflow:hidden;display:flex;">';
    zones.forEach(function(zn){
      html+='<div style="flex:1;background:'+zn.bg+';display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:'+zn.color+';">'+zn.label+'</div>';
    });
    html+='</div>';
    // Marker triangle
    html+='<div style="position:relative;height:16px;">';
    html+='<div style="position:absolute;left:'+pct.toFixed(1)+'%;transform:translateX(-50%);font-size:18px;line-height:1;color:'+z.color+';">&#9650;</div>';
    html+='</div>';
    // Threshold labels
    html+='<div style="display:flex;font-size:10px;color:#a0aec0;margin-top:2px;">';
    html+='<div style="flex:1;text-align:left;">0</div>';
    zones.forEach(function(zn,i){
      html+='<div style="flex:1;text-align:'+(i===zones.length-1?'right':'center')+';">'+zn.max+'</div>';
    });
    html+='</div>';
    el.innerHTML=html;
  }

  function updateStatsCard(stats){
    var card=document.getElementById('statsCard');if(!card)return;
    var items=[
      {l:'RMS',v:fmt(stats.rms||0)},
      {l:'Peak-to-Peak',v:fmt(stats.p2p||0)},
      {l:'Crest Factor',v:fmt(stats.crest||0)},
      {l:'AVG',v:fmt(stats.avg||0)},
      {l:'MIN',v:fmt(stats.min||0)},
      {l:'MAX',v:fmt(stats.max||0)}
    ];
    card.innerHTML=items.map(function(it){return '<div class="stat-item"><div class="stat-label">'+it.l+'</div><div class="stat-value">'+it.v+'</div></div>';}).join('');
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
      var fc=document.getElementById('fftChart');if(fc){var fctx=fc.getContext('2d');fctx.clearRect(0,0,fc.width,fc.height);fctx.fillStyle='#8e99a4';fctx.font='14px Segoe UI';fctx.textAlign='center';fctx.fillText('FFT 데이터 없음',fc.width/2,fc.height/2);}
    }

    // --- Gauge + Stats ---
    var stats=d.stats||{};
    drawGauge(stats.rms||0);
    updateStatsCard(stats);
  };

  // Initial render
  if(currentTag)switchTag(currentTag);
})();
</script>
</body>
</html>
```
