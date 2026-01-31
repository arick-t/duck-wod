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

  buildLay
