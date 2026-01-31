// ===============================
// DUCK-WOD Frontend Logic
// ===============================

const DATA_URL =
  "https://raw.githubusercontent.com/arick-t/duck-wod/main/data/wods.json";

let allWods = [];
let selectedDate = null;
let selectedSources = new Set();

// -------------------------------
// Utils
// -------------------------------
function todayISO() {
  return new Date().toISOString().split("T")[0];
}

function addDays(dateStr, delta) {
  const d = new Date(dateStr);
  d.setDate(d.getDate() + delta);
  return d.toISOString().split("T")[0];
}

function formatDayLabel(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString("he-IL", {
    weekday: "short",
    day: "numeric",
    month: "numeric",
  });
}

// -------------------------------
// Load data
// -------------------------------
async function loadWods() {
  try {
    const res = await fetch(DATA_URL);
    if (!res.ok) throw new Error("Failed to load wods.json");

    allWods = await res.json();

    init();
  } catch (err) {
    console.error(err);
    document.getElementById("app").innerHTML =
      "❌ שגיאה בטעינת אימונים";
  }
}

// -------------------------------
// Init
// -------------------------------
function init() {
  selectedDate = todayISO();

  buildLayout();
  buildSourceSelector();
  buildWeekSelector();
  renderWods();
}

// -------------------------------
// Layout
// -------------------------------
function buildLayout() {
  const app = document.getElementById("app");

  app.innerHTML = `
    <div id="sources-bar"></div>
    <div id="week-bar"></div>
    <div id="wods-container"></div>
  `;
}

// -------------------------------
// Sources selector
// -------------------------------
function buildSourceSelector() {
  const bar = document.getElementById("sources-bar");

  const sources = [...new Set(allWods.map(w => w.source))];

  sources.forEach(src => selectedSources.add(src));

  bar.innerHTML = `
    <h3>מקורות</h3>
    ${sources
      .map(
        src => `
        <label>
          <input type="checkbox" checked data-source="${src}" />
          ${src}
        </label>
      `
      )
      .join("")}
  `;

  bar.querySelectorAll("input").forEach(cb => {
    cb.addEventListener("change", e => {
      const src = e.target.dataset.source;
      e.target.checked
        ? selectedSources.add(src)
        : selectedSources.delete(src);
      renderWods();
    });
  });
}

// -------------------------------
// Week selector
// -------------------------------
function buildWeekSelector() {
  const bar = document.getElementById("week-bar");

  const days = [];
  for (let i = -3; i <= 3; i++) {
    days.push(addDays(selectedDate, i));
  }

  bar.innerHTML = `
    <h3>בחר יום</h3>
    <div class="week">
      ${days
        .map(
          d => `
          <button class="day ${
            d === selectedDate ? "active" : ""
          }" data-date="${d}">
            ${formatDayLabel(d)}
          </button>
        `
        )
        .join("")}
    </div>
  `;

  bar.querySelectorAll(".day").forEach(btn => {
    btn.addEventListener("click", e => {
      selectedDate = e.target.dataset.date;
      buildWeekSelector();
      renderWods();
    });
  });
}

// -------------------------------
// Render WODs
// -------------------------------
function renderWods() {
  const container = document.getElementById("wods-container");

  const wods = allWods.filter(
    w =>
      w.date === selectedDate &&
      selectedSources.has(w.source)
  );

  if (wods.length === 0) {
    container.innerHTML =
      "<p>אין אימונים זמינים ליום זה עבור המקורות שנבחרו</p>";
    return;
  }

  container.innerHTML = wods
    .map(
      wod => `
      <div class="wod-card">
        <h4>${wod.source}</h4>
        ${wod.sections
          .map(
            s => `
            <div class="section">
              <strong>${s.title}</strong>
              <ul>
                ${s.lines.map(l => `<li>${l}</li>`).join("")}
              </ul>
            </div>
          `
          )
          .join("")}
      </div>
    `
    )
    .join("");
}

// -------------------------------
// Start
// -------------------------------
document.addEventListener("DOMContentLoaded", loadWods);
