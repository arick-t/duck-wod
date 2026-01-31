const DATA_URL = "data/wods.json";

let allSources = [];
let activeSources = new Set();
let selectedDate = null;

// ---------- INIT ----------
fetch(DATA_URL)
  .then(res => {
    if (!res.ok) throw new Error("Failed to load wods.json");
    return res.json();
  })
  .then(data => {
    allSources = data.sources || [];
    if (!allSources.length) {
      showError("אין מקורות");
      return;
    }

    allSources.forEach(s => activeSources.add(s.id));
    selectedDate = today();

    renderSourceSelector();
    renderDateSelector();
    renderWods();
  })
  .catch(err => {
    console.error(err);
    showError("❌ שגיאה בטעינת אימונים");
  });

// ---------- HELPERS ----------
function today() {
  return new Date().toISOString().slice(0, 10);
}

function getWeekDates(baseDate) {
  const base = new Date(baseDate);
  const start = new Date(base);
  start.setDate(base.getDate() - base.getDay());

  return Array.from({ length: 7 }).map((_, i) => {
    const d = new Date(start);
    d.setDate(start.getDate() + i);
    return d.toISOString().slice(0, 10);
  });
}

function showError(msg) {
  document.getElementById("content").innerText = msg;
}

// ---------- UI ----------
function renderSourceSelector() {
  const el = document.getElementById("sources");
  el.innerHTML = "";

  allSources.forEach(src => {
    const label = document.createElement("label");
    label.style.marginRight = "12px";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = activeSources.has(src.id);

    cb.onchange = () => {
      cb.checked ? activeSources.add(src.id) : activeSources.delete(src.id);
      renderWods();
    };

    label.appendChild(cb);
    label.append(" " + src.name);
    el.appendChild(label);
  });
}

function renderDateSelector() {
  const el = document.getElementById("dates");
  el.innerHTML = "";

  getWeekDates(selectedDate).forEach(date => {
    const btn = document.createElement("button");
    btn.textContent = date.slice(5);
    if (date === selectedDate) btn.classList.add("active");

    btn.onclick = () => {
      selectedDate = date;
      renderDateSelector();
      renderWods();
    };

    el.appendChild(btn);
  });
}

// ---------- WODS ----------
function renderWods() {
  const container = document.getElementById("content");
  container.innerHTML = "";

  let found = false;

  allSources.forEach(src => {
    if (!activeSources.has(src.id)) return;

    const wod = (src.wods || []).find(w => w.date === selectedDate);
    if (!wod) return;

    found = true;

    const card = document.createElement("div");
    card.className = "wod";

    const title = document.createElement("h2");
    title.textContent = src.name + " – " + wod.date;
    card.appendChild(title);

    wod.sections.forEach(sec => {
      const secDiv = document.createElement("div");
      secDiv.className = "section";

      const h3 = document.createElement("h3");
      h3.textContent = sec.title;
      secDiv.appendChild(h3);

      const ul = document.createElement("ul");
      sec.lines.forEach(line => {
        const li = document.createElement("li");
        li.textContent = line;
        ul.appendChild(li);
      });

      secDiv.appendChild(ul);
      card.appendChild(secDiv);
    });

    container.appendChild(card);
  });

  if (!found) {
    container.innerText = "אין אימונים ליום זה";
  }
}
