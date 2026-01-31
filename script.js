// DUCK-WOD Frontend Script – FINAL FIXED VERSION 🦆

// ---- Utils ----
function getBasePath() {
  // Works for GitHub Pages project sites
  const path = window.location.pathname;
  if (path === "/" || path === "") return "";
  return path.replace(/\/[^\/]*$/, "");
}

const BASE_PATH = getBasePath();
const WODS_URL = `${BASE_PATH}/data/wods.json`;

// ---- DOM ----
const container = document.getElementById("wods-container") || document.body;

// ---- Load WODs ----
async function loadWods() {
  try {
    const res = await fetch(WODS_URL, { cache: "no-store" });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    const data = await res.json();

    if (!data.sources || data.sources.length === 0) {
      throw new Error("No sources found");
    }

    renderWods(data.sources);
  } catch (err) {
    console.error("WOD load error:", err);
    container.innerHTML = `
      <div style="color:#dc2626; font-weight:700; text-align:center; margin-top:40px">
        ❌ שגיאה בטעינת אימונים<br>
        <span style="font-size:14px; color:#888">
          (${err.message})
        </span>
      </div>
    `;
  }
}

// ---- Render ----
function renderWods(sources) {
  container.innerHTML = "";

  sources.forEach(source => {
    if (!source.wods || source.wods.length === 0) return;

    sou
