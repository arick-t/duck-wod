// PATH: /script.js
// שלב 1 – טעינת WODs מ־data/wods.json והדפסה לקונסול

const DATA_URL = './data/wods.json';

async function loadWods() {
  try {
    const response = await fetch(DATA_URL);

    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }

    const data = await response.json();

    console.log('WODS DATA LOADED:', data);

    // זמנית – רק בדיקה
    console.log('Sources:', data.sources);

  } catch (error) {
    console.error('Failed to load wods.json:', error);
  }
}

document.addEventListener('DOMContentLoaded', loadWods);
