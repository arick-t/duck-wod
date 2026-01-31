const DATA_URL = './data/wods.json';

let allData = null;
let selectedDate = null;
let enabledSources = new Set();

// ---------- utils ----------
function formatDate(date) {
  return date.toISOString().split('T')[0];
}

function todayDate() {
  return formatDate(new Date());
}

// ---------- load ----------
async function loadData() {
  try {
    const res = await fetch(DATA_URL);
    if (!res.ok) throw new Error('Fetch failed');
    allData = await res.json();
    init();
  } catch (e) {
    document.getElementById('wods').innerText = '❌ שגיאה בטעינת אימונים';
    console.error(e);
  }
}

// ---------- init ----------
function init() {
  selectedDate = todayDate();

  allData.sources.forEach(src => {
    enabledSources.add(src.id);
  });

  renderSources();
  renderDays();
  renderWods();
}

// ---------- sources ----------
function renderSources() {
  const el = document.getElementById('sources');
  el.innerHTML = '';

  allData.sources.forEach(src => {
    const label = document.createElement('label');
    label.className = 'source-toggle';

    const cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.checked = true;

    cb.onchange = () => {
      cb.checked ? enabledSources.add(src.id) : enabledSources.delete(src.id);
      renderWods();
    };

    label.append(cb, ' ', src.name);
    el.appendChild(label);
  });
}

// ---------- days ----------
function renderDays() {
  const el = document.getElementById('days');
  el.innerHTML = '';

  const dates = new Set();

  allData.sources.forEach(src => {
    src.wods?.forEach(w => dates.add(w.date));
  });

  [...dates].sort().forEach(date => {
    const btn = document.createElement('button');
    btn.innerText = date;
    btn.className = date === selectedDate ? 'active' : '';

    btn.onclick = () => {
      selectedDate = date;
      renderDays();
      renderWods();
    };

    el.appendChild(btn);
  });
}

// ---------- wods ----------
function renderWods() {
  const el = document.getElementById('wods');
  el.innerHTML = '';

  let found = false;

  allData.sources.forEach(src => {
    if (!enabledSources.has(src.id)) return;

    const wod = src.wods?.find(w => w.date === selectedDate);
    if (!wod) return;

    found = true;

    const box = document.createElement('div');
    box.className = 'wod';

    const h = document.createElement('h3');
    h.innerText = `${src.name} — ${selectedDate}`;
    box.appendChild(h);

    wod.sections.forEach(sec => {
      const t = document.createElement('h4');
      t.innerText = sec.title;
      box.appendChild(t);

      const ul = document.createElement('ul');
      sec.lines.forEach(line => {
        const li = document.createElement('li');
        li.innerText = line;
        ul.appendChild(li);
      });
      box.appendChild(ul);
    });

    el.appendChild(box);
  });

  if (!found) {
    el.innerText = 'אין אימונים ליום הנבחר';
  }
}

// ---------- start ----------
loadData();
