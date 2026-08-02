(function () {
  const statTotal = document.getElementById("stat-total");
  if (!statTotal) return; // not on this page

  let chartPasswords, chartUrls, chartFiles;
  const CHART_TEXT = "#8798B3";
  const CHART_GRID = "#223049";

  function baseChartOptions(legendPos = "bottom") {
    return {
      responsive: true,
      plugins: {
        legend: { position: legendPos, labels: { color: CHART_TEXT, font: { family: "JetBrains Mono", size: 11 } } },
      },
    };
  }

  function renderPasswordChart(byStrength) {
    const order = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"];
    const colors = { "Very Weak": "#E8555F", "Weak": "#E8813F", "Fair": "#F4B740", "Strong": "#7FE0A8", "Very Strong": "#3FD8C4" };
    const labels = order.filter(k => byStrength[k]);
    const values = labels.map(k => byStrength[k]);
    const ctx = document.getElementById("chart-passwords").getContext("2d");
    if (chartPasswords) chartPasswords.destroy();
    chartPasswords = new Chart(ctx, {
      type: "doughnut",
      data: { labels: labels.length ? labels : ["No data"], datasets: [{
        data: values.length ? values : [1],
        backgroundColor: labels.length ? labels.map(l => colors[l]) : ["#223049"],
        borderColor: "#121B2E", borderWidth: 2,
      }]},
      options: baseChartOptions(),
    });
  }

  function renderUrlChart(byVerdict) {
    const order = ["Likely Safe", "Low Risk", "Medium Risk", "High Risk", "Invalid"];
    const colors = { "Likely Safe": "#3FD8C4", "Low Risk": "#7FE0A8", "Medium Risk": "#F4B740", "High Risk": "#E8555F", "Invalid": "#5A6B87" };
    const labels = order.filter(k => byVerdict[k]);
    const values = labels.map(k => byVerdict[k]);
    const ctx = document.getElementById("chart-urls").getContext("2d");
    if (chartUrls) chartUrls.destroy();
    chartUrls = new Chart(ctx, {
      type: "bar",
      data: { labels: labels.length ? labels : ["No data"], datasets: [{
        data: values.length ? values : [0],
        backgroundColor: labels.length ? labels.map(l => colors[l]) : ["#223049"],
        borderRadius: 4,
      }]},
      options: { ...baseChartOptions(), plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: CHART_TEXT, font: { family: "JetBrains Mono", size: 10 } }, grid: { color: CHART_GRID } },
          y: { beginAtZero: true, ticks: { color: CHART_TEXT, precision: 0 }, grid: { color: CHART_GRID } },
        } },
    });
  }

  function renderFileChart(byVerdict) {
    const order = ["Clean", "Suspicious", "Malicious"];
    const colors = { "Clean": "#3FD8C4", "Suspicious": "#F4B740", "Malicious": "#E8555F" };
    const labels = order.filter(k => byVerdict[k]);
    const values = labels.map(k => byVerdict[k]);
    const ctx = document.getElementById("chart-files").getContext("2d");
    if (chartFiles) chartFiles.destroy();
    chartFiles = new Chart(ctx, {
      type: "pie",
      data: { labels: labels.length ? labels : ["No data"], datasets: [{
        data: values.length ? values : [1],
        backgroundColor: labels.length ? labels.map(l => colors[l]) : ["#223049"],
        borderColor: "#121B2E", borderWidth: 2,
      }]},
      options: baseChartOptions(),
    });
  }

  function renderActivity(items) {
    const log = document.getElementById("activity-log");
    log.innerHTML = "";
    if (!items.length) {
      log.innerHTML = '<li class="activity-empty">No activity yet. Run a check to populate the feed.</li>';
      return;
    }
    const typeLabel = { password: "PASSWORD", url: "URL", file: "FILE" };
    items.forEach(item => {
      const li = document.createElement("li");
      const badgeClass = verdictBadgeClass(item.label);
      const time = new Date(item.created_at + "Z").toLocaleTimeString("en-GB");
      li.innerHTML = `
        <span>[${typeLabel[item.type]}] ${item.label}</span>
        <span class="tag-pill ${badgeClass}">${time}</span>
      `;
      log.appendChild(li);
    });
  }

  async function loadDashboard() {
    try {
      const data = await Api.getDashboardStats();

      document.getElementById("stat-passwords").textContent = data.totals.passwords_checked;
      document.getElementById("stat-urls").textContent = data.totals.urls_scanned;
      document.getElementById("stat-files").textContent = data.totals.files_scanned;
      document.getElementById("stat-total").textContent =
        data.totals.passwords_checked + data.totals.urls_scanned + data.totals.files_scanned;
      document.getElementById("stat-threat-intel").textContent = data.threat_intel_size;

      renderPasswordChart(data.passwords_by_strength);
      renderUrlChart(data.urls_by_verdict);
      renderFileChart(data.files_by_verdict);
      renderActivity(data.recent_activity);
    } catch (e) {
      console.error("Failed to load dashboard", e);
    }
  }

  document.getElementById("export-history-btn")?.addEventListener("click", () => {
    window.location.href = "/api/history/export";
  });

  loadDashboard();
  setInterval(loadDashboard, 15000); // keep the console live
})();
