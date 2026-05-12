# 운전 행동 데이터 HTML 분석 리포트 템플릿

운전 행동 데이터(IMU 가속도/자이로 + 행동 분류)에 적합한 HTML 분석 리포트 템플릿입니다.
안전 점수 게이지, 이벤트 타임라인, 3축 가속도/자이로 추이, Class 분포 차트를 포함합니다.

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
| {DRIVING_DATA_JSON} | 태그별 raw+rollup+이벤트 JSON | SQL → 자동 계산 |
| {ROLLUP_LABEL} | ROLLUP 단위 라벨 | 자동 계산 |
| {ANALYSIS} | 심층 분석 | LLM 생성 |
| {RECOMMENDATIONS} | 종합 소견 및 권고 | LLM 생성 |

---

### R-3. 운전 행동 데이터 종합 분석 리포트
용도: 운전 행동 데이터(가속도, 자이로, 행동 분류 등)의 안전 점수, 급가속/급제동/급회전 이벤트, 3축 IMU 추이, Class 분포를 차트와 함께 보여주는 심층 분석 보고서입니다.

```html
<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{TABLE} 운전 행동 분석 리포트</title>
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
  .icon-teal { background: #e6fffa; color: #319795; }

  .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 8px; }
  .kpi-card { background: linear-gradient(135deg, #2c5364 0%, #203a43 100%); border-radius: 12px; padding: 20px; color: #fff; text-align: center; }
  .kpi-card:nth-child(2) { background: linear-gradient(135deg, #e53e3e 0%, #c53030 100%); }
  .kpi-card:nth-child(3) { background: linear-gradient(135deg, #ed8936 0%, #dd6b20 100%); }
  .kpi-card:nth-child(4) { background: linear-gradient(135deg, #38b2ac 0%, #319795 100%); }
  .kpi-card .kpi-label { font-size: 12px; text-transform: uppercase; letter-spacing: 1px; opacity: 0.85; margin-bottom: 6px; }
  .kpi-card .kpi-value { font-size: 24px; font-weight: 800; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .kpi-card:nth-child(4) .kpi-value { font-size: 16px; }

  .gauge-row { display: flex; gap: 24px; align-items: stretch; }
  .gauge-wrap { flex: 1; }
  .stats-card { flex: 1; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .stat-item { background: #f7fafc; border-radius: 8px; padding: 12px 16px; }
  .stat-item .stat-label { font-size: 11px; color: #718096; text-transform: uppercase; letter-spacing: 0.5px; }
  .stat-item .stat-value { font-size: 20px; font-weight: 800; color: #2d3748; font-variant-numeric: tabular-nums; }

  .tag-select { padding: 8px 14px; border-radius: 8px; border: 2px solid #e2e8f0; font-size: 14px; font-weight: 600; color: #2d3748; background: #fff; cursor: pointer; margin-left: 16px; min-width: 160px; }
  .tag-select:focus { outline: none; border-color: #2c5364; }

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
  .crosshair-v { width: 1px; background: rgba(44,83,100,0.5); position: absolute; top: 0; height: 100%; }

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
  @media (max-width: 768px) { .kpi-grid { grid-template-columns: repeat(2, 1fr); } .gauge-row { flex-direction: column; } .page { padding: 16px; } }
</style>
</head>
<body>
<div class="page">

  <div class="report-header">
    <h1>{TABLE} 운전 행동 분석 리포트</h1>
    <div class="subtitle">Machbase Neo AI 기반 운전 행동 심층 분석 보고서</div>
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

  <!-- Safety Score + Stats -->
  <div class="section">
    <div class="section-title"><div class="icon icon-green">&#128663;</div> 운전 안전 점수</div>
    <div class="gauge-row">
      <div class="gauge-wrap">
        <div id="safetyGauge"></div>
        <div class="gauge-note">급가속/급제동/급회전 빈도 및 위험 운전 비율 기반</div>
      </div>
      <div class="stats-card" id="statsCard"></div>
    </div>
  </div>

  <!-- Event Timeline + Summary Table -->
  <div class="section">
    <div class="section-title"><div class="icon icon-red">&#9888;</div> 이벤트 타임라인 (급가속/급제동/급회전)</div>
    <div class="chart-full chart-wrap"><canvas id="eventChart" height="300"></canvas><div class="crosshair" id="eventCross"><div class="crosshair-v"></div></div><div class="tooltip" id="eventTip"></div></div>
    <div style="margin-top:16px;">
      <table>
        <thead><tr>
          <th>이벤트 유형</th><th class="num">발생 횟수</th><th class="num">비율(%)</th><th>최대 집중 구간</th>
        </tr></thead>
        <tbody id="eventTableBody"></tbody>
      </table>
    </div>
  </div>

  <!-- Raw Waveform with Tag Selector -->
  <div class="section">
    <div class="section-title"><div class="icon icon-blue">&#128200;</div> 원시 파형 <select id="tagSelect" class="tag-select" onchange="switchTag(this.value)"></select></div>
    <div class="chart-full chart-wrap"><canvas id="waveChart" height="300"></canvas><div class="crosshair" id="waveCross"><div class="crosshair-v"></div></div><div class="tooltip" id="waveTip"></div></div>
  </div>

  <!-- 3-Axis Accelerometer Trend -->
  <div class="section">
    <div class="section-title"><div class="icon icon-orange">&#128202;</div> 3축 가속도 추이 ({ROLLUP_LABEL} 평균)</div>
    <div class="chart-full chart-wrap"><canvas id="accChart" height="280"></canvas><div class="tooltip" id="accTip"></div></div>
  </div>

  <!-- 3-Axis Gyroscope Trend -->
  <div class="section">
    <div class="section-title"><div class="icon icon-purple">&#128202;</div> 3축 자이로 추이 ({ROLLUP_LABEL} 평균)</div>
    <div class="chart-full chart-wrap"><canvas id="gyroChart" height="280"></canvas><div class="tooltip" id="gyroTip"></div></div>
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
    <div class="section-title"><div class="icon icon-green">&#128161;</div> 종합 소견 및 권고사항</div>
    <div class="analysis-content">{RECOMMENDATIONS}</div>
  </div>

  <div class="report-footer">Machbase Neo 데이터 기반으로 생성 되었습니다.</div>
</div>

<script>
(function(){
  var tagList = {TAG_LIST_JSON};
  var D = {DRIVING_DATA_JSON};
  var perTag = D.per_tag || {};
  var events = D.events || {};
  var safetyScore = D.safety_score || 0;
  var summary = D.summary || {};
  var thresholds = D.thresholds || {};
  var currentTag = '';

  // Filter IMU tags (exclude Class)
  var imuTags = tagList.filter(function(t){ return t.toLowerCase() !== 'class'; });
  currentTag = imuTags[0] || '';

  var dpr = window.devicePixelRatio || 1;
  function setup(id,h){var c=document.getElementById(id);if(!c)return null;var w=c.parentElement.getBoundingClientRect().width;c.width=w*dpr;c.height=h*dpr;c.style.width=w+'px';c.style.height=h+'px';var ctx=c.getContext('2d');ctx.scale(dpr,dpr);return{ctx:ctx,w:w,h:h,canvas:c};}
  function niceMax(v){if(v<=0)return 1;var p=Math.pow(10,Math.floor(Math.log10(v)));return Math.ceil(v/p)*p;}
  function fmt(v){if(Math.abs(v)>=10000)return(v/1000).toFixed(1)+'K';if(Math.abs(v)>=100)return v.toFixed(1);if(Math.abs(v)>=1)return v.toFixed(2);return v.toFixed(4);}
  function z(n){return n<10?'0'+n:''+n;}
  function toHHMM(ms){var dt=new Date(ms);return z(dt.getHours())+':'+z(dt.getMinutes());}
  function toFullTime(ms){var dt=new Date(ms);return dt.getFullYear()+'-'+z(dt.getMonth()+1)+'-'+z(dt.getDate())+' '+z(dt.getHours())+':'+z(dt.getMinutes())+':'+z(dt.getSeconds())+'.'+String(dt.getMilliseconds()).padStart(3,'0');}
  function rollupToHHMM(t){var m=t.match(/(\d{2}:\d{2})/);return m?m[1]:t;}

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
    // Scroll zoom
    function onWheel(ev){
      ev.preventDefault();var rect=cv.getBoundingClientRect(),mx=ev.clientX-rect.left;
      var cw=rect.width-100,n=st.e-st.s;var ratio=Math.max(0,Math.min(1,(mx-70)/cw));
      var zf=ev.deltaY>0?1.3:0.7,newN=Math.round(n*zf);if(newN<4)newN=4;
      if(newN>=fullLen){st.s=0;st.e=fullLen;drawFn(st.s,st.e);return;}
      var center=st.s+Math.round(n*ratio),ns=Math.round(center-newN*ratio);
      if(ns<0)ns=0;var ne=ns+newN;if(ne>fullLen){ne=fullLen;ns=ne-newN;}
      st.s=Math.max(0,ns);st.e=ne;drawFn(st.s,st.e);
    }
    // Double-click reset
    function onDbl(){st.s=0;st.e=fullLen;drawFn(st.s,st.e);}
    // Drag to pan
    var drag={active:false,startX:0,startS:0,startE:0};
    function onDown(ev){
      if(st.e-st.s>=fullLen)return;// no pan when fully zoomed out
      drag.active=true;drag.startX=ev.clientX;drag.startS=st.s;drag.startE=st.e;
      cv.style.cursor='grabbing';
    }
    function onMove(ev){
      if(!drag.active)return;
      var rect=cv.getBoundingClientRect(),cw=rect.width-100;
      var n=drag.startE-drag.startS;
      var dx=ev.clientX-drag.startX;
      var shift=Math.round(-dx/cw*n);
      var ns=drag.startS+shift,ne=drag.startE+shift;
      if(ns<0){ns=0;ne=n;}
      if(ne>fullLen){ne=fullLen;ns=fullLen-n;}
      st.s=ns;st.e=ne;drawFn(st.s,st.e);
    }
    function onUp(){drag.active=false;cv.style.cursor='crosshair';}
    cv.addEventListener('wheel',onWheel,{passive:false});
    cv.addEventListener('dblclick',onDbl);
    cv.addEventListener('mousedown',onDown);
    cv.addEventListener('mousemove',onMove);
    cv.addEventListener('mouseup',onUp);
    cv.addEventListener('mouseleave',onUp);
    zoomHandlers[canvasId]={w:onWheel,d:onDbl,md:onDown,mm:onMove,mu:onUp,ml:onUp};
  }

  // --- Draw line chart (single series) ---
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
    ctx.fillStyle='#8e99a4';ctx.font='10px Segoe UI';ctx.textAlign='center';
    var ls=Math.max(1,Math.floor(n/8)),lastLabel='';
    for(var i=0;i<n;i+=ls){if(xLabels[i]!==lastLabel){ctx.fillText(xLabels[i],pad.l+step*i,H-pad.b+18);lastLabel=xLabels[i];}}
    ctx.strokeStyle='#cbd5e0';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);ctx.lineTo(W-pad.r,pad.t+ch);ctx.stroke();
    var pts=vals.map(function(v,i){var x=pad.l+step*i,y=pad.t+ch-((v-mn)/range*ch);return{x:x,y:y,label:'<strong>'+tl[i]+'</strong><br>'+fmt(v)};});
    addTip(canvasId,tipId,pts);
  }

  // --- Draw multi-line chart (3 axes overlaid, with legend toggle) ---
  var toggleState={};
  function drawMultiLine(canvasId,tipId,xLabels,series,height,tipLabels){
    if(!toggleState[canvasId])toggleState[canvasId]={};
    var c=setup(canvasId,height);if(!c)return;
    var tl=tipLabels||xLabels;
    var ctx=c.ctx,W=c.w,H=c.h,pad={t:30,r:100,b:50,l:70};
    var cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
    var n=xLabels.length;if(n<2)return;
    // Filter visible series
    var visible=series.filter(function(s){return toggleState[canvasId][s.name]!==false;});
    var allVals=[];visible.forEach(function(s){allVals=allVals.concat(s.data);});
    if(allVals.length===0)allVals=[0];
    var mn=Math.min.apply(null,allVals),mx=Math.max.apply(null,allVals);
    var margin=(mx-mn)*0.1||1;mn-=margin;mx+=margin;
    var range=mx-mn||1,step=cw/(n-1);
    ctx.clearRect(0,0,W,H);
    ctx.strokeStyle='#e8ecf1';ctx.lineWidth=1;
    for(var i=0;i<=5;i++){var y=pad.t+ch-(ch*i/5);ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle='#8e99a4';ctx.font='11px Segoe UI';ctx.textAlign='right';ctx.fillText(fmt(mn+range*i/5),pad.l-10,y+4);}
    // Zero line
    var zy=pad.t+ch-((-mn)/range*ch);
    if(zy>pad.t&&zy<pad.t+ch){ctx.strokeStyle='#cbd5e0';ctx.lineWidth=1;ctx.setLineDash([3,3]);ctx.beginPath();ctx.moveTo(pad.l,zy);ctx.lineTo(W-pad.r,zy);ctx.stroke();ctx.setLineDash([]);}
    var pts=[];
    // Draw visible lines
    visible.forEach(function(s){
      ctx.beginPath();
      for(var i=0;i<n;i++){var x=pad.l+step*i,y=pad.t+ch-((s.data[i]-mn)/range*ch);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
      ctx.strokeStyle=s.color;ctx.lineWidth=1.8;ctx.stroke();
    });
    // Legend (all series, dimmed if hidden)
    var legendHitBoxes=[];
    series.forEach(function(s,si){
      var ly=pad.t+16+si*20;
      var isVisible=toggleState[canvasId][s.name]!==false;
      ctx.globalAlpha=isVisible?1.0:0.3;
      ctx.fillStyle=s.color;ctx.fillRect(W-pad.r+10,ly-5,12,3);
      ctx.font='bold 12px Segoe UI';ctx.textAlign='left';
      ctx.fillText(s.name,W-pad.r+26,ly);
      ctx.globalAlpha=1.0;
      legendHitBoxes.push({name:s.name,x:W-pad.r+8,y:ly-12,w:80,h:20});
    });
    // Legend click handler
    var cv=document.getElementById(canvasId);
    if(cv&&!cv._legendBound){
      cv._legendBound=true;
      cv.addEventListener('click',function(e){
        var rect=cv.getBoundingClientRect();
        var mx=e.clientX-rect.left,my=e.clientY-rect.top;
        legendHitBoxes.forEach(function(hb){
          if(mx>=hb.x&&mx<=hb.x+hb.w&&my>=hb.y&&my<=hb.y+hb.h){
            toggleState[canvasId][hb.name]=toggleState[canvasId][hb.name]===false?true:false;
            drawMultiLine(canvasId,tipId,xLabels,series,height,tipLabels);
          }
        });
      });
    }
    // Tooltip
    for(var i=0;i<n;i++){
      var x=pad.l+step*i,y=pad.t+ch/2;
      var label='<strong>'+tl[i]+'</strong>';
      visible.forEach(function(s){label+='<br><span style="color:'+s.color+'">'+s.name+':</span> '+fmt(s.data[i]);});
      pts.push({x:x,y:y,label:label});
    }
    ctx.fillStyle='#8e99a4';ctx.font='10px Segoe UI';ctx.textAlign='center';
    var ls=Math.max(1,Math.floor(n/8)),lastLabel='';
    for(var i=0;i<n;i+=ls){if(xLabels[i]!==lastLabel){ctx.fillText(xLabels[i],pad.l+step*i,H-pad.b+18);lastLabel=xLabels[i];}}
    addTip(canvasId,tipId,pts);
  }

  // --- Safety gauge ---
  function drawSafetyGauge(score){
    var el=document.getElementById('safetyGauge');if(!el)return;
    var zones=[
      {min:80,max:100,color:'#48bb78',bg:'#c6f6d5',label:'Safe',emoji:'&#9989;'},
      {min:60,max:80,color:'#ecc94b',bg:'#fefcbf',label:'Moderate',emoji:'&#9888;&#65039;'},
      {min:40,max:60,color:'#ed8936',bg:'#feebc8',label:'Risky',emoji:'&#128308;'},
      {min:0,max:40,color:'#e53e3e',bg:'#fed7d7',label:'Dangerous',emoji:'&#128680;'}
    ];
    var activeZone=zones.length-1;
    for(var i=0;i<zones.length;i++){if(score>=zones[i].min){activeZone=i;break;}}
    var zn=zones[activeZone];
    var pct=Math.min(100,Math.max(0,score));
    var html='<div style="text-align:center;margin-bottom:16px;">';
    html+='<span style="font-size:36px;font-weight:800;color:'+zn.color+';">'+score.toFixed(1)+'</span>';
    html+='<span style="font-size:14px;color:#718096;margin-left:8px;">/ 100</span>';
    html+='<div style="font-size:15px;font-weight:700;color:'+zn.color+';margin-top:4px;">'+zn.emoji+' '+zn.label+'</div>';
    html+='</div>';
    html+='<div style="position:relative;height:32px;border-radius:16px;overflow:hidden;display:flex;">';
    zones.slice().reverse().forEach(function(z){
      html+='<div style="flex:1;background:'+z.bg+';display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:600;color:'+z.color+';">'+z.label+'</div>';
    });
    html+='</div>';
    html+='<div style="position:relative;height:16px;">';
    html+='<div style="position:absolute;left:'+pct.toFixed(1)+'%;transform:translateX(-50%);font-size:18px;line-height:1;color:'+zn.color+';">&#9650;</div>';
    html+='</div>';
    html+='<div style="display:flex;font-size:10px;color:#a0aec0;margin-top:2px;">';
    html+='<div style="flex:1;text-align:left;">0</div><div style="flex:1;text-align:center;">40</div><div style="flex:1;text-align:center;">60</div><div style="flex:1;text-align:center;">80</div><div style="flex:1;text-align:right;">100</div>';
    html+='</div>';
    el.innerHTML=html;
  }

  // --- Stats card ---
  function updateStatsCard(){
    var card=document.getElementById('statsCard');if(!card)return;
    var items=[
      {l:'Safety Score',v:safetyScore.toFixed(1)+' / 100'},
      {l:'Total Events',v:(summary.total_events||0).toLocaleString()},
      {l:'Accel',v:(summary.accel_count||0).toLocaleString()+' ('+(summary.accel_rate||0)+'%)'},
      {l:'Brake',v:(summary.brake_count||0).toLocaleString()+' ('+(summary.brake_rate||0)+'%)'},
      {l:'Turn',v:(summary.turn_count||0).toLocaleString()+' ('+(summary.turn_rate||0)+'%)'},
      {l:'Total Samples',v:(summary.total_samples||0).toLocaleString()}
    ];
    card.innerHTML=items.map(function(it){return '<div class="stat-item"><div class="stat-label">'+it.l+'</div><div class="stat-value">'+it.v+'</div></div>';}).join('');
  }

  // --- Event timeline (AccX waveform + event markers) + summary table ---
  function drawEventTimeline(s,e){
    var accXData=perTag['AccX']||perTag['accx']||perTag['ACCX'];
    if(!accXData||!accXData.raw)return;
    var raw=accXData.raw;
    var times=raw.times_ms||[],vals=raw.values||[];
    var st=s||0,en=e||vals.length;
    var tSlice=times.slice(st,en),vSlice=vals.slice(st,en);
    var n=vSlice.length;if(n<2)return;

    var c=setup('eventChart',300);if(!c)return;
    var ctx=c.ctx,W=c.w,H=c.h,pad={t:30,r:120,b:50,l:70};
    var cw=W-pad.l-pad.r,ch=H-pad.t-pad.b;
    var mn=Math.min.apply(null,vSlice),mx=Math.max.apply(null,vSlice);
    var margin=(mx-mn)*0.1||1;mn-=margin;mx+=margin;
    var range=mx-mn||1,step=cw/(n-1);
    ctx.clearRect(0,0,W,H);

    // Grid
    ctx.strokeStyle='#e8ecf1';ctx.lineWidth=1;
    for(var i=0;i<=5;i++){var y=pad.t+ch-(ch*i/5);ctx.beginPath();ctx.moveTo(pad.l,y);ctx.lineTo(W-pad.r,y);ctx.stroke();ctx.fillStyle='#8e99a4';ctx.font='11px Segoe UI';ctx.textAlign='right';ctx.fillText(fmt(mn+range*i/5),pad.l-10,y+4);}

    // Threshold lines (adaptive: mean ± 2σ)
    var refs=[];
    if(thresholds.accel_upper!=null)refs.push({val:thresholds.accel_upper,color:'#e53e3e',label:'Accel +2σ'});
    if(thresholds.brake_lower!=null)refs.push({val:thresholds.brake_lower,color:'#3182ce',label:'Brake -2σ'});
    refs.forEach(function(rl){
      var ry=pad.t+ch-((rl.val-mn)/range*ch);
      if(ry>pad.t&&ry<pad.t+ch){ctx.strokeStyle=rl.color;ctx.lineWidth=1;ctx.setLineDash([5,5]);ctx.beginPath();ctx.moveTo(pad.l,ry);ctx.lineTo(W-pad.r,ry);ctx.stroke();ctx.setLineDash([]);ctx.fillStyle=rl.color;ctx.font='10px Segoe UI';ctx.textAlign='left';ctx.fillText(rl.label,W-pad.r+4,ry+3);}
    });

    // AccX waveform
    ctx.beginPath();
    for(var i=0;i<n;i++){var x=pad.l+step*i,y=pad.t+ch-((vSlice[i]-mn)/range*ch);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);}
    ctx.strokeStyle='#a0aec0';ctx.lineWidth=1.2;ctx.stroke();

    // Event markers (sampled to avoid clutter)
    var t0=tSlice[0],t1=tSlice[n-1],tRange=t1-t0||1;
    var evTypes=[
      {key:'accel',color:'#e53e3e',label:'급가속',shape:'up'},
      {key:'brake',color:'#3182ce',label:'급제동',shape:'down'},
      {key:'turn',color:'#ed8936',label:'급회전',shape:'diamond'}
    ];
    var maxMarkers=200;
    evTypes.forEach(function(et){
      var evts=(events[et.key]||[]).filter(function(ev){return ev.t_ms>=t0&&ev.t_ms<=t1;});
      var sampleStep=Math.max(1,Math.ceil(evts.length/maxMarkers));
      for(var i=0;i<evts.length;i+=sampleStep){
        var ev=evts[i];
        var ex=pad.l+((ev.t_ms-t0)/tRange)*cw;
        var ey=pad.t+ch-((ev.value-mn)/range*ch);
        ctx.fillStyle=et.color;ctx.beginPath();
        if(et.shape==='up'){ctx.moveTo(ex,ey-6);ctx.lineTo(ex-4,ey+3);ctx.lineTo(ex+4,ey+3);}
        else if(et.shape==='down'){ctx.moveTo(ex,ey+6);ctx.lineTo(ex-4,ey-3);ctx.lineTo(ex+4,ey-3);}
        else{ctx.moveTo(ex,ey-5);ctx.lineTo(ex+4,ey);ctx.lineTo(ex,ey+5);ctx.lineTo(ex-4,ey);}
        ctx.closePath();ctx.fill();
      }
    });

    // Legend
    evTypes.forEach(function(et,i){
      var ly=pad.t+16+i*18;
      ctx.fillStyle=et.color;ctx.beginPath();
      if(et.shape==='up'){ctx.moveTo(W-pad.r+16,ly-4);ctx.lineTo(W-pad.r+12,ly+4);ctx.lineTo(W-pad.r+20,ly+4);}
      else if(et.shape==='down'){ctx.moveTo(W-pad.r+16,ly+4);ctx.lineTo(W-pad.r+12,ly-4);ctx.lineTo(W-pad.r+20,ly-4);}
      else{ctx.moveTo(W-pad.r+16,ly-4);ctx.lineTo(W-pad.r+20,ly);ctx.lineTo(W-pad.r+16,ly+4);ctx.lineTo(W-pad.r+12,ly);}
      ctx.closePath();ctx.fill();
      ctx.fillStyle='#4a5568';ctx.font='12px Segoe UI';ctx.textAlign='left';
      ctx.fillText(et.label,W-pad.r+26,ly+4);
    });

    // X-axis
    var xLabels=tSlice.map(toHHMM);
    ctx.fillStyle='#8e99a4';ctx.font='10px Segoe UI';ctx.textAlign='center';
    var ls=Math.max(1,Math.floor(n/8)),lastLabel='';
    for(var i=0;i<n;i+=ls){if(xLabels[i]!==lastLabel){ctx.fillText(xLabels[i],pad.l+step*i,H-pad.b+18);lastLabel=xLabels[i];}}
    ctx.strokeStyle='#cbd5e0';ctx.lineWidth=1.5;ctx.beginPath();ctx.moveTo(pad.l,pad.t+ch);ctx.lineTo(W-pad.r,pad.t+ch);ctx.stroke();

    // Tooltip
    var pts=vSlice.map(function(v,i){
      var x=pad.l+step*i,y=pad.t+ch-((v-mn)/range*ch);
      return{x:x,y:y,label:'<strong>'+toFullTime(tSlice[i])+'</strong><br>AccX: '+fmt(v)};
    });
    addTip('eventChart','eventTip',pts);
  }

  function drawEventCharts(){
    drawEventTimeline();
    var accXData=perTag['AccX']||perTag['accx']||perTag['ACCX'];
    if(accXData&&accXData.raw){
      addZoom('eventChart',(accXData.raw.values||[]).length,drawEventTimeline);
    }

    // Bucket events for peak detection using rollup time axis
    var refTag=perTag['AccX']||perTag['accx']||perTag['ACCX']||{};
    var rollup=refTag.rollup||[];
    var tipLabels=rollup.map(function(r){return r.t;});
    var nB=rollup.length||1;

    var allEvts=[].concat(events.accel||[],events.brake||[],events.turn||[]);
    var tMin=Infinity,tMax=-Infinity;
    allEvts.forEach(function(ev){if(ev.t_ms<tMin)tMin=ev.t_ms;if(ev.t_ms>tMax)tMax=ev.t_ms;});
    if(tMin===Infinity){tMin=0;tMax=1;}

    function bucketAndPeak(evtArray){
      var counts=[];for(var i=0;i<nB;i++)counts.push(0);
      var tr=tMax-tMin||1;
      (evtArray||[]).forEach(function(ev){
        var idx=Math.floor((ev.t_ms-tMin)/tr*(nB-1));
        if(idx<0)idx=0;if(idx>=nB)idx=nB-1;
        counts[idx]++;
      });
      var maxVal=0,maxIdx=0;
      counts.forEach(function(v,i){if(v>maxVal){maxVal=v;maxIdx=i;}});
      return tipLabels[maxIdx]||'-';
    }

    var accelPeak=bucketAndPeak(events.accel);
    var brakePeak=bucketAndPeak(events.brake);
    var turnPeak=bucketAndPeak(events.turn);

    var accelTotal=summary.accel_count||0,brakeTotal=summary.brake_count||0,turnTotal=summary.turn_count||0;
    var grandTotal=accelTotal+brakeTotal+turnTotal;

    var tbody=document.getElementById('eventTableBody');
    if(tbody){
      var rows=[
        {name:'<span style="color:#e53e3e;font-weight:700;">&#9650;</span> 급가속',count:accelTotal,rate:summary.accel_rate||0,peak:accelPeak},
        {name:'<span style="color:#3182ce;font-weight:700;">&#9660;</span> 급제동',count:brakeTotal,rate:summary.brake_rate||0,peak:brakePeak},
        {name:'<span style="color:#ed8936;font-weight:700;">&#9670;</span> 급회전',count:turnTotal,rate:summary.turn_rate||0,peak:turnPeak}
      ];
      var html=rows.map(function(r){
        return '<tr><td>'+r.name+'</td><td class="num">'+r.count.toLocaleString()+'</td><td class="num">'+r.rate+'%</td><td>'+r.peak+'</td></tr>';
      }).join('');
      var totalRate=Math.round(((summary.accel_rate||0)+(summary.brake_rate||0)+(summary.turn_rate||0))*10)/10;
      html+='<tr style="font-weight:700;background:#f7fafc;"><td>합계</td><td class="num">'+grandTotal.toLocaleString()+'</td><td class="num">'+totalRate+'%</td><td>-</td></tr>';
      tbody.innerHTML=html;
    }

  }

  // --- 3-axis multi-line charts ---
  function drawAccTrend(){
    var accTags=['AccX','AccY','AccZ'];
    var colors=['#e53e3e','#3182ce','#38a169'];
    var series=[];var xLabels=null,tipLabels=null;
    accTags.forEach(function(tag,i){
      var td=perTag[tag];if(!td||!td.rollup)return;
      var rollup=td.rollup;
      if(!xLabels){xLabels=rollup.map(function(r){return rollupToHHMM(r.t);});tipLabels=rollup.map(function(r){return r.t;});}
      series.push({name:tag,color:colors[i],data:rollup.map(function(r){return r.avg;})});
    });
    if(xLabels&&series.length>0){
      drawMultiLine('accChart','accTip',xLabels,series,280,tipLabels);
      addZoom('accChart',xLabels.length,function(s,e){
        var sl=[];series.forEach(function(sr){sl.push({name:sr.name,color:sr.color,data:sr.data.slice(s,e)});});
        drawMultiLine('accChart','accTip',xLabels.slice(s,e),sl,280,tipLabels.slice(s,e));
      });
    }
  }
  function drawGyroTrend(){
    var gyroTags=['GyroX','GyroY','GyroZ'];
    var colors=['#805ad5','#d69e2e','#319795'];
    var series=[];var xLabels=null,tipLabels=null;
    gyroTags.forEach(function(tag,i){
      var td=perTag[tag];if(!td||!td.rollup)return;
      var rollup=td.rollup;
      if(!xLabels){xLabels=rollup.map(function(r){return rollupToHHMM(r.t);});tipLabels=rollup.map(function(r){return r.t;});}
      series.push({name:tag,color:colors[i],data:rollup.map(function(r){return r.avg;})});
    });
    if(xLabels&&series.length>0){
      drawMultiLine('gyroChart','gyroTip',xLabels,series,280,tipLabels);
      addZoom('gyroChart',xLabels.length,function(s,e){
        var sl=[];series.forEach(function(sr){sl.push({name:sr.name,color:sr.color,data:sr.data.slice(s,e)});});
        drawMultiLine('gyroChart','gyroTip',xLabels.slice(s,e),sl,280,tipLabels.slice(s,e));
      });
    }
  }

  // --- Populate dropdown (IMU tags only) ---
  var sel=document.getElementById('tagSelect');
  imuTags.forEach(function(t){var o=document.createElement('option');o.value=t;o.textContent=t;sel.appendChild(o);});

  // --- Switch tag (raw waveform only) ---
  window.switchTag=function(tag){
    currentTag=tag;
    var d=perTag[tag];if(!d)return;
    var raw=d.raw||{};
    var wTimes=raw.times_ms||[],wVals=raw.values||[];
    if(wVals.length>=2){
      var wAxis=wTimes.map(toHHMM),wTip=wTimes.map(toFullTime);
      drawLineChart('waveChart','waveTip',wAxis,wVals,'#2c5364',300,null,wTip);
      addZoom('waveChart',wVals.length,function(s,e){
        drawLineChart('waveChart','waveTip',wAxis.slice(s,e),wVals.slice(s,e),'#2c5364',300,null,wTip.slice(s,e));
      });
    }
  };

  // --- Initial render ---
  drawSafetyGauge(safetyScore);
  updateStatsCard();
  drawEventCharts();
  drawAccTrend();
  drawGyroTrend();
  if(currentTag)switchTag(currentTag);
})();
</script>
</body>
</html>
```
