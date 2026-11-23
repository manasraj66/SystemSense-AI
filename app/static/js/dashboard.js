(() => {
  const colors = { cpu: '#00f0ff', memory: '#ff1e42', disk: '#ffae00' };
  const state = { rows: [], processes: [], range: '5m', paused: false, polling: false, visible: { cpu: true, memory: true, disk: true }, timer: null, lastSync: null };
  const canvas = document.getElementById('resourceChart');
  const ctx = canvas.getContext('2d');
  const tooltip = document.getElementById('chartTooltip');
  let hoverIndex = -1;

  function statusFor(key, value) {
    const warning = key === 'memory' ? 85 : 80;
    const critical = 90;
    return value >= critical ? 'critical' : value >= warning ? 'warning' : 'healthy';
  }
  function renderMetric(key, value, timestamp) {
    const card = document.getElementById(key + 'Card');
    const valueNode = document.getElementById(key + 'Value');
    if (key === 'process') {
      valueNode.textContent = Number(value).toLocaleString();
      document.getElementById('processStatus').textContent = 'Processes detected';
      document.getElementById('processThreshold').textContent = 'COUNT';
      card.classList.remove('metric-card-warning', 'metric-card-critical');
      return;
    }
    const number = Number(value) || 0;
    const status = statusFor(key, number);
    valueNode.textContent = number.toFixed(1) + '%';
    const gauge = document.getElementById(key + 'Gauge');
    gauge.style.strokeDashoffset = String(113.1 * (1 - Math.min(100, Math.max(0, number)) / 100));
    const segments = document.getElementById(key + 'Segments');
    if (!segments.childElementCount) for (let i = 0; i < 18; i++) segments.append(document.createElement('i'));
    [...segments.children].forEach((segment, index) => segment.classList.toggle('on', index < Math.round(Math.min(100, number) / 100 * 18)));
    card.classList.toggle('metric-card-warning', status === 'warning');
    card.classList.toggle('metric-card-critical', status === 'critical');
    document.getElementById(key + 'Status').textContent = status === 'healthy' ? 'Within range' : status === 'warning' ? 'Warning threshold' : 'Critical threshold';
    document.getElementById(key + 'Threshold').textContent = status === 'healthy' ? 'NORMAL' : status.toUpperCase();
  }
  function downsample(rows, limit = 60) {
    if (rows.length <= limit) return rows;
    const step = (rows.length - 1) / (limit - 1);
    return Array.from({ length: limit }, (_, i) => rows[Math.round(i * step)]);
  }
  function currentWindow(rows) {
    const minutes = { live: 5, '5m': 5, '15m': 15, '1h': 60 }[state.range];
    const cutoff = Date.now() - minutes * 60000;
    return downsample(rows.filter(row => new Date(row.timestamp).getTime() >= cutoff));
  }
  function setTelemetryState(connected, message = '') {
    document.getElementById('telemetryState').textContent = connected ? 'Active' : 'Unavailable';
    if (connected) state.lastSync = Date.now();
    else state.lastSync = null;
    const pill = document.getElementById('monitoringPill');
    pill.classList.toggle('offline', !connected);
    pill.lastChild.textContent = connected ? ' MONITORING ACTIVE' : ' TELEMETRY OFFLINE';
    document.getElementById('lastSynced').textContent = connected ? 'Just now' : 'No connection';
    if (!connected) {
      document.getElementById('healthStatus').textContent = 'OFFLINE';
      document.getElementById('healthText').textContent = 'System telemetry could not be reached.';
      document.getElementById('healthRadar').className = 'radar critical';
      document.getElementById('diagnosticCallout').hidden = false;
      document.getElementById('diagnosticCallout').textContent = message || 'Check the local monitoring service.';
    }
  }
  function renderHealth(latest) {
    const breached = [
      ['CPU', latest.cpu, 80], ['Memory', latest.memory, 85], ['Disk', latest.disk, 90]
    ].filter(([, value, limit]) => Number(value) >= limit);
    const critical = breached.some(([, value]) => Number(value) >= 90);
    const radar = document.getElementById('healthRadar');
    radar.className = 'radar' + (breached.length ? (critical ? ' critical' : ' warning') : '');
    document.getElementById('healthStatus').textContent = breached.length ? 'ATTENTION REQUIRED' : 'OPTIMAL';
    document.getElementById('healthText').textContent = breached.length ? 'Resource thresholds have been crossed.' : 'All monitored resources are within range.';
    const callout = document.getElementById('diagnosticCallout');
    callout.hidden = !breached.length;
    if (breached.length) callout.textContent = breached.map(([name, value, limit]) => `${name} usage at ${Number(value).toFixed(1)}% exceeds ${limit}% threshold`).join(' · ');
  }
  function renderRows(rows) {
    const visible = rows.filter(row => state.visible[row.key]);
    const rect = canvas.getBoundingClientRect();
    const ratio = Math.max(1, window.devicePixelRatio || 1);
    const width = Math.max(320, rect.width), height = Math.max(190, rect.height);
    canvas.width = Math.round(width * ratio); canvas.height = Math.round(height * ratio);
    ctx.setTransform(ratio, 0, 0, ratio, 0, 0); ctx.clearRect(0, 0, width, height);
    const pad = { left: 37, right: 9, top: 11, bottom: 25 }, plotW = width - pad.left - pad.right, plotH = height - pad.top - pad.bottom;
    ctx.font = '9px "JetBrains Mono", Consolas, monospace'; ctx.textBaseline = 'middle';
    [0, 25, 50, 75, 100].forEach(value => { const y = pad.top + plotH * (1 - value / 100); ctx.strokeStyle = '#222b39'; ctx.beginPath(); ctx.moveTo(pad.left, y); ctx.lineTo(width - pad.right, y); ctx.stroke(); ctx.fillStyle = '#77869b'; ctx.textAlign = 'right'; ctx.fillText(value + '%', pad.left - 6, y); });
    const count = Math.max(1, rows.length);
    visible.forEach(({ key, label }) => {
      if (!rows.length) return;
      const points = rows.map((row, index) => ({ x: pad.left + (count === 1 ? plotW : index / (count - 1) * plotW), y: pad.top + plotH * (1 - Math.min(100, Math.max(0, Number(row[key]) || 0)) / 100) }));
      ctx.beginPath(); points.forEach((point, index) => index ? ctx.lineTo(point.x, point.y) : ctx.moveTo(point.x, point.y));
      ctx.strokeStyle = colors[key]; ctx.lineWidth = 2; ctx.shadowColor = colors[key]; ctx.shadowBlur = 7; ctx.stroke(); ctx.shadowBlur = 0;
      const gradient = ctx.createLinearGradient(0, pad.top, 0, pad.top + plotH); gradient.addColorStop(0, colors[key] + '26'); gradient.addColorStop(1, colors[key] + '00');
      ctx.lineTo(points.at(-1).x, pad.top + plotH); ctx.lineTo(points[0].x, pad.top + plotH); ctx.closePath(); ctx.fillStyle = gradient; ctx.fill();
    });
    ctx.fillStyle = '#77869b'; ctx.textAlign = 'left';
    if (rows.length) { ctx.fillText(new Date(rows[0].timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), pad.left, height - 9); ctx.textAlign = 'right'; ctx.fillText(new Date(rows.at(-1).timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' }), width - pad.right, height - 9); }
    canvas.dataset.plotLeft = String(pad.left); canvas.dataset.plotWidth = String(plotW); canvas.dataset.count = String(rows.length);
    canvas.dataset.plotTop = String(pad.top); canvas.dataset.plotHeight = String(plotH);
    canvas._chartRows = rows;
  }
  async function fetchMetrics() {
    const endpoint = state.range === '1h' ? '/api/history?limit=720' : state.range === '15m' ? '/api/history?limit=200' : '/api/metrics';
    const response = await fetch(endpoint, { headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`Metrics request failed (${response.status})`);
    const rows = await response.json();
    if (!Array.isArray(rows)) throw new Error('Invalid metrics response');
    if (!rows.length) { setTelemetryState(true); state.lastSync = null; document.getElementById('lastSynced').textContent = 'No samples yet'; return; }
    const latest = rows.at(-1);
    state.rows = downsample(rows.slice(-720));
    renderMetric('cpu', latest.cpu, latest.timestamp); renderMetric('memory', latest.memory, latest.timestamp); renderMetric('disk', latest.disk, latest.timestamp); renderMetric('process', latest.process_count, latest.timestamp);
    renderHealth(latest); setTelemetryState(true);
    renderRows(currentWindow(state.rows));
  }
  function renderProcesses() {
    const filter = document.querySelector('[data-process-filter].selected')?.dataset.processFilter || 'all';
    let rows = [...state.processes];
    if (filter === 'cpu') rows = rows.filter(row => Number(row.cpu_percent) >= 80).sort((a, b) => b.cpu_percent - a.cpu_percent);
    if (filter === 'memory') rows = rows.filter(row => Number(row.memory_percent) >= 85).sort((a, b) => b.memory_percent - a.memory_percent);
    rows = rows.slice(0, 8);
    const target = document.getElementById('consumerRows');
    if (!rows.length) { target.innerHTML = `<tr><td colspan="6" class="process-empty">${state.processes.length ? 'No processes match this filter.' : 'No process telemetry is available.'}</td></tr>`; return; }
    target.innerHTML = rows.map(row => `<tr><td>${Number(row.pid)}</td><td>${escapeHtml(row.name || 'Unknown')}</td><td>${escapeHtml(row.username || 'N/A')}</td><td>${Number(row.cpu_percent || 0).toFixed(1)}%</td><td>${Number(row.memory_percent || 0).toFixed(1)}%</td><td><span class="process-status ${row.status === 'running' ? '' : 'sleeping'}">${escapeHtml(row.status || 'unknown')}</span></td></tr>`).join('');
  }
  function escapeHtml(value) { return String(value).replace(/[&<>"']/g, ch => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[ch]); }
  async function fetchProcesses() {
    try { const response = await fetch('/api/processes', { headers: { Accept: 'application/json' } }); if (!response.ok) throw new Error('Process request failed'); state.processes = await response.json(); document.getElementById('processSummary').textContent = `${state.processes.length} processes returned`; renderProcesses(); }
    catch (_) { document.getElementById('processSummary').textContent = 'Process service unavailable'; document.getElementById('consumerRows').innerHTML = '<tr><td colspan="6" class="process-empty">Process telemetry is unavailable.</td></tr>'; }
  }
  async function poll() {
    if (state.paused || document.hidden || state.polling) return;
    state.polling = true;
    try { try { await fetchMetrics(); } catch (error) { setTelemetryState(false, error.message); } await fetchProcesses(); }
    finally { state.polling = false; }
  }
  function startPolling() { clearInterval(state.timer); state.timer = setInterval(poll, 5000); }
  window.refreshDashboard = poll;
  setInterval(() => { if (state.lastSync !== null) document.getElementById('lastSynced').textContent = `${Math.floor((Date.now() - state.lastSync) / 1000)}s ago`; }, 1000);
  document.querySelectorAll('[data-range]').forEach(button => button.addEventListener('click', () => {
    document.querySelectorAll('[data-range]').forEach(item => item.classList.toggle('selected', item === button)); state.range = button.dataset.range;
    document.getElementById('chartWindow').textContent = { live: 'Live sample window', '5m': 'Last 5 minutes', '15m': 'Last 15 minutes', '1h': 'Last hour' }[state.range]; poll();
  }));
  document.querySelectorAll('[data-series]').forEach(button => button.addEventListener('click', () => { const key = button.dataset.series; state.visible[key] = !state.visible[key]; button.classList.toggle('active', state.visible[key]); renderRows(currentWindow(state.rows)); }));
  document.querySelectorAll('[data-process-filter]').forEach(button => button.addEventListener('click', () => { document.querySelectorAll('[data-process-filter]').forEach(item => item.classList.toggle('selected', item === button)); renderProcesses(); }));
  document.getElementById('streamToggle').addEventListener('click', event => { state.paused = !state.paused; event.currentTarget.textContent = state.paused ? 'Resume stream' : 'Pause stream'; if (!state.paused) poll(); });
  canvas.addEventListener('mousemove', event => {
    const rows = canvas._chartRows || []; if (!rows.length) return;
    const bounds = canvas.getBoundingClientRect(), x = event.clientX - bounds.left, left = Number(canvas.dataset.plotLeft), plotWidth = Number(canvas.dataset.plotWidth);
    hoverIndex = Math.max(0, Math.min(rows.length - 1, Math.round((x - left) / plotWidth * (rows.length - 1))));
    renderRows(currentWindow(state.rows));
    const row = rows[hoverIndex]; tooltip.hidden = false; tooltip.style.left = Math.min(bounds.width - 160, Math.max(4, x + 12)) + 'px'; tooltip.style.top = '10px';
    tooltip.innerHTML = `<b>${new Date(row.timestamp).toLocaleString()}</b><br><span style="color:${colors.cpu}">CPU ${Number(row.cpu).toFixed(1)}%</span> · <span style="color:${colors.memory}">RAM ${Number(row.memory).toFixed(1)}%</span> · <span style="color:${colors.disk}">Disk ${Number(row.disk).toFixed(1)}%</span>`;
    const padLeft = Number(canvas.dataset.plotLeft), plotW = Number(canvas.dataset.plotWidth), padTop = Number(canvas.dataset.plotTop), plotH = Number(canvas.dataset.plotHeight), ratio = Math.max(1, window.devicePixelRatio || 1);
    ctx.save(); ctx.setTransform(ratio, 0, 0, ratio, 0, 0); ctx.strokeStyle = '#cbd5e155'; ctx.setLineDash([3, 4]); ctx.beginPath(); ctx.moveTo(padLeft + (rows.length === 1 ? 0 : hoverIndex / (rows.length - 1) * plotW), padTop); ctx.lineTo(padLeft + (rows.length === 1 ? 0 : hoverIndex / (rows.length - 1) * plotW), padTop + plotH); ctx.stroke(); ctx.restore();
  });
  canvas.addEventListener('mouseleave', () => { tooltip.hidden = true; renderRows(currentWindow(state.rows)); });
  document.addEventListener('visibilitychange', () => { if (document.hidden) clearInterval(state.timer); else { poll(); startPolling(); } });
  window.addEventListener('resize', () => renderRows(currentWindow(state.rows)));
  poll(); startPolling();
})();
