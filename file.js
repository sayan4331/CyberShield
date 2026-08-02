(function () {
  const dropzone = document.getElementById("dropzone");
  if (!dropzone) return; // not on this page

  const fileInput = document.getElementById("file-input");
  const fileResult = document.getElementById("file-result");

  dropzone.addEventListener("click", () => fileInput.click());
  ["dragenter", "dragover"].forEach(evt =>
    dropzone.addEventListener(evt, e => { e.preventDefault(); dropzone.classList.add("dragover"); })
  );
  ["dragleave", "drop"].forEach(evt =>
    dropzone.addEventListener(evt, e => { e.preventDefault(); dropzone.classList.remove("dragover"); })
  );
  dropzone.addEventListener("drop", e => {
    const file = e.dataTransfer.files[0];
    if (file) scanFile(file);
  });
  fileInput.addEventListener("change", () => {
    if (fileInput.files[0]) scanFile(fileInput.files[0]);
  });

  async function scanFile(file) {
    const formData = new FormData();
    formData.append("file", file);
    const label = dropzone.querySelector("p");
    label.textContent = `Scanning ${file.name}...`;
    try {
      const data = await Api.scanFile(formData);
      fileResult.classList.remove("hidden");
      const badge = document.getElementById("file-verdict-badge");
      badge.textContent = data.verdict;
      badge.className = `verdict-badge ${verdictBadgeClass(data.verdict)}`;
      document.getElementById("file-risk-score").textContent = data.risk_score;
      document.getElementById("file-name").textContent = data.filename;
      document.getElementById("file-size").textContent = fmtBytes(data.size_bytes);
      document.getElementById("file-hash").textContent = data.sha256;
      const list = document.getElementById("file-flag-list");
      list.innerHTML = "";
      data.flags.forEach(f => {
        const li = document.createElement("li");
        li.textContent = f;
        list.appendChild(li);
      });
    } catch (e) {
      console.error("File scan failed", e);
    } finally {
      label.innerHTML = "<strong>Drop a file here</strong> or click to browse";
    }
  }
})();
