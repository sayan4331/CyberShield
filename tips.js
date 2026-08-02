(function () {
  const grid = document.getElementById("tips-grid");
  if (!grid) return; // not on this page

  async function loadTips() {
    try {
      const tips = await Api.getTips();
      grid.innerHTML = "";
      tips.forEach(t => {
        const card = document.createElement("div");
        card.className = "tip-card";
        card.innerHTML = `
          <span class="tip-category">${t.category}</span>
          <h3>${t.title}</h3>
          <p>${t.body}</p>
        `;
        grid.appendChild(card);
      });
    } catch (e) {
      console.error("Failed to load tips", e);
    }
  }

  loadTips();
})();
