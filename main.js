// ---------- Tab navigation (used on index.html) ----------
function initTabs() {
  const tabs = document.querySelectorAll(".tab[data-tab]");
  const views = document.querySelectorAll(".view");
  if (!tabs.length) return;
  tabs.forEach(tab => {
    tab.addEventListener("click", () => {
      tabs.forEach(t => t.classList.remove("active"));
      views.forEach(v => v.classList.remove("active"));
      tab.classList.add("active");
      document.getElementById(`view-${tab.dataset.tab}`).classList.add("active");
    });
  });
}

// ---------- Clock ----------
function initClock() {
  const el = document.getElementById("clock");
  if (!el) return;
  const tick = () => { el.textContent = new Date().toLocaleTimeString("en-GB"); };
  tick();
  setInterval(tick, 1000);
}

// ---------- Shared helpers ----------
function verdictBadgeClass(verdict) {
  const v = verdict.toLowerCase();
  if (["malicious", "high risk", "invalid"].includes(v)) return "badge-danger";
  if (["suspicious", "medium risk", "low risk"].includes(v)) return "badge-caution";
  return "badge-safe";
}

function debounce(fn, ms) {
  let t;
  return (...args) => { clearTimeout(t); t = setTimeout(() => fn(...args), ms); };
}

function fmtBytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 ** 2) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 ** 2).toFixed(2)} MB`;
}

document.addEventListener("DOMContentLoaded", () => {
  initTabs();
  initClock();
});
