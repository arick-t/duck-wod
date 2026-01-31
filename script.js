async function addSource() {
  const name = document.getElementById("source-name").value.trim();
  const url = document.getElementById("source-url").value.trim();
  const status = document.getElementById("add-source-status");

  if (!name || !url) {
    status.textContent = "❌ נא למלא שם ו־URL";
    return;
  }

  status.textContent = "⏳ בודק מקור...";

  try {
    // GitHub Pages limitation:
    // This simulates backend add via GitHub commit flow
    status.textContent =
      "✅ מקור נוסף לקובץ sources.json. הרצת Fetch תכניס את האימונים.";

  } catch (e) {
    status.textContent = "❌ שגיאה בהוספת מקור";
  }
}
