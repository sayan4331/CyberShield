(function () {
  const pwInput = document.getElementById("password-input");
  if (!pwInput) return; // not on this page

  const toggleBtn = document.getElementById("toggle-password");
  const gaugeFill = document.getElementById("pw-gauge-fill");
  const scoreText = document.getElementById("pw-score-text");
  const strengthLabel = document.getElementById("pw-strength-label");
  const GAUGE_CIRC = 251;

  toggleBtn.addEventListener("click", () => {
    const isPw = pwInput.type === "password";
    pwInput.type = isPw ? "text" : "password";
    toggleBtn.textContent = isPw ? "Hide" : "Show";
  });

  function resetGauge() {
    gaugeFill.style.strokeDashoffset = GAUGE_CIRC;
    scoreText.textContent = "0";
    strengthLabel.textContent = "—";
    document.getElementById("pw-entropy").textContent = "0";
    document.getElementById("pw-crack-time").textContent = "—";
    document.querySelectorAll(".check-item").forEach(el => el.classList.remove("pass"));
  }

  function updateGauge(score, strength) {
    const offset = GAUGE_CIRC - (GAUGE_CIRC * score) / 100;
    gaugeFill.style.strokeDashoffset = offset;
    let color = "var(--red)";
    if (score >= 90) color = "var(--teal)";
    else if (score >= 70) color = "#7FE0A8";
    else if (score >= 50) color = "var(--amber)";
    else if (score >= 30) color = "#E8813F";
    gaugeFill.style.stroke = color;
    scoreText.textContent = score;
    strengthLabel.textContent = strength;
  }

  async function checkPassword(pw) {
    if (!pw) { resetGauge(); return; }
    try {
      const data = await Api.checkPassword(pw);
      updateGauge(data.score, data.strength);
      document.getElementById("pw-entropy").textContent = data.entropy_bits;
      document.getElementById("pw-crack-time").textContent = data.estimated_crack_time;
      Object.entries(data.checks).forEach(([key, passed]) => {
        const el = document.querySelector(`.check-item[data-key="${key}"]`);
        if (el) el.classList.toggle("pass", passed);
      });
    } catch (e) {
      console.error("Password check failed", e);
    }
  }

  pwInput.addEventListener("input", debounce(e => checkPassword(e.target.value), 300));
  resetGauge();
})();
