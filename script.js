let allWods = [];
let activeDate = null;
let enabledSources = new Set();

/* ---------- Date helpers ---------- */

const WEEKDAYS_HE = [
  "ראשון",
  "שני",
  "שלישי",
  "רביעי",
  "חמישי",
  "שישי",
  "שבת"
];

function isToday(dateStr) {
  const d = new Date(dateStr);
  const t = new Date();
  return (
    d.getFullYear() === t.getFullYear() &&
    d.getMonth() === t.getMonth() &&
    d.getDate() === t.getDate()
  );
}

function formatDayLabel(dateStr) {
  const date = new Date(dateStr);

  const dayName = isToday(dateStr)
    ? "היום"
    : WEEKDAYS_HE[date.getDay()];

  const shortDate = `${date.getDate()}/${date.getMonth() + 1}`;

  return { dayName, shortDate };
}

/* ---------- Load data ---------- */

async function loadWods() {
  try {
    const res = await fetch("data/wods.json");
    if (!res.ok) throw new Error("HTTP error");

    const data = await res.json();
    allWods = data.sources || [];

    enabledSources.clear();
    allWods.forEach(s => enabledSources.add(s.id));

    buildSourceFilter();
    buildDaySelector();
    renderWods();
  } catch (e) {
    document.getElementById("wods").innerText = "❌ שגיאה בטעינת אימונים";
    console.error(e);
  }
}

/* ---------- UI builders ---------- */

function buildSourceFilter() {
  const container = document.getElementById("sources");
  container.innerHTML = "";

  allWods.forEach(source => {
    const label = document.createElement("label");
    label.className = "source-checkbox";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = true;
    cb.onchange = () => {
      cb.checked
        ? enabledSources.add(source.id)
        : enabledSources.delete(source.id);
      renderWods();
    };

    label.appendChild(cb);
    label.append(" " + source.name);
    container.appendChild(label);
  });
}

function buildDaySelector() {
  const container = document.getElementById("days");
  container.innerHTML = "";

  const dates = new Set();
  allWods.forEach(src =>
    src.wods.forEach(w => dates.add(w.date))
  );

  const sortedDates = Array.from(dates).sort().reverse();

  if (!activeDate) {
    activeDate =
      sortedDates.find(isToday) || sortedDates[0];
  }

  sortedDates.forEach(date => {
    const { dayName, shortDate } = formatDayLabel(date);

    const btn = document.createElement("button");
    btn.className = "day-btn";
    if (isToday(date)) btn.classList.add("today");
    if (date === activeDate) btn.classList.add("active");

    btn.innerHTML = `
      <div class="day-name">${dayName}</div>
      <div class="day-date">${shortDate}</div>
    `;

    btn.onclick = () => {
      activeDate = date;
      buildDaySelector();
      renderWods();
    };

    container.appendChild(btn);
  });
}

/* ---------- Render ---------- */

function renderWods() {
  const container = document.getElementById("wods");
  container.innerHTML = "";

  let found = false;

  allWods.forEach(source => {
    if (!enabledSources.has(source.id)) return;

    source.wods.forEach(wod => {
      if (wod.date !== activeDate) return;

      found = true;

      const card = document.createElement("div");
      card.className = "wod-card";

      card.innerHTML = `
        <div class="wod-header">
          <div class="wod-source">${source.name}</div>
          <div class="wod-date">${wod.date}</div>
        </div>
      `;

      wod.sections.forEach(sec => {
        const section = document.createElement("div");
        section.className = "wod-section";

        section.innerHTML = `
          <div class="section-title">${sec.title}</div>
          <ul class="section-lines">
            ${sec.lines.map(l => `<li>${l}</li>`).join("")}
          </ul>
        `;

        card.appendChild(section);
      });

      container.appendChild(card);
    });
  });

  if (!found) {
    container.innerText = "אין אימונים ליום הזה";
  }
}

/* ---------- Init ---------- */

document.addEventListener("DOMContentLoaded", loadWods);
