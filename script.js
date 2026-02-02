const container = document.getElementById("wods-container");
const loading = document.getElementById("loading");
const todayBtn = document.getElementById("today-btn");

let allWods = [];

fetch("data/wods.json")
  .then(res => res.json())
  .then(data => {
    loading.remove();

    // רק MYLOE
    allWods = data.filter(w => w.source === "MYLOE");
    renderWods(allWods);
  });

function renderWods(wods) {
  container.innerHTML = "";

  wods.forEach(wod => {
    const day = document.createElement("div");
    day.className = "wod-day";
    day.dataset.date = wod.date;

    day.innerHTML = `
      <div class="wod-date">${wod.date}</div>
      <pre class="wod-text">${wod.content}</pre>
    `;

    container.appendChild(day);
  });
}

// כפתור היום
todayBtn.addEventListener("click", () => {
  const today = new Date().toISOString().split("T")[0];

  document.querySelectorAll(".wod-day").forEach(day => {
    day.style.display =
      day.dataset.date === today ? "block" : "none";
  });
});
