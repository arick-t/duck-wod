const wodsEl = document.getElementById("wods");
const sourceFilter = document.getElementById("sourceFilter");
const dateFilter = document.getElementById("dateFilter");

let allWods = [];

fetch("data/wods.json")
  .then(res => res.json())
  .then(data => {
    allWods = data;
    populateSources(data);
    render();
  })
  .catch(() => {
    wodsEl.innerHTML = "<p>❌ שגיאה בטעינת אימונים</p>";
  });

function populateSources(wods) {
  const sources = new Set(wods.map(w => w.source));
  sources.forEach(src => {
    const opt = document.createElement("option");
    opt.value = src;
    opt.textContent = src;
    sourceFilter.appendChild(opt);
  });
}

sourceFilter.addEventListener("change", render);
dateFilter.addEventListener("change", render);

function render() {
  const source = sourceFilter.value;
  const date = dateFilter.value;

  let filtered = allWods;

  if (source !== "all") {
    filtered = filtered.filter(w => w.source === source);
  }

  if (date) {
    filtered = filtered.filter(w => w.date === date);
  }

  if (!filtered.length) {
    wodsEl.innerHTML = "<p>😕 לא נמצאו אימונים</p>";
    return;
  }

  wodsEl.innerHTML = "";

  filtered
    .sort((a, b) => b.date.localeCompare(a.date))
    .forEach(wod => {
      const div = document.createElement("div");
      div.className = "wod";

      div.innerHTML = `
        <h2>${wod.source} – ${wod.date}</h2>
        ${wod.sections.map(sec => `
          <div class="section">
            <h3>${sec.title}</h3>
            <ul>
              ${sec.lines.map(l => `<li>${l}</li>`).join("")}
            </ul>
          </div>
        `).join("")}
        <p><a href="${wod.url}" target="_blank">🔗 מקור</a></p>
      `;

      wodsEl.appendChild(div);
    });
}
