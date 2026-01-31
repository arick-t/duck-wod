/* DUCK-WOD Frontend – Stable v1 */

const DATA_URL = './data/wods.json';

const sourcesDiv = document.getElementById('sources');
const datesDiv = document.getElementById('dates');
const contentDiv = document.getElementById('content');

let allData = null;
let selectedDate = null;
let enabledSources = new Set();

/* ---------- Helpers ---------- */

function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function getLast7Days() {
  const days = [];
  const today = new Date();
  for (let i = 0; i < 7; i++) {
    const d = new Date(today);
    d.setDate(today.getDate() - i);
    days.push(formatDate(d));
  }
  return days;
}

/* ---------- Render Sources ---------- */

function renderSources() {
  sourcesDiv.innerHTML = '';

  allData.sources.forEach(src => {
    enabledSources.add(src.id);

    const label = document.createElement('label');
    label.style.display = 'block';

    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = true;

    cb.onchange = () => {
      if (cb.checked) enabledSources.add(src.id);
      else enabledSources.delete(src.id);
      renderWods();
    };

    label.appendChild(cb);
    label.append(' ' + src.name);
    sourcesDiv.appendChild(label);
  });
}

/* ---------- Render Dates ---------- */

function renderDates() {
  const days = getLast7Days();
  selectedDate = days[0];

  datesDiv.innerHTML = '';

  days.forEach(day => {
    const btn = document.createElement('button');
    btn.textContent = day;
    btn.className = day === selectedDate ? 'active' : '';

    btn.onclick = () => {
      selectedDate = day;
      renderDates();
      renderWods();
    };

    datesDiv.appendChild(btn);
  });
}

/* ---------- Render WODs ---------- */

function renderWods() {
  contentDiv.innerHTML = '';

  let foundAny = false;

  allData.sources.forEach(src => {
    if (!enabledSources.has(src.id)) return;

    const wod = src.wods.find(w => w.date === selectedDate);
    if (!wod) return;

    foundAny = true;

    const box = document.createElement('div');
    box.className = 'wod';

    const title = document.createElement('h2');
    title.textContent = src.name + ' – ' + wod.date;
    box.appendChild(title);

    wod.sections.forEach(sec => {
      const section = document.createElement('div');
      section.className = 'section';

      const h3 = document.createElement('h3');
      h3.textContent = sec.title;
      section.appendChild(h3);

      const ul = document.createElement('ul');
      sec.lines.forEach(line => {
        const li = document.createElement('li');
        li.textContent = line;
        ul.appendChild(li);
      });

      section.appendChild(ul);
      box.appendChild(section);
    });

    contentDiv.appendChild(box);
  });

  if (!foundAny) {
    contentDiv.textContent = 'אין אימונים ליום הנבחר';
  }
}

/* ---------- Init ---------- */

fetch(DATA_URL)
  .then(res => {
    if (!res.ok) throw new Error('Failed to load wods.json');
    return res.json();
  })
  .then(data => {
    allData = data;
    renderSources();
    renderDates();
    renderWods();
  })
  .catch(err => {
    contentDiv.textContent = '❌ שגיאה בטעינת אימונים';
  });
