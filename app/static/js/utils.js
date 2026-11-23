async function collectNow(event) {
  const button = event?.currentTarget || document.getElementById('snapshotButton');
  if (!button || button.disabled) return;
  const label = button.innerHTML;
  button.disabled = true;
  button.textContent = 'Collecting…';
  try {
    const response = await fetch('/api/metrics/collect', { method: 'POST', headers: { Accept: 'application/json' } });
    if (!response.ok) throw new Error(`Snapshot failed (${response.status})`);
    const result = await response.json();
    if (window.showHudToast) showHudToast(`Snapshot collected · ${new Date(result.timestamp).toLocaleTimeString()}`);
    if (window.refreshDashboard) await refreshDashboard();
  } catch (error) {
    if (window.showHudToast) showHudToast(`Snapshot failed · ${error.message}`);
  } finally {
    button.innerHTML = label;
    button.disabled = false;
  }
}
