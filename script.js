// DUCK-WOD Frontend Script v1.0
// Simple, stable, GitHub Pages compatible

document.addEventListener("DOMContentLoaded", () => {
  loadWods();
});

async function loadWods() {
  const container = document.getElementById("wods");
  if (!container) {
    console.error("❌ Element #wods not found in index.html");
    return;
  }

  container.innerHTML = "⏳ טוען אימונים...";

  try {
    const response = await fetch("./data/wods.json", { cache: "no-store" });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`);
    }

    const data = await response.json();

    if (!data.sources || data.sources.length === 0) {
      container.innerHTML = "⚠️ אין מקורות זמינים";
      return;
    }

    container.innerHTML = "";

    data.sources.forEach(source => {
      if (!source.wods || source.wods.length === 0) return;

      const sourceBlock = document.createElement("div");
      sourceBlock.className = "source";

      const sourceTitle = document.createElement("h2");
      sourceTitle.textContent = source.name;
      sourceBlock.appendChild(sourceTitle);

      source.wods.forEach(wod => {
        const wodCard = document.createElement("div");
        wodCard.className = "wod";

        const dateEl = document.createElement("h3");
        dateEl.textContent = wod.date;
        wodCard.appendChild(dateEl);

        wod.sections.forEach(section => {
          const sectionTitle = document.createElement("h4");
          sectionTitle.textContent = section.title;
          wodCard.appendChild(sectionTitle);

          const ul = document.createElement("ul");
          section.lines.forEach(line => {
            const li = document.createElement("li");
            li.textContent = line;
            ul.appendChild(li);
          });

          wodCard.appendChild(ul);
        });

        const link = document.createElement("a");
        link.href = wod.url;
        link.textContent = "🔗 למקור המקורי";
        link.target = "_blank";
        wodCard.appendChild(link);

        sourceBlock.appendChild(wodCard);
      });

      container.appendChild(sourceBlock);
    });

  } catch (err) {
    console.error("❌ Failed loading WODs:", err);
    container.innerHTML = "❌ שגיאה בטעינת אימונים";
  }
}
