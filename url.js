(function () {
  const urlInput = document.getElementById("url-input");
  if (!urlInput) return; // not on this page

  const urlScanBtn = document.getElementById("url-scan-btn");
  const urlResult = document.getElementById("url-result");

  async function scanUrl() {
    const url = urlInput.value.trim();
    if (!url) return;
    urlScanBtn.disabled = true;
    urlScanBtn.textContent = "Scanning...";
    try {
      const data = await Api.scanUrl(url);
      urlResult.classList.remove("hidden");
      const badge = document.getElementById("url-verdict-badge");
      badge.textContent = data.verdict;
      badge.className = `verdict-badge ${verdictBadgeClass(data.verdict)}`;
      document.getElementById("url-risk-score").textContent = data.risk_score;
      const list = document.getElementById("url-flag-list");
      list.innerHTML = "";
      data.flags.forEach(f => {
        const li = document.createElement("li");
        li.textContent = f;
        list.appendChild(li);
      });
    } catch (e) {
      console.error("URL scan failed", e);
    } finally {
      urlScanBtn.disabled = false;
      urlScanBtn.textContent = "Scan";
    }
  }

  urlScanBtn.addEventListener("click", scanUrl);
  urlInput.addEventListener("keydown", e => { if (e.key === "Enter") scanUrl(); });
})();
