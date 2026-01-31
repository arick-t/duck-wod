const DATA_URL = "data/wods.json";

let allData = null;
let selectedDate = new Date().toISOString().slice(0, 10);
let enabledSources = new Set();

document.addEventListener("DOMContentLoaded", () => {
  loadData();
});

async function loadData() {
  try {
    const res = await fetch(DATA_URL);
    if (!res.ok) throw new Error("Fetch failed");
    allData = await res.json();

    initSources();
    initDatePicker();
    render();
  } catch (e) {
    document.getElementById("content").innerHTML =
      "❌ שגיאה בטעינת אימונים";
    console.error(e);
  }
}

/* ---------- SOURCES ---------- */

function initSources() {
  const container = document.getElementById("sources");
  container.innerHTML = "";

  allData.sources.forEach(src => {
    enabledSources.add(src.id);

    const label = document.createElement("label");
    label.style.marginRight = "12px";

    const cb = document.createElement("input");
    cb.type = "checkbox";
    cb.checked = true;
    cb.onchange = () => {
      cb.checked ? enabledSources.add(src.id) : enabledSources.delete(src.id);
      render();
    };

    label.appendChild(cb);
    label.append(" " + src.name);
    container.appendChild(label);
  });
}

/* ---------- DATE PICKER ---------- */

function initDatePicker() {
  const container = document.getElementById("dates");
  container.innerHTML = "";

  const today = new Date(selectedDate);

  for (let i = -3; i <= 3; i++) {
    const d = new Date(today);
    d.setDate(today.getDate() + i);
    const iso = d.toISOString().slice(0, 10);

    const btn = document.createElement("button");
    btn.textContent = iso === selectedDate ? "היום" : iso.slice(5);
    btn.className = iso === selectedDate ? "active" : "";

    btn.onclick = () => {
      selectedDate = iso;
      initDatePicker();
      render();
    };

    container.appendChild(btn);
  }
}

/* ---------- RENDER ---------- */

function render() {
  const container = document.getElementById("content");
  container.innerHTML = "";

  let foundAny = false;

  allData.sources.forEach(src => {
    if (!enabledSources.has(src.id)) return;

    const wod = src.wods.find(w => w.date === selectedDate);
    if (!wod) return;

    foundAny = true;

    const block = document.createElement("div");
    block.className = "wod";

    const title = document.createElement("h2");
    title.textContent = src.name;
    block.appendChild(title);

    wod.sections.forEach(sec => {
      const secEl = document.createElement("div");
      secEl.className = "section";

      const h3 = document.createElement("h3");
      h3.textContent = sec.title;
      secEl.appendChild(h3);

      const ul = document.createElement("ul");
      sec.lines.forEach(line => {
        const li = document.createElement("li");
        li.textContent = line;
        ul.appendChild(li);
      });

      secEl.appendChild(ul);
      block.appendChild(secEl);
    });

    container.appendChild(block);
  });

  if (!foundAny) {
    container.innerHTML = "❌ אין אימונים ליום זה";
  }
}
